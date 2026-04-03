from __future__ import annotations

from typing import Any

from app.core.config import settings
from app.schemas.patient import PatientDetail, PatientSummary, VitalSigns


LIST_PATIENTS_SQL = """
WITH latest_vitals AS (
    SELECT DISTINCT ON (patientunitstayid)
        patientunitstayid,
        heartrate,
        sao2,
        temperature,
        systemicsystolic,
        systemicdiastolic
    FROM vitalperiodic
    ORDER BY patientunitstayid, observationoffset DESC NULLS LAST
)
SELECT
    p.patientunitstayid,
    p.uniquepid,
    p.gender,
    p.age,
    p.apacheadmissiondx,
    p.wardid,
    p.unittype,
    lv.heartrate,
    lv.sao2
FROM patient p
LEFT JOIN latest_vitals lv ON lv.patientunitstayid = p.patientunitstayid
ORDER BY p.patientunitstayid
LIMIT 100
"""


LIST_PATIENTS_FILTER_SQL = """
WITH latest_vitals AS (
    SELECT DISTINCT ON (patientunitstayid)
        patientunitstayid,
        heartrate,
        sao2,
        temperature,
        systemicsystolic,
        systemicdiastolic
    FROM vitalperiodic
    ORDER BY patientunitstayid, observationoffset DESC NULLS LAST
)
SELECT
    p.patientunitstayid,
    p.uniquepid,
    p.gender,
    p.age,
    p.apacheadmissiondx,
    p.wardid,
    p.unittype,
    lv.heartrate,
    lv.sao2
FROM patient p
LEFT JOIN latest_vitals lv ON lv.patientunitstayid = p.patientunitstayid
WHERE (
    CAST(p.patientunitstayid AS TEXT) ILIKE %(q_like)s
    OR COALESCE(p.uniquepid, '') ILIKE %(q_like)s
    OR COALESCE(p.apacheadmissiondx, '') ILIKE %(q_like)s
)
ORDER BY p.patientunitstayid
LIMIT 100
"""


PATIENT_DETAIL_SQL = """
WITH latest_vitals AS (
    SELECT DISTINCT ON (patientunitstayid)
        patientunitstayid,
        heartrate,
        sao2,
        temperature,
        systemicsystolic,
        systemicdiastolic
    FROM vitalperiodic
    ORDER BY patientunitstayid, observationoffset DESC NULLS LAST
)
SELECT
    p.patientunitstayid,
    p.uniquepid,
    p.gender,
    p.age,
    p.apacheadmissiondx,
    p.wardid,
    p.unittype,
    lv.heartrate,
    lv.sao2,
    lv.temperature,
    lv.systemicsystolic,
    lv.systemicdiastolic
FROM patient p
LEFT JOIN latest_vitals lv ON lv.patientunitstayid = p.patientunitstayid
WHERE p.patientunitstayid = %(patient_id)s
LIMIT 1
"""


def _get_psycopg():
    try:
        import psycopg
        from psycopg.rows import dict_row
    except ImportError:
        return None, None
    return psycopg, dict_row


def _fetch_all(query: str, params: dict[str, Any]) -> list[dict[str, Any]] | None:
    if not settings.database_url:
        return None
    psycopg, dict_row = _get_psycopg()
    if not psycopg:
        return None
    try:
        with psycopg.connect(settings.database_url, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                rows = cur.fetchall()
        return [dict(row) for row in rows]
    except Exception:
        return None


def _fetch_one(query: str, params: dict[str, Any]) -> dict[str, Any] | None:
    rows = _fetch_all(query, params)
    if not rows:
        return None
    return rows[0]


def _parse_age(age: Any) -> int:
    if age is None:
        return 0
    text = str(age).strip()
    if text.startswith(">"):
        return 90
    try:
        return int(float(text))
    except ValueError:
        return 0


def _room_label(wardid: Any, unittype: Any) -> str:
    if wardid not in (None, ""):
        return f"Ward {wardid}"
    if unittype:
        return str(unittype)
    return "ICU"


def _display_name(uniquepid: Any, patientunitstayid: Any) -> str:
    identifier = uniquepid or patientunitstayid
    return f"Patient {identifier}"


def _status(dx: Any, hr: Any, sao2: Any) -> str:
    diagnosis = str(dx or "").lower()
    severe_terms = ("sepsis", "shock", "failure", "arrest", "hemorrhage")
    if any(term in diagnosis for term in severe_terms):
        return "Critical"
    try:
        if hr is not None and float(hr) >= 110:
            return "Critical"
        if sao2 is not None and float(sao2) <= 92:
            return "Critical"
    except (TypeError, ValueError):
        pass
    return "Stable"


def _blood_pressure(sys: Any, dia: Any) -> str:
    if sys is None or dia is None:
        return "N/A"
    return f"{int(sys)}/{int(dia)}"


def _to_summary(row: dict[str, Any]) -> PatientSummary:
    stay_id = int(row["patientunitstayid"])
    hr = float(row["heartrate"]) if row.get("heartrate") is not None else 0.0
    sao2 = float(row["sao2"]) if row.get("sao2") is not None else 0.0
    return PatientSummary(
        id=stay_id,
        display_id=stay_id,
        mrn=str(row.get("uniquepid") or f"ICU-{stay_id}"),
        full_name=_display_name(row.get("uniquepid"), stay_id),
        room=_room_label(row.get("wardid"), row.get("unittype")),
        primary_diagnosis=str(row.get("apacheadmissiondx") or "No diagnosis listed"),
        age=_parse_age(row.get("age")),
        gender=str(row.get("gender") or "Unknown"),
        clinical_status=_status(row.get("apacheadmissiondx"), hr, sao2),
        latest_hr=hr,
        latest_spo2=sao2,
    )


def list_patients_from_db(query: str | None = None) -> list[PatientSummary] | None:
    q = query.strip() if query else None
    if q:
        rows = _fetch_all(LIST_PATIENTS_FILTER_SQL, {"q_like": f"%{q}%"})
    else:
        rows = _fetch_all(LIST_PATIENTS_SQL, {})
    if rows is None:
        return None
    return [_to_summary(row) for row in rows]


def get_patient_from_db(patient_id: int) -> PatientDetail | None:
    row = _fetch_one(PATIENT_DETAIL_SQL, {"patient_id": patient_id})
    if row is None:
        return None
    summary = _to_summary(row)
    temp = float(row["temperature"]) if row.get("temperature") is not None else 0.0
    detail = PatientDetail(
        **summary.model_dump(),
        allergies=[],
        medications=[],
        care_plan="",
        care_providers=[],
        past_medical_history=[],
        diagnoses=[],
        notes=[],
        treatments=[],
        assigned_nurses=[],
        vitals=VitalSigns(
            heart_rate=int(row["heartrate"]) if row.get("heartrate") is not None else 0,
            blood_pressure=_blood_pressure(
                row.get("systemicsystolic"), row.get("systemicdiastolic")
            ),
            oxygen_saturation=int(row["sao2"]) if row.get("sao2") is not None else 0,
            temperature_c=temp,
        ),
    )
    return detail


def get_monitoring_from_db(patient_id: int) -> VitalSigns | None:
    row = _fetch_one(PATIENT_DETAIL_SQL, {"patient_id": patient_id})
    if row is None:
        return None
    return VitalSigns(
        heart_rate=int(row["heartrate"]) if row.get("heartrate") is not None else 0,
        blood_pressure=_blood_pressure(
            row.get("systemicsystolic"), row.get("systemicdiastolic")
        ),
        oxygen_saturation=int(row["sao2"]) if row.get("sao2") is not None else 0,
        temperature_c=float(row["temperature"]) if row.get("temperature") is not None else 0.0,
    )
