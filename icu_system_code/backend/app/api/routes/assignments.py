from fastapi import APIRouter, HTTPException

from app.schemas.clinical import AssignNurseRequest
from app.services.mock_data import assign_nurse

router = APIRouter(prefix="/patients/{patient_id}/assign-nurse", tags=["assignments"])


@router.post("")
def create_assignment(patient_id: int, payload: AssignNurseRequest) -> dict[str, list[str]]:
    nurses = assign_nurse(patient_id=patient_id, nurse_name=payload.nurse_name)
    if not nurses:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"assigned_nurses": nurses}
