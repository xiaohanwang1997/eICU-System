from copy import deepcopy

from app.schemas.patient import (
    ClinicalNote,
    DiagnosisRecord,
    MedicationRecord,
    PatientDetail,
    PatientSummary,
    VitalSigns,
)


DOCTOR_USER = {
    # Use a normal domain; .local is rejected by email-validator (reserved TLD).
    "email": "doctor@example.com",
    "password": "doctor123",
    "name": "Dr. Maya Chen",
}

PATIENTS: dict[int, PatientDetail] = {
    1: PatientDetail(
        id=1,
        display_id=1001,
        mrn="ICU-1001",
        full_name="John Carter",
        room="ICU-12",
        primary_diagnosis="Sepsis with respiratory distress",
        age=67,
        gender="Male",
        clinical_status="Critical",
        latest_hr=102.0,
        latest_spo2=94.0,
        allergies=["Penicillin", "Latex"],
        medications=[
            MedicationRecord(
                id=1,
                name="Meropenem",
                dosage="1 g IV",
                schedule="Every 8 hours",
                status="Active",
            ),
            MedicationRecord(
                id=2,
                name="Norepinephrine",
                dosage="4 mcg/min",
                schedule="Continuous infusion",
                status="Active",
            ),
        ],
        care_plan="Maintain hemodynamic stability, monitor cultures, and wean oxygen as tolerated.",
        care_providers=[
            {"role": "Doctor", "name": "Dr. Maya Chen"},
            {"role": "Respiratory Therapist", "name": "Alex Rivera"},
        ],
        past_medical_history=["Type 2 diabetes", "Hypertension", "CKD stage 2"],
        diagnoses=[
            DiagnosisRecord(
                id=1,
                diagnosis="Septic shock",
                status="Confirmed",
                clinician="Dr. Maya Chen",
            )
        ],
        notes=[
            ClinicalNote(
                id=1,
                author="Dr. Maya Chen",
                note_type="Progress Note",
                content="Patient responding to fluids and vasopressors. Continue antibiotic coverage.",
            )
        ],
        treatments=["IV fluids", "Broad-spectrum antibiotics", "Oxygen therapy"],
        assigned_nurses=["Nurse Taylor"],
        vitals=VitalSigns(
            heart_rate=102,
            blood_pressure="102/64",
            oxygen_saturation=94,
            temperature_c=38.1,
        ),
    ),
    2: PatientDetail(
        id=2,
        display_id=1002,
        mrn="ICU-1002",
        full_name="Maria Chen",
        room="ICU-07",
        primary_diagnosis="Post-operative monitoring",
        age=54,
        gender="Female",
        clinical_status="Stable",
        latest_hr=80.0,
        latest_spo2=99.0,
        allergies=["Aspirin sensitivity"],
        medications=[
            MedicationRecord(
                id=3,
                name="Heparin",
                dosage="5000 units",
                schedule="Every 12 hours",
                status="Active",
            )
        ],
        care_plan="Monitor cardiac rhythm, trend troponins, and manage pain.",
        care_providers=[
            {"role": "Doctor", "name": "Dr. Maya Chen"},
            {"role": "Nurse", "name": "Nurse Patel"},
        ],
        past_medical_history=["Hyperlipidemia", "Coronary artery disease"],
        diagnoses=[
            DiagnosisRecord(
                id=2,
                diagnosis="NSTEMI",
                status="Confirmed",
                clinician="Dr. Maya Chen",
            )
        ],
        notes=[
            ClinicalNote(
                id=2,
                author="Dr. Maya Chen",
                note_type="Admission Note",
                content="Chest pain improving after initial treatment. Continue telemetry.",
            )
        ],
        treatments=["Telemetry", "Anticoagulation"],
        assigned_nurses=["Nurse Patel"],
        vitals=VitalSigns(
            heart_rate=80,
            blood_pressure="128/78",
            oxygen_saturation=99,
            temperature_c=36.8,
        ),
    ),
}


def list_patients(query: str | None = None) -> list[PatientSummary]:
    patients = list(PATIENTS.values())
    if query:
        lowered = query.lower()
        patients = [
            patient
            for patient in patients
            if lowered in patient.full_name.lower()
            or lowered in patient.mrn.lower()
            or lowered in patient.primary_diagnosis.lower()
            or lowered in str(patient.display_id)
        ]
    return [PatientSummary(**patient.model_dump()) for patient in patients]


def get_patient(patient_id: int) -> PatientDetail | None:
    patient = PATIENTS.get(patient_id)
    return deepcopy(patient) if patient else None


def add_diagnosis(patient_id: int, diagnosis: str, status: str) -> DiagnosisRecord | None:
    patient = PATIENTS.get(patient_id)
    if not patient:
        return None
    record = DiagnosisRecord(
        id=len(patient.diagnoses) + 1,
        diagnosis=diagnosis,
        status=status,
        clinician=DOCTOR_USER["name"],
    )
    patient.diagnoses.append(record)
    return record


def add_note(patient_id: int, note_type: str, content: str) -> ClinicalNote | None:
    patient = PATIENTS.get(patient_id)
    if not patient:
        return None
    record = ClinicalNote(
        id=len(patient.notes) + 1,
        author=DOCTOR_USER["name"],
        note_type=note_type,
        content=content,
    )
    patient.notes.append(record)
    return record


def assign_nurse(patient_id: int, nurse_name: str) -> list[str] | None:
    patient = PATIENTS.get(patient_id)
    if not patient:
        return None
    if nurse_name not in patient.assigned_nurses:
        patient.assigned_nurses.append(nurse_name)
    return patient.assigned_nurses


def prescribe_medication(
    patient_id: int, name: str, dosage: str, schedule: str
) -> MedicationRecord | None:
    patient = PATIENTS.get(patient_id)
    if not patient:
        return None
    record = MedicationRecord(
        id=len(patient.medications) + 1,
        name=name,
        dosage=dosage,
        schedule=schedule,
        status="Active",
    )
    patient.medications.append(record)
    return record
