from collections.abc import Iterator

from app.core.config import settings
from app.schemas.patient import PatientDetail


def _build_prompt(
    patient: PatientDetail, message: str, history: list[dict[str, str]] | None = None
) -> str:
    medications = ", ".join(
        f"{med.name} ({med.dosage}, {med.schedule})" for med in patient.medications[:5]
    ) or "None listed"
    diagnoses = ", ".join(item.diagnosis for item in patient.diagnoses[:5]) or "None listed"
    allergies = ", ".join(patient.allergies[:10]) or "None listed"
    latest_note = patient.notes[-1].content if patient.notes else "No note available"
    history_lines: list[str] = []
    for turn in history or []:
        role = "User" if turn.get("role") == "user" else "Assistant"
        text = turn.get("text", "").strip()
        if text:
            history_lines.append(f"{role}: {text}")
    conversation_history = "\n".join(history_lines) if history_lines else "None"

    return f"""
You are a concise ICU clinical assistant inside a hospital dashboard.
Use only the patient data provided below. If the question requires unavailable data, say what is missing.
Do not claim certainty beyond the provided chart data. Keep answers short and practical.

Patient name: {patient.full_name}
Room: {patient.room}
Status: {patient.clinical_status}
Primary diagnosis: {patient.primary_diagnosis}
Age: {patient.age}
Gender: {patient.gender}
Vitals:
- Heart rate: {patient.vitals.heart_rate} bpm
- Blood pressure: {patient.vitals.blood_pressure}
- Oxygen saturation: {patient.vitals.oxygen_saturation}%
- Temperature: {patient.vitals.temperature_c} C
Care plan: {patient.care_plan}
Diagnoses: {diagnoses}
Medications: {medications}
Allergies: {allergies}
Assigned nurses: {", ".join(patient.assigned_nurses) or "None listed"}
Latest note: {latest_note}
Conversation history:
{conversation_history}

User question: {message}
""".strip()


def _get_gemini_client():
    if not settings.gemini_api_key:
        raise RuntimeError("Gemini is not configured. Add GEMINI_API_KEY to backend/.env.")

    try:
        from google import genai
        from google.genai import types
    except ImportError as exc:
        raise RuntimeError(
            "Gemini SDK is not installed. Run `pip install -r backend/requirements.txt`."
        ) from exc

    return genai.Client(api_key=settings.gemini_api_key), types


def run_gemini_agent(
    patient: PatientDetail, message: str, history: list[dict[str, str]] | None = None
) -> str:
    client, types = _get_gemini_client()
    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=_build_prompt(patient, message, history),
        config=types.GenerateContentConfig(
            temperature=0.2,
            max_output_tokens=400,
        ),
    )

    reply = getattr(response, "text", None)
    if not reply:
        raise RuntimeError("Gemini returned an empty response.")

    return reply.strip()


def stream_gemini_agent(
    patient: PatientDetail, message: str, history: list[dict[str, str]] | None = None
) -> Iterator[str]:
    client, types = _get_gemini_client()
    stream = client.models.generate_content_stream(
        model=settings.gemini_model,
        contents=_build_prompt(patient, message, history),
        config=types.GenerateContentConfig(
            temperature=0.2,
            max_output_tokens=400,
        ),
    )

    emitted = False
    for chunk in stream:
        text = getattr(chunk, "text", None)
        if text:
            emitted = True
            yield text

    if not emitted:
        raise RuntimeError("Gemini returned an empty response.")
