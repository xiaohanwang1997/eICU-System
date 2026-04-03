from fastapi import APIRouter

from app.api.routes import agent, assignments, auth, diagnoses, medications, monitoring, notes, patients

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(agent.router)
api_router.include_router(patients.router)
api_router.include_router(diagnoses.router)
api_router.include_router(notes.router)
api_router.include_router(assignments.router)
api_router.include_router(medications.router)
api_router.include_router(monitoring.router)
