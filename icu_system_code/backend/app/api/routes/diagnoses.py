from fastapi import APIRouter, HTTPException

from app.schemas.clinical import CreateDiagnosisRequest
from app.schemas.patient import DiagnosisRecord
from app.services.mock_data import add_diagnosis

router = APIRouter(prefix="/patients/{patient_id}/diagnoses", tags=["diagnoses"])


@router.post("", response_model=DiagnosisRecord)
def create_diagnosis(patient_id: int, payload: CreateDiagnosisRequest) -> DiagnosisRecord:
    record = add_diagnosis(
        patient_id=patient_id,
        diagnosis=payload.diagnosis,
        status=payload.status,
    )
    if not record:
        raise HTTPException(status_code=404, detail="Patient not found")
    return record
