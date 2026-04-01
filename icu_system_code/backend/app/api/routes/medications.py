from fastapi import APIRouter, HTTPException

from app.schemas.clinical import PrescribeMedicationRequest
from app.schemas.patient import MedicationRecord
from app.services.mock_data import prescribe_medication

router = APIRouter(prefix="/patients/{patient_id}/medications", tags=["medications"])


@router.post("", response_model=MedicationRecord)
def create_medication(
    patient_id: int, payload: PrescribeMedicationRequest
) -> MedicationRecord:
    record = prescribe_medication(
        patient_id=patient_id,
        name=payload.name,
        dosage=payload.dosage,
        schedule=payload.schedule,
    )
    if not record:
        raise HTTPException(status_code=404, detail="Patient not found")
    return record
