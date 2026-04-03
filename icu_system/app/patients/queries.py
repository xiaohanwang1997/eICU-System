from sqlalchemy import cast, or_, String

from ..models import Note, Patient, VitalPeriodic


def search_patients(keyword: str):
    query = Patient.query
    if keyword:
        query = query.filter(
            or_(
                Patient.patient_name.ilike(f'%{keyword}%'),
                Patient.diagnosis_summary.ilike(f'%{keyword}%'),
                cast(Patient.patientunitstayid, String).ilike(f'%{keyword}%'),
            )
        )
    return query.order_by(Patient.patientunitstayid).all()


def get_patient_by_id(patient_id: int):
    return Patient.query.get_or_404(patient_id)


def get_vitals_for_patient(patient_id: int):
    return (
        VitalPeriodic.query
        .filter_by(patientunitstayid=patient_id)
        .order_by(VitalPeriodic.observationoffset.asc())
        .all()
    )


def get_notes_for_patient(patient_id: int):
    return (
        Note.query
        .filter_by(patientunitstayid=patient_id)
        .order_by(Note.noteoffset.desc())
        .all()
    )
