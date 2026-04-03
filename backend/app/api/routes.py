from __future__ import annotations

import json
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.services.patient_service import get_patients, get_patient_detail
from app.services.agent_service import stream_agent_response

router = APIRouter()


# ---------------------------------------------------------------------------
# DB dependency
# ---------------------------------------------------------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Auth (simple mock – replace with real JWT in production)
# ---------------------------------------------------------------------------

class LoginRequest(BaseModel):
    email: str
    password: str


MOCK_USERS = {
    "doctor@example.com": {
        "password": "doctor123",
        "doctor_name": "Dr. Alex Rivera",
        "access_token": "mock-token-doctor",
    },
    "nurse@example.com": {
        "password": "nurse123",
        "doctor_name": "Nurse Jordan Lee",
        "access_token": "mock-token-nurse",
    },
}


@router.post("/auth/login")
def login(body: LoginRequest):
    user = MOCK_USERS.get(body.email)
    if not user or user["password"] != body.password:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {
        "access_token": user["access_token"],
        "doctor_name": user["doctor_name"],
        "token_type": "bearer",
    }


# ---------------------------------------------------------------------------
# Patients
# ---------------------------------------------------------------------------

@router.get("/patients")
def list_patients(q: Optional[str] = None, db: Session = Depends(get_db)):
    return get_patients(db, q)


@router.get("/patients/{patient_id}")
def patient_detail(patient_id: int, db: Session = Depends(get_db)):
    patient = get_patient_detail(db, patient_id)
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


# ---------------------------------------------------------------------------
# Agent chat – both routes fetch full patient data from DB and pass to Gemini
# ---------------------------------------------------------------------------

class ChatHistoryMessage(BaseModel):
    role: str
    text: str


class AgentContext(BaseModel):
    page: Optional[str] = None
    patient_name: Optional[str] = None
    clinical_status: Optional[str] = None
    primary_diagnosis: Optional[str] = None


class AgentChatRequest(BaseModel):
    patient_id: int
    message: str
    history: Optional[list[ChatHistoryMessage]] = []
    context: Optional[AgentContext] = None


@router.post("/agent/chat/stream")
async def agent_chat_stream(body: AgentChatRequest, db: Session = Depends(get_db)):
    patient = get_patient_detail(db, body.patient_id)
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")

    history = [h.model_dump() for h in (body.history or [])]

    return StreamingResponse(
        stream_agent_response(
            patient=patient,
            message=body.message,
            history=history,
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@router.post("/agent/chat")
async def agent_chat(body: AgentChatRequest, db: Session = Depends(get_db)):
    """Non-streaming fallback – returns full reply at once."""
    patient = get_patient_detail(db, body.patient_id)
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")

    history = [h.model_dump() for h in (body.history or [])]
    full_reply = ""

    async for chunk in stream_agent_response(
        patient=patient,
        message=body.message,
        history=history,
    ):
        if chunk.startswith("data: "):
            data = json.loads(chunk[6:].strip())
            if data.get("type") == "delta":
                full_reply += data.get("text", "")

    return {"reply": full_reply}


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

@router.get("/")
def root():
    return {"status": "ok", "service": "eICU API"}
