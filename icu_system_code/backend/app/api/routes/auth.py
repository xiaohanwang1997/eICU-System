from fastapi import APIRouter, HTTPException, status

from app.core.security import create_access_token
from app.schemas.clinical import LoginRequest, LoginResponse
from app.services.mock_data import DOCTOR_USER

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest) -> LoginResponse:
    if (
        payload.email != DOCTOR_USER["email"]
        or payload.password != DOCTOR_USER["password"]
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    return LoginResponse(
        access_token=create_access_token(subject=payload.email),
        doctor_name=DOCTOR_USER["name"],
    )
