import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Cloud-friendly default: allow overriding with DATABASE_URL.
# Examples:
# - sqlite:////data/eicu.db (persistent volume)
# - sqlite:////app/backend/eicu.db (bundled in image)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///eicu.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
