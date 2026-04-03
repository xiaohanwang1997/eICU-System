"""
Load all 31 eICU CSV.GZ files into eicu.db (SQLite).
Run once from the project root:
    python load_data.py
Place all *_csv.gz files inside  data/  before running.
"""

import sys
import pandas as pd
from sqlalchemy import create_engine, text

DATA_DIR = "data"
DB_PATH = "eicu.db"

engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)

TABLES = [
    # (csv_stem, table_name)
    ("admissiondrug_csv",              "admissiondrug"),
    ("admissionDx_csv",                "admissiondx"),
    ("allergy_csv",                    "allergy"),
    ("apacheApsVar_csv",               "apacheapsvar"),
    ("apachePatientResult_csv",        "apachepatientresult"),
    ("apachePredVar_csv",              "apachepredvar"),
    ("carePlanCareProvider_csv",       "careplancareProvider"),
    ("carePlanEOL_csv",                "careplaneol"),
    ("carePlanGeneral_csv",            "careplangeneral"),
    ("carePlanGoal_csv",               "careplangoal"),
    ("carePlanInfectiousDisease_csv",  "careplaninfectiousdisease"),
    ("customLab_csv",                  "customlab"),
    ("diagnosis_csv",                  "diagnosis"),
    ("hospital_csv",                   "hospital"),
    ("infusiondrug_csv",               "infusiondrug"),
    ("intakeOutput_csv",               "intakeoutput"),
    ("lab_csv",                        "lab"),
    ("medication_csv",                 "medication"),
    ("microLab_csv",                   "microlab"),
    ("note_csv",                       "note"),
    ("nurseAssessment_csv",            "nurseassessment"),
    ("nurseCare_csv",                  "nursecare"),
    ("nurseCharting_csv",              "nursecharting"),
    ("pastHistory_csv",                "pasthistory"),
    ("patient_csv",                    "patient"),
    ("physicalExam_csv",               "physicalexam"),
    ("respiratoryCare_csv",            "respiratorycare"),
    ("respiratoryCharting_csv",        "respiratorycharting"),
    ("treatment_csv",                  "treatment"),
    ("vitalAperiodic_csv",             "vitalaperiodic"),
    ("vitalPeriodic_csv",              "vitalperiodic"),
]


def load_table(csv_stem: str, table_name: str) -> None:
    path = f"{DATA_DIR}/{csv_stem.replace('_csv', '.csv')}.gz"
    try:
        df = pd.read_csv(path, compression="gzip", low_memory=False)
        df.columns = [c.lower() for c in df.columns]
        df.to_sql(table_name, engine, if_exists="replace", index=False,
                  chunksize=50_000)
        print(f"  ✓ {table_name:35s} {len(df):>8,} rows")
    except FileNotFoundError:
        print(f"  ✗ {table_name:35s} FILE NOT FOUND – skipped", file=sys.stderr)
    except Exception as exc:
        print(f"  ✗ {table_name:35s} ERROR: {exc}", file=sys.stderr)


def create_indexes() -> None:
    """Add patientunitstayid indexes for fast per-patient lookups."""
    indexed = [
        "admissiondrug", "admissiondx", "allergy", "apacheapsvar",
        "apachepatientresult", "apachepredvar", "careplancareProvider",
        "careplangeneral", "careplangoal", "careplaninfectiousdisease",
        "diagnosis", "infusiondrug", "intakeoutput", "lab",
        "medication", "microlab", "note", "nurseassessment",
        "nursecare", "nursecharting", "pasthistory", "physicalexam",
        "respiratorycare", "respiratorycharting", "treatment",
        "vitalaperiodic", "vitalperiodic",
    ]
    with engine.connect() as conn:
        for tbl in indexed:
            try:
                conn.execute(
                    text(
                        f"CREATE INDEX IF NOT EXISTS idx_{tbl}_pid "
                        f"ON {tbl} (patientunitstayid)"
                    )
                )
            except Exception:
                pass
        conn.commit()
    print("  ✓ indexes created")


if __name__ == "__main__":
    print(f"Loading eICU tables into {DB_PATH} …\n")
    for stem, tbl in TABLES:
        load_table(stem, tbl)
    print("\nCreating indexes …")
    create_indexes()
    print("\nDone.")
