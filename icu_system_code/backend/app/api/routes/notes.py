from fastapi import APIRouter, HTTPException

from app.schemas.clinical import CreateNoteRequest
from app.schemas.patient import ClinicalNote
from app.services.mock_data import add_note

router = APIRouter(prefix="/patients/{patient_id}/notes", tags=["notes"])


@router.post("", response_model=ClinicalNote)
def create_note(patient_id: int, payload: CreateNoteRequest) -> ClinicalNote:
    record = add_note(
        patient_id=patient_id,
        note_type=payload.note_type,
        content=payload.content,
    )
    if not record:
        raise HTTPException(status_code=404, detail="Patient not found")
    return record
