from fastapi import APIRouter, HTTPException, Query

from app.schemas.patient import PatientDetail, PatientSummary
from app.services.mock_data import get_patient, list_patients
from app.services.patient_db import get_patient_from_db, list_patients_from_db

router = APIRouter(prefix="/patients", tags=["patients"])


@router.get("", response_model=list[PatientSummary])
def search_patients(q: str | None = Query(default=None)) -> list[PatientSummary]:
    db_patients = list_patients_from_db(query=q)
    if db_patients is not None:
        return db_patients
    return list_patients(query=q)


@router.get("/{patient_id}", response_model=PatientDetail)
def get_patient_detail(patient_id: int) -> PatientDetail:
    patient = get_patient_from_db(patient_id)
    if patient:
        return patient
    patient = get_patient(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient
