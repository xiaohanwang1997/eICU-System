import json

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from app.services.agent_service import run_gemini_agent, stream_gemini_agent
from app.services.mock_data import get_patient
from app.services.patient_db import get_patient_from_db

router = APIRouter(prefix="/agent", tags=["agent"])


class AgentChatContext(BaseModel):
    page: str | None = None
    patient_name: str | None = None
    clinical_status: str | None = None
    primary_diagnosis: str | None = None


class AgentChatMessage(BaseModel):
    role: str
    text: str = Field(min_length=1, max_length=4000)


class AgentChatRequest(BaseModel):
    patient_id: int
    message: str = Field(min_length=1, max_length=1000)
    context: AgentChatContext | None = None
    history: list[AgentChatMessage] = Field(default_factory=list)


class AgentChatResponse(BaseModel):
    reply: str


def _load_patient(patient_id: int):
    patient = get_patient_from_db(patient_id)
    if not patient:
        patient = get_patient(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


def _history_payload(payload: AgentChatRequest) -> list[dict[str, str]]:
    normalized: list[dict[str, str]] = []
    for turn in payload.history[-12:]:
        role = turn.role.strip().lower()
        if role not in {"user", "assistant"}:
            continue
        text = turn.text.strip()
        if not text:
            continue
        normalized.append({"role": role, "text": text})
    return normalized


def _sse_event(data: dict[str, str]) -> str:
    return f"data: {json.dumps(data, ensure_ascii=False)}\n\n"


@router.post("/chat", response_model=AgentChatResponse)
def chat_with_agent(payload: AgentChatRequest) -> AgentChatResponse:
    patient = _load_patient(payload.patient_id)

    try:
        reply = run_gemini_agent(patient, payload.message.strip(), _history_payload(payload))
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Gemini request failed: {exc}") from exc

    return AgentChatResponse(reply=reply)


@router.post("/chat/stream")
def stream_chat_with_agent(payload: AgentChatRequest) -> StreamingResponse:
    patient = _load_patient(payload.patient_id)
    history = _history_payload(payload)

    def event_stream():
        try:
            for chunk in stream_gemini_agent(patient, payload.message.strip(), history):
                yield _sse_event({"type": "delta", "text": chunk})
            yield _sse_event({"type": "done", "text": ""})
        except RuntimeError as exc:
            yield _sse_event({"type": "error", "text": str(exc)})
        except Exception as exc:
            yield _sse_event({"type": "error", "text": f"Gemini request failed: {exc}"})

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
