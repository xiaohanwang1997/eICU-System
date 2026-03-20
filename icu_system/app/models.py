from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='doctor', nullable=False)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Patient(db.Model):
    __tablename__ = 'patient'

    patientunitstayid = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(100))
    gender = db.Column(db.String(20))
    age = db.Column(db.String(20))
    ethnicity = db.Column(db.String(50))
    hospitalid = db.Column(db.Integer)
    unitadmitsource = db.Column(db.String(100))
    unitdischargestatus = db.Column(db.String(50))
    diagnosis_summary = db.Column(db.String(255))

    vitals = db.relationship('VitalPeriodic', backref='patient', lazy=True)
    labs = db.relationship('Lab', backref='patient', lazy=True)
    medications = db.relationship('Medication', backref='patient', lazy=True)
    diagnoses = db.relationship('Diagnosis', backref='patient', lazy=True)
    notes = db.relationship('Note', backref='patient', lazy=True)


class VitalPeriodic(db.Model):
    __tablename__ = 'vital_periodic'

    id = db.Column(db.Integer, primary_key=True)
    patientunitstayid = db.Column(db.Integer, db.ForeignKey('patient.patientunitstayid'), nullable=False)
    observationoffset = db.Column(db.Integer, nullable=False)
    heartrate = db.Column(db.Float)
    systemicsystolic = db.Column(db.Float)
    systemicdiastolic = db.Column(db.Float)
    spo2 = db.Column(db.Float)
    respiration = db.Column(db.Float)
    temperature = db.Column(db.Float)


class Lab(db.Model):
    __tablename__ = 'lab'

    id = db.Column(db.Integer, primary_key=True)
    patientunitstayid = db.Column(db.Integer, db.ForeignKey('patient.patientunitstayid'), nullable=False)
    labresultoffset = db.Column(db.Integer)
    labname = db.Column(db.String(100))
    labresult = db.Column(db.String(50))
    labmeasurenamesystem = db.Column(db.String(50))


class Medication(db.Model):
    __tablename__ = 'medication'

    id = db.Column(db.Integer, primary_key=True)
    patientunitstayid = db.Column(db.Integer, db.ForeignKey('patient.patientunitstayid'), nullable=False)
    drugname = db.Column(db.String(100))
    dosage = db.Column(db.String(50))
    routeadmin = db.Column(db.String(50))
    frequency = db.Column(db.String(50))


class Diagnosis(db.Model):
    __tablename__ = 'diagnosis'

    id = db.Column(db.Integer, primary_key=True)
    patientunitstayid = db.Column(db.Integer, db.ForeignKey('patient.patientunitstayid'), nullable=False)
    diagnosisstring = db.Column(db.String(255))
    icd9code = db.Column(db.String(20))


class Note(db.Model):
    __tablename__ = 'note'

    id = db.Column(db.Integer, primary_key=True)
    patientunitstayid = db.Column(db.Integer, db.ForeignKey('patient.patientunitstayid'), nullable=False)
    noteoffset = db.Column(db.Integer)
    notetext = db.Column(db.Text)
