from flask import Blueprint, render_template
from flask_login import login_required

from ..models import Patient
from ..patients.services import get_dashboard_stats, get_latest_vitals_map


dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/')
@login_required
def home():
    patients = Patient.query.order_by(Patient.patientunitstayid).limit(20).all()
    stats = get_dashboard_stats()
    latest_vitals = get_latest_vitals_map([p.patientunitstayid for p in patients])
    return render_template(
        'dashboard.html',
        patients=patients,
        stats=stats,
        latest_vitals=latest_vitals,
    )
