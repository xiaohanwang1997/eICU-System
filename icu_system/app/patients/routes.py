from flask import Blueprint, jsonify, render_template, request
from flask_login import login_required

from ..extensions import db
from ..models import Note
from .queries import search_patients
from .services import get_patient_detail_bundle


patients_bp = Blueprint('patients', __name__, url_prefix='/patients')


@patients_bp.route('/search')
@login_required
def patient_search():
    keyword = request.args.get('q', '').strip()
    patients = search_patients(keyword)
    return render_template('dashboard.html', patients=patients, stats=None, latest_vitals={})


@patients_bp.route('/<int:patient_id>')
@login_required
def detail(patient_id):
    data = get_patient_detail_bundle(patient_id)
    return render_template('patient_detail.html', **data)


@patients_bp.route('/api/<int:patient_id>/vitals')
@login_required
def vitals_api(patient_id):
    data = get_patient_detail_bundle(patient_id)
    vitals = [
        {
            'offset': v.observationoffset,
            'heartrate': v.heartrate,
            'systolic': v.systemicsystolic,
            'diastolic': v.systemicdiastolic,
            'spo2': v.spo2,
            'respiration': v.respiration,
            'temperature': v.temperature,
        }
        for v in data['vitals']
    ]
    return jsonify(vitals)


@patients_bp.route('/api/<int:patient_id>/notes', methods=['POST'])
@login_required
def add_note(patient_id):
    payload = request.get_json(silent=True) or {}
    text = (payload.get('notetext') or '').strip()

    if not text:
        return jsonify({'error': 'Note text is required.'}), 400

    note = Note(patientunitstayid=patient_id, noteoffset=0, notetext=text)
    db.session.add(note)
    db.session.commit()
    return jsonify({'message': 'Note added successfully.'}), 201
