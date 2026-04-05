import { getPatient } from "@/services/api";
import { PatientPageShell } from "@/components/patient-page-shell";

const NOTE_TYPE_COLOR: Record<string, { bg: string; color: string }> = {
  "Progress Note": { bg: "#eff6ff", color: "#1d4ed8" },
  "Nursing Note": { bg: "#f0fdf4", color: "#166534" },
  "Admission Note": { bg: "#fdf4ff", color: "#7e22ce" },
  "Discharge Note": { bg: "#fff7ed", color: "#9a3412" },
  "Consult": { bg: "#f0f9ff", color: "#0369a1" },
};

function noteStyle(type: string) {
  return NOTE_TYPE_COLOR[type] ?? { bg: "#f8fafc", color: "#334155" };
}

export default async function NotesPage({ params }: { params: { id: string } }) {
  const patient = await getPatient(params.id);
  const notes = patient.notes ?? [];

  const byType: Record<string, typeof notes> = {};
  for (const note of notes) {
    const t = note.note_type ?? "Other";
    if (!byType[t]) byType[t] = [];
    byType[t].push(note);
  }

  const types = Object.keys(byType);

  return (
    <PatientPageShell patientId={params.id} title={patient.full_name} subtitle="Clinical Notes & Documentation">

      {/* Note type summary */}
      <div style={{ display: "flex", flexWrap: "wrap", gap: 10 }}>
        {types.map((t) => {
          const s = noteStyle(t);
          return (
            <div key={t} style={{ padding: "8px 16px", borderRadius: 8, background: s.bg, color: s.color, fontWeight: 600, fontSize: "0.875rem" }}>
              {t} ({byType[t].length})
            </div>
          );
        })}
        {notes.length === 0 && <p className="muted">No notes on record.</p>}
      </div>

      {/* Notes by type */}
      {types.map((t) => (
        <div key={t} className="card">
          <h3 className="section-title" style={{ color: noteStyle(t).color }}>{t}</h3>
          <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
            {byType[t].map((note) => (
              <div key={note.id} style={{ padding: "14px 16px", borderRadius: 10, background: noteStyle(note.note_type).bg, border: `1px solid ${noteStyle(note.note_type).bg}` }}>
                <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 8, flexWrap: "wrap", gap: 8 }}>
                  <span style={{ fontWeight: 700, color: "#0f172a" }}>{note.author}</span>
                  <span style={{ fontSize: "0.8rem", fontWeight: 600, padding: "2px 10px", borderRadius: 999, background: "rgba(255,255,255,0.7)", color: noteStyle(note.note_type).color }}>
                    {note.note_type}
                  </span>
                </div>
                <p style={{ margin: 0, color: "#334155", lineHeight: 1.6, fontSize: "0.925rem" }}>{note.content}</p>
              </div>
            ))}
          </div>
        </div>
      ))}

      {notes.length === 0 && (
        <div className="card">
          <p className="muted" style={{ margin: 0 }}>No clinical notes recorded for this patient encounter.</p>
        </div>
      )}

      <div className="card">
        <p className="muted" style={{ margin: 0, fontSize: "0.875rem" }}>
          Data from <strong>note</strong> (24,758 rows) and <strong>physicalExam</strong> (84,058 rows).
          In production, this page includes keyword search, NLP summarization, and timeline view.
        </p>
      </div>

    </PatientPageShell>
  );
}
