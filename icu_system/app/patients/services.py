from collections import Counter

from ..models import Lab, Medication, Note, Patient, VitalPeriodic


def get_dashboard_stats():
    patients = Patient.query.all()
    status_counter = Counter((p.unitdischargestatus or 'Unknown') for p in patients)
    return {
        'total_patients': len(patients),
        'status_breakdown': dict(status_counter),
    }


def get_latest_vitals_map(patient_ids):
    result = {}
    for patient_id in patient_ids:
        latest = (
            VitalPeriodic.query
            .filter_by(patientunitstayid=patient_id)
            .order_by(VitalPeriodic.observationoffset.desc())
            .first()
        )
        result[patient_id] = latest
    return result


def get_patient_detail_bundle(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    vitals = (
        VitalPeriodic.query
        .filter_by(patientunitstayid=patient_id)
        .order_by(VitalPeriodic.observationoffset.asc())
        .all()
    )
    labs = (
        Lab.query
        .filter_by(patientunitstayid=patient_id)
        .order_by(Lab.labresultoffset.desc())
        .all()
    )
    medications = Medication.query.filter_by(patientunitstayid=patient_id).all()
    notes = (
        Note.query
        .filter_by(patientunitstayid=patient_id)
        .order_by(Note.noteoffset.desc())
        .all()
    )
    return {
        'patient': patient,
        'vitals': vitals,
        'labs': labs,
        'medications': medications,
        'notes': notes,
    }
