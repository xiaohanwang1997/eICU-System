"""
Patient service – builds API response dicts from raw eICU SQLite tables.
All queries use raw SQL via SQLAlchemy text() for performance.
"""

from __future__ import annotations

import hashlib
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session

# ---------------------------------------------------------------------------
# Name generation (dataset is de-identified – generate deterministic names)
# ---------------------------------------------------------------------------

_MALE_FIRST = [
    "Michael", "James", "Robert", "David", "William",
    "Richard", "Joseph", "Thomas", "Charles", "Christopher",
    "Daniel", "Matthew", "Anthony", "Donald", "Mark",
]
_FEMALE_FIRST = [
    "Mary", "Patricia", "Jennifer", "Linda", "Barbara",
    "Elizabeth", "Susan", "Jessica", "Sarah", "Karen",
    "Lisa", "Nancy", "Betty", "Margaret", "Sandra",
]
_LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones",
    "Garcia", "Miller", "Davis", "Wilson", "Taylor",
    "Anderson", "Thomas", "Jackson", "White", "Harris",
    "Martin", "Thompson", "Moore", "Martinez", "Robinson",
]


def _gen_name(uniquepid: str, gender: str) -> str:
    h = int(hashlib.md5(str(uniquepid).encode()).hexdigest(), 16)
    pool = _MALE_FIRST if str(gender).lower().startswith("m") else _FEMALE_FIRST
    first = pool[h % len(pool)]
    last = _LAST_NAMES[(h >> 8) % len(_LAST_NAMES)]
    return f"{first} {last}"


def _parse_age(age_val: Any) -> int:
    if age_val is None:
        return 0
    s = str(age_val).strip()
    if s.startswith(">"):
        return 90
    try:
        return int(float(s))
    except (ValueError, TypeError):
        return 0


def _clinical_status(hr: float | None, spo2: float | None,
                     apache_mort: float | None) -> str:
    if hr and hr > 120:
        return "Critical"
    if spo2 and spo2 < 90:
        return "Critical"
    if apache_mort and apache_mort > 0.30:
        return "Critical"
    return "Stable"


def _row_to_dict(row) -> dict:
    if row is None:
        return {}
    if hasattr(row, "_mapping"):
        return dict(row._mapping)
    return dict(row)


# ---------------------------------------------------------------------------
# Patient list  (GET /api/patients)
# ---------------------------------------------------------------------------

def get_patients(db: Session, q: str | None = None) -> list[dict]:
    sql = text("""
        SELECT
            p.patientunitstayid,
            p.uniquepid,
            p.gender,
            p.age,
            p.unittype,
            p.wardid,
            p.hospitalid,
            p.unitdischargestatus
        FROM patient p
        ORDER BY p.patientunitstayid
        LIMIT 200
    """)
    rows = db.execute(sql).fetchall()

    result = []
    for row in rows:
        d = _row_to_dict(row)
        pid = d["patientunitstayid"]

        # ── latest vitals ──────────────────────────────────────────────────
        v = db.execute(text("""
            SELECT heartrate, sao2, temperature,
                   systemicsystolic, systemicdiastolic
            FROM vitalperiodic
            WHERE patientunitstayid = :pid
              AND heartrate IS NOT NULL
            ORDER BY observationoffset DESC
            LIMIT 1
        """), {"pid": pid}).fetchone()
        vitals = _row_to_dict(v)

        # ── APACHE mortality prediction ────────────────────────────────────
        apr = db.execute(text("""
            SELECT predictedicumortality
            FROM apachepatientresult
            WHERE patientunitstayid = :pid
            LIMIT 1
        """), {"pid": pid}).fetchone()
        apache_mort = float(apr[0]) if apr and apr[0] is not None else None

        # ── primary diagnosis ──────────────────────────────────────────────
        dx = db.execute(text("""
            SELECT diagnosisstring
            FROM diagnosis
            WHERE patientunitstayid = :pid
            ORDER BY diagnosisoffset ASC
            LIMIT 1
        """), {"pid": pid}).fetchone()
        primary_dx = dx[0] if dx else (d.get("apacheadmissiondx") or "Unknown")
        # Clean up path-style strings like "sepsis|infection|..."
        if primary_dx and "|" in str(primary_dx):
            primary_dx = str(primary_dx).split("|")[-1].strip().capitalize()

        hr = vitals.get("heartrate")
        spo2 = vitals.get("sao2")
        gender = str(d.get("gender") or "Unknown")
        age_parsed = _parse_age(d.get("age"))
        room = f"{d.get('unittype', 'ICU')} W{d.get('wardid', '')}"

        patient_item = {
            "id": pid,
            "display_id": pid % 10000 + 1000,
            "mrn": str(d.get("uniquepid") or f"ICU-{pid}"),
            "full_name": _gen_name(d.get("uniquepid", str(pid)), gender),
            "room": room,
            "primary_diagnosis": str(primary_dx)[:80],
            "age": age_parsed,
            "gender": gender.capitalize(),
            "clinical_status": _clinical_status(hr, spo2, apache_mort),
            "latest_hr": round(float(hr), 1) if hr else 0.0,
            "latest_spo2": round(float(spo2), 1) if spo2 else 0.0,
        }

        # Optional search filter
        if q:
            qlow = q.lower()
            searchable = (
                patient_item["full_name"].lower()
                + patient_item["mrn"].lower()
                + patient_item["primary_diagnosis"].lower()
            )
            if qlow not in searchable:
                continue

        result.append(patient_item)

    return result


# ---------------------------------------------------------------------------
# Patient detail  (GET /api/patients/{id})
# ---------------------------------------------------------------------------

def get_patient_detail(db: Session, pid: int) -> dict | None:
    # ── base patient row ───────────────────────────────────────────────────
    row = db.execute(text("""
        SELECT patientunitstayid, uniquepid, gender, age,
               unittype, wardid, hospitalid, apacheadmissiondx,
               admissionheight, admissionweight, unitdischargestatus
        FROM patient
        WHERE patientunitstayid = :pid
        LIMIT 1
    """), {"pid": pid}).fetchone()
    if row is None:
        return None
    d = _row_to_dict(row)

    gender = str(d.get("gender") or "Unknown").capitalize()
    age = _parse_age(d.get("age"))

    # ── latest vitals ──────────────────────────────────────────────────────
    v = db.execute(text("""
        SELECT heartrate, sao2, temperature,
               systemicsystolic, systemicdiastolic, systemicmean,
               respiration
        FROM vitalperiodic
        WHERE patientunitstayid = :pid
          AND heartrate IS NOT NULL
        ORDER BY observationoffset DESC
        LIMIT 1
    """), {"pid": pid}).fetchone()
    vd = _row_to_dict(v)

    hr     = vd.get("heartrate") or 0
    spo2   = vd.get("sao2") or 0
    temp   = vd.get("temperature") or 0
    sys_bp = vd.get("systemicsystolic") or 0
    dia_bp = vd.get("systemicdiastolic") or 0

    # ── APACHE ─────────────────────────────────────────────────────────────
    apr = db.execute(text("""
        SELECT predictedicumortality, apachescore, predictediculos
        FROM apachepatientresult
        WHERE patientunitstayid = :pid LIMIT 1
    """), {"pid": pid}).fetchone()
    aprd = _row_to_dict(apr)
    apache_mort = float(aprd.get("predictedicumortality") or 0)

    # ── primary diagnosis ──────────────────────────────────────────────────
    dx_rows = db.execute(text("""
        SELECT diagnosisid, diagnosisstring, diagnosispriority
        FROM diagnosis
        WHERE patientunitstayid = :pid
        ORDER BY diagnosisoffset ASC
        LIMIT 10
    """), {"pid": pid}).fetchall()
    diagnoses = []
    primary_dx = d.get("apacheadmissiondx") or "Unknown"
    for i, dx in enumerate(dx_rows):
        dxd = _row_to_dict(dx)
        s = str(dxd.get("diagnosisstring") or "")
        label = s.split("|")[-1].strip().capitalize() if "|" in s else s
        if i == 0:
            primary_dx = label
        diagnoses.append({
            "id": dxd.get("diagnosisid", i + 1),
            "diagnosis": label,
            "status": "Active" if dxd.get("activeupondischarge") else "Resolved",
            "clinician": "Attending",
        })

    if not diagnoses:
        diagnoses = [{"id": 1, "diagnosis": str(primary_dx), "status": "Active", "clinician": "Attending"}]

    # ── allergies ──────────────────────────────────────────────────────────
    allergy_rows = db.execute(text("""
        SELECT DISTINCT allergyname
        FROM allergy
        WHERE patientunitstayid = :pid
          AND allergyname IS NOT NULL
        LIMIT 10
    """), {"pid": pid}).fetchall()
    allergies = [r[0] for r in allergy_rows] or ["NKDA"]

    # ── medications ────────────────────────────────────────────────────────
    med_rows = db.execute(text("""
        SELECT medicationid, drugname, dosage, routeadmin, frequency
        FROM medication
        WHERE patientunitstayid = :pid
          AND drugname IS NOT NULL
          AND drugordercancelled != 'Yes'
        ORDER BY drugstartoffset DESC
        LIMIT 20
    """), {"pid": pid}).fetchall()
    medications = []
    for med in med_rows:
        md = _row_to_dict(med)
        medications.append({
            "id": md.get("medicationid", 0),
            "name": str(md.get("drugname", "")).strip(),
            "dosage": str(md.get("dosage") or "—"),
            "schedule": str(md.get("frequency") or md.get("routeadmin") or "—"),
            "status": "Active",
        })

    # ── infusions ──────────────────────────────────────────────────────────
    inf_rows = db.execute(text("""
        SELECT infusiondrugid, drugname, drugrate, infusionrate
        FROM infusiondrug
        WHERE patientunitstayid = :pid
          AND drugname IS NOT NULL
        ORDER BY infusionoffset DESC
        LIMIT 10
    """), {"pid": pid}).fetchall()
    infusions = []
    for inf in inf_rows:
        ifd = _row_to_dict(inf)
        rate = ifd.get("drugrate") or ifd.get("infusionrate") or "—"
        infusions.append({
            "id": ifd.get("infusiondrugid", 0),
            "name": str(ifd.get("drugname", "")).strip(),
            "rate": str(rate),
            "status": "Running",
        })

    # ── intake / output ────────────────────────────────────────────────────
    io_row = db.execute(text("""
        SELECT
            MAX(intaketotal)  AS intake_ml,
            MAX(outputtotal)  AS output_ml,
            MAX(nettotal)     AS net_ml
        FROM intakeoutput
        WHERE patientunitstayid = :pid
    """), {"pid": pid}).fetchone()
    iod = _row_to_dict(io_row)
    intake_output = [{
        "id": 1,
        "shift": "24h cumulative",
        "intake_ml": int(iod.get("intake_ml") or 0),
        "output_ml": int(iod.get("output_ml") or 0),
        "net_ml": int(iod.get("net_ml") or 0),
    }]

    # ── respiratory ────────────────────────────────────────────────────────
    resp_rows = db.execute(text("""
        SELECT respcareid, airwaytype, airwaysize, airwayposition, ventstartoffset
        FROM respiratorycare
        WHERE patientunitstayid = :pid
        ORDER BY respcarestatusoffset DESC
        LIMIT 5
    """), {"pid": pid}).fetchall()
    respiratory = []
    for i, rr in enumerate(resp_rows):
        rrd = _row_to_dict(rr)
        respiratory.append({
            "id": rrd.get("respcareid", i + 1),
            "device": str(rrd.get("airwaytype") or "Unknown"),
            "mode": str(rrd.get("airwayposition") or "—"),
            "details": f"Size {rrd.get('airwaysize') or '—'}",
        })
    if not respiratory:
        # Check respiratory charting for O2 device info
        rc = db.execute(text("""
            SELECT respchartvaluelabel, respchartvalue
            FROM respiratorycharting
            WHERE patientunitstayid = :pid
              AND respcharttypecat = 'Airway'
            ORDER BY respchartoffset DESC
            LIMIT 3
        """), {"pid": pid}).fetchall()
        for i, rr in enumerate(rc):
            rrd = _row_to_dict(rr)
            respiratory.append({
                "id": i + 1,
                "device": str(rrd.get("respchartvaluelabel") or "O2 Therapy"),
                "mode": str(rrd.get("respchartvalue") or "—"),
                "details": "—",
            })

    # ── labs ───────────────────────────────────────────────────────────────
    lab_rows = db.execute(text("""
        SELECT labid, labname, labresult, labresulttext,
               labresultoffset
        FROM lab
        WHERE patientunitstayid = :pid
          AND labname IS NOT NULL
        ORDER BY labresultoffset DESC
        LIMIT 30
    """), {"pid": pid}).fetchall()
    seen_labs: set[str] = set()
    labs = []
    CRITICAL_LABS = {
        "WBC", "Hgb", "Hct", "Platelets", "Sodium", "Potassium",
        "Creatinine", "BUN", "Glucose", "Lactate", "pH", "pO2", "pCO2",
        "Troponin", "ALT (SGPT)", "AST (SGOT)", "Total Bilirubin",
    }
    for lb in lab_rows:
        lbd = _row_to_dict(lb)
        name = str(lbd.get("labname") or "")
        if name in seen_labs:
            continue
        seen_labs.add(name)
        val = lbd.get("labresult")
        val_str = f"{val:.2f}" if isinstance(val, float) else str(lbd.get("labresulttext") or val or "—")
        labs.append({
            "id": lbd.get("labid", 0),
            "name": name,
            "value": val_str,
            "status": "High" if name in CRITICAL_LABS and val and float(str(val).replace(",", "") or 0) > 10 else "Normal",
        })

    # ── care plan ──────────────────────────────────────────────────────────
    cp_row = db.execute(text("""
        SELECT cplgoalcategory, cplgoalvalue
        FROM careplangoal
        WHERE patientunitstayid = :pid
        ORDER BY cplgoaloffset ASC
        LIMIT 5
    """), {"pid": pid}).fetchall()
    care_plan_parts = [f"{_row_to_dict(r).get('cplgoalcategory','')}: {_row_to_dict(r).get('cplgoalvalue','')}"
                       for r in cp_row if _row_to_dict(r).get("cplgoalvalue")]
    care_plan = ". ".join(care_plan_parts) or "Standard ICU care plan. Monitor vitals and adjust therapy as needed."

    # ── care providers ─────────────────────────────────────────────────────
    cp_provider_rows = db.execute(text("""
        SELECT DISTINCT providertype, specialty
        FROM careplancareProvider
        WHERE patientunitstayid = :pid
          AND providertype IS NOT NULL
        LIMIT 8
    """), {"pid": pid}).fetchall()
    care_providers = []
    for i, cp in enumerate(cp_provider_rows):
        cpd = _row_to_dict(cp)
        care_providers.append({
            "role": str(cpd.get("providertype") or "Clinician"),
            "name": _gen_name(f"{pid}-{i}", "m" if i % 2 == 0 else "f"),
        })
    if not care_providers:
        care_providers = [{"role": "Attending Physician", "name": "Dr. " + _gen_name(str(pid), "m")}]

    # ── past medical history ───────────────────────────────────────────────
    ph_rows = db.execute(text("""
        SELECT DISTINCT pasthistoryvalue
        FROM pasthistory
        WHERE patientunitstayid = :pid
          AND pasthistoryvalue IS NOT NULL
        LIMIT 10
    """), {"pid": pid}).fetchall()
    past_medical_history = [r[0] for r in ph_rows if r[0]] or ["None on record"]

    # ── clinical notes ─────────────────────────────────────────────────────
    note_rows = db.execute(text("""
        SELECT noteid, notetype, notetext
        FROM note
        WHERE patientunitstayid = :pid
          AND notetext IS NOT NULL
        ORDER BY noteoffset DESC
        LIMIT 10
    """), {"pid": pid}).fetchall()
    notes = []
    for nt in note_rows:
        ntd = _row_to_dict(nt)
        notes.append({
            "id": ntd.get("noteid", 0),
            "author": "Clinician",
            "note_type": str(ntd.get("notetype") or "Note"),
            "content": str(ntd.get("notetext") or "")[:400],
        })

    # ── treatments ─────────────────────────────────────────────────────────
    tx_rows = db.execute(text("""
        SELECT DISTINCT treatmentstring
        FROM treatment
        WHERE patientunitstayid = :pid
          AND treatmentstring IS NOT NULL
        LIMIT 12
    """), {"pid": pid}).fetchall()
    treatments = []
    for tx in tx_rows:
        s = str(tx[0])
        label = s.split("|")[-1].strip().capitalize() if "|" in s else s
        treatments.append(label)
    if not treatments:
        treatments = ["Standard ICU monitoring"]

    # ── assigned nurses ────────────────────────────────────────────────────
    nurse_rows = db.execute(text("""
        SELECT DISTINCT nursingchartcelltypecat
        FROM nursecharting
        WHERE patientunitstayid = :pid
        LIMIT 3
    """), {"pid": pid}).fetchall()
    assigned_nurses = [
        "Nurse " + _gen_name(f"{pid}-nurse-{i}", "f").split()[0]
        for i in range(min(len(nurse_rows), 2) or 1)
    ]

    # ── vitals hr trend (last 20 periodic readings) ────────────────────────
    trend_rows = db.execute(text("""
        SELECT heartrate
        FROM vitalperiodic
        WHERE patientunitstayid = :pid
          AND heartrate IS NOT NULL
        ORDER BY observationoffset DESC
        LIMIT 20
    """), {"pid": pid}).fetchall()
    hr_trend = [round(float(r[0]), 1) for r in reversed(trend_rows)]

    return {
        # Summary fields
        "id": pid,
        "display_id": pid % 10000 + 1000,
        "mrn": str(d.get("uniquepid") or f"ICU-{pid}"),
        "full_name": _gen_name(d.get("uniquepid", str(pid)), gender),
        "room": f"{d.get('unittype', 'ICU')} W{d.get('wardid', '')}",
        "primary_diagnosis": str(primary_dx)[:80],
        "age": age,
        "gender": gender,
        "clinical_status": _clinical_status(hr, spo2, apache_mort),
        "latest_hr": round(float(hr), 1),
        "latest_spo2": round(float(spo2), 1),
        # Detail fields
        "allergies": allergies,
        "medications": medications,
        "infusions": infusions,
        "intake_output": intake_output,
        "respiratory": respiratory,
        "labs": labs,
        "care_plan": care_plan,
        "care_providers": care_providers,
        "past_medical_history": past_medical_history,
        "diagnoses": diagnoses,
        "notes": notes,
        "treatments": treatments,
        "assigned_nurses": assigned_nurses,
        "vitals": {
            "heart_rate": round(float(hr), 1),
            "blood_pressure": f"{int(sys_bp)}/{int(dia_bp)}" if sys_bp and dia_bp else "—",
            "oxygen_saturation": round(float(spo2), 1),
            "temperature_c": round(float(temp), 1) if temp else 0.0,
        },
        "hr_trend": hr_trend,
        # Extra Apache data
        "apache": {
            "score": aprd.get("apachescore"),
            "predicted_icu_mortality": apache_mort,
            "predicted_icu_los": aprd.get("predictediculos"),
        },
    }
