#!/usr/bin/env python3
"""Import eICU hospital CSV/CSV.GZ into PostgreSQL/Supabase.

Usage:
  .venv/bin/python scripts/import_hospital_csv.py \
    "../../eicu-collaborative-research-database-demo-2.0.1/hospital.csv.gz"

Notes:
  - Reads DATABASE_URL from backend/.env via app.core.config.settings
  - Expects the target table `hospital` to already exist
"""

from __future__ import annotations

import argparse
import gzip
from pathlib import Path
import sys
from typing import TextIO

import psycopg

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.core.config import settings


COPY_SQL = """
COPY hospital (
    hospitalid,
    numbedscategory,
    teachingstatus,
    region
)
FROM STDIN WITH (FORMAT csv, HEADER true)
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Import eICU hospital CSV/CSV.GZ into PostgreSQL/Supabase."
    )
    parser.add_argument(
        "csv_path",
        help="Path to hospital.csv or hospital.csv.gz",
    )
    parser.add_argument(
        "--database-url",
        default=settings.database_url,
        help="Override DATABASE_URL from backend/.env",
    )
    parser.add_argument(
        "--truncate",
        action="store_true",
        help="TRUNCATE hospital before import",
    )
    return parser.parse_args()


def open_input(path: Path) -> TextIO:
    if path.suffix == ".gz":
        return gzip.open(path, mode="rt", encoding="utf-8", newline="")
    return path.open(mode="rt", encoding="utf-8", newline="")


def main() -> int:
    args = parse_args()

    if not args.database_url:
        raise SystemExit(
            "DATABASE_URL is not set. Add it to backend/.env or pass --database-url."
        )

    csv_path = Path(args.csv_path).expanduser().resolve()
    if not csv_path.exists():
        raise SystemExit(f"Input file not found: {csv_path}")

    print(f"Importing {csv_path} -> hospital")

    try:
        with psycopg.connect(args.database_url) as conn:
            with conn.cursor() as cur:
                if args.truncate:
                    print("Truncating hospital table first...")
                    cur.execute("TRUNCATE TABLE hospital RESTART IDENTITY CASCADE")

                with open_input(csv_path) as src, cur.copy(COPY_SQL) as copy:
                    while chunk := src.read(1024 * 1024):
                        copy.write(chunk)

            conn.commit()
    except psycopg.Error as exc:
        raise SystemExit(
            "Import failed.\n"
            f"PostgreSQL error: {exc}"
        ) from exc

    print("Import complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
