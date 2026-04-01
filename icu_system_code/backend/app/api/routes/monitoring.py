from fastapi import APIRouter, HTTPException

from app.schemas.patient import VitalSigns
from app.services.mock_data import get_patient
from app.services.patient_db import get_monitoring_from_db

router = APIRouter(prefix="/patients/{patient_id}/monitoring", tags=["monitoring"])


@router.get("", response_model=VitalSigns)
def get_monitoring_snapshot(patient_id: int) -> VitalSigns:
    db_vitals = get_monitoring_from_db(patient_id)
    if db_vitals:
        return db_vitals
    patient = get_patient(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient.vitals
