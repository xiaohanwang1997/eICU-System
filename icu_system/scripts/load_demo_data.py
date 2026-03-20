from app import create_app
from app.extensions import db
from app.models import Diagnosis, Lab, Medication, Note, Patient, VitalPeriodic


app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    patient_1 = Patient(
        patientunitstayid=1001,
        patient_name='John Carter',
        gender='Male',
        age='67',
        ethnicity='Caucasian',
        hospitalid=1,
        unitadmitsource='ED',
        unitdischargestatus='Critical',
        diagnosis_summary='Sepsis with respiratory failure',
    )
    patient_2 = Patient(
        patientunitstayid=1002,
        patient_name='Maria Chen',
        gender='Female',
        age='54',
        ethnicity='Asian',
        hospitalid=1,
        unitadmitsource='Ward',
        unitdischargestatus='Stable',
        diagnosis_summary='Post-operative monitoring',
    )

    db.session.add_all([patient_1, patient_2])

    vitals = [
        VitalPeriodic(patientunitstayid=1001, observationoffset=0, heartrate=110, systemicsystolic=92, systemicdiastolic=60, spo2=90, respiration=24, temperature=38.4),
        VitalPeriodic(patientunitstayid=1001, observationoffset=30, heartrate=106, systemicsystolic=95, systemicdiastolic=62, spo2=92, respiration=22, temperature=38.1),
        VitalPeriodic(patientunitstayid=1001, observationoffset=60, heartrate=102, systemicsystolic=98, systemicdiastolic=64, spo2=94, respiration=20, temperature=37.8),
        VitalPeriodic(patientunitstayid=1002, observationoffset=0, heartrate=82, systemicsystolic=118, systemicdiastolic=75, spo2=98, respiration=16, temperature=36.9),
        VitalPeriodic(patientunitstayid=1002, observationoffset=30, heartrate=80, systemicsystolic=120, systemicdiastolic=78, spo2=99, respiration=16, temperature=36.8),
    ]
    db.session.add_all(vitals)

    db.session.add_all([
        Medication(patientunitstayid=1001, drugname='Vancomycin', dosage='1 g', routeadmin='IV', frequency='q12h'),
        Medication(patientunitstayid=1002, drugname='Acetaminophen', dosage='500 mg', routeadmin='PO', frequency='PRN'),
        Lab(patientunitstayid=1001, labresultoffset=60, labname='Lactate', labresult='2.8', labmeasurenamesystem='mmol/L'),
        Lab(patientunitstayid=1002, labresultoffset=30, labname='WBC', labresult='7.1', labmeasurenamesystem='K/uL'),
        Diagnosis(patientunitstayid=1001, diagnosisstring='Sepsis', icd9code='995.91'),
        Diagnosis(patientunitstayid=1002, diagnosisstring='Observation after surgery', icd9code='V67.00'),
        Note(patientunitstayid=1001, noteoffset=60, notetext='Patient improving after fluids and antibiotics.'),
        Note(patientunitstayid=1002, noteoffset=30, notetext='Pain controlled. Continue monitoring.'),
    ])

    db.session.commit()
    print('Demo data loaded successfully.')
