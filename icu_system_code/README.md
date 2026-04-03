# ICU System Starter

Starter monorepo for an ICU information system built with `FastAPI` and `Next.js`.

## Included

- Doctor login starter flow
- Patient search and detail views
- Diagnoses, notes, treatments, and nurse assignment API stubs
- Medication management API stubs
- Real-time monitoring starter endpoint design
- Mock backend data so the app can run before a database is added

## Structure

```text
icu-system/
  backend/
  frontend/
  docker-compose.yml
```

## Run Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend runs at `http://127.0.0.1:8000`.

## Run Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://127.0.0.1:3000`.
This starter is pinned to a `Next.js` version that works with Node `18.20.8`.

## Next Steps

1. Replace mock services with a PostgreSQL database layer.
2. Add JWT auth and password hashing persistence.
3. Add WebSocket streaming for live bedside monitor data.
4. Add audit logging and role-based permissions.
