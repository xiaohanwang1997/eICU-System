from pydantic import BaseModel


class CareProvider(BaseModel):
    role: str
    name: str


class MedicationRecord(BaseModel):
    id: int
    name: str
    dosage: str
    schedule: str
    status: str


class DiagnosisRecord(BaseModel):
    id: int
    diagnosis: str
    status: str
    clinician: str


class ClinicalNote(BaseModel):
    id: int
    author: str
    note_type: str
    content: str


class VitalSigns(BaseModel):
    heart_rate: int
    blood_pressure: str
    oxygen_saturation: int
    temperature_c: float


class PatientSummary(BaseModel):
    id: int
    display_id: int
    mrn: str
    full_name: str
    room: str
    primary_diagnosis: str
    age: int
    gender: str
    clinical_status: str
    latest_hr: float
    latest_spo2: float


class PatientDetail(PatientSummary):
    allergies: list[str]
    medications: list[MedicationRecord]
    care_plan: str
    care_providers: list[CareProvider]
    past_medical_history: list[str]
    diagnoses: list[DiagnosisRecord]
    notes: list[ClinicalNote]
    treatments: list[str]
    assigned_nurses: list[str]
    vitals: VitalSigns
