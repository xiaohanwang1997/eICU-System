from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    doctor_name: str


class CreateDiagnosisRequest(BaseModel):
    diagnosis: str
    status: str


class AssignNurseRequest(BaseModel):
    nurse_name: str


class CreateNoteRequest(BaseModel):
    note_type: str
    content: str


class PrescribeMedicationRequest(BaseModel):
    name: str
    dosage: str
    schedule: str
