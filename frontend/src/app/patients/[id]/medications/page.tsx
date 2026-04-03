import { getPatient } from "@/services/api";
import { PatientPageShell } from "@/components/patient-page-shell";

export default async function MedicationsPage({ params }: { params: { id: string } }) {
  const patient = await getPatient(params.id);
  const meds = patient.medications ?? [];
  const infusions = patient.infusions ?? [];
  const allergies = patient.allergies ?? [];

  // Detect allergy conflicts
  const conflicts = meds.filter((m) =>
    allergies.some((a) => m.name.toLowerCase().includes(a.toLowerCase()) || a.toLowerCase().includes(m.name.toLowerCase().split(" ")[0]))
  );

  return (
    <PatientPageShell patientId={params.id} title={patient.full_name} subtitle="Medications & Infusions">

      {/* Allergy warning */}
      {conflicts.length > 0 && (
        <div className="alert-box" style={{ borderColor: "#fca5a5", background: "#fff7f7" }}>
          <span style={{ fontSize: "1.3rem" }}>🚨</span>
          <div>
            <strong style={{ color: "#b91c1c" }}>Potential allergy conflict:</strong>{" "}
            <span className="muted">{conflicts.map((c) => c.name).join(", ")} — check against allergy list ({allergies.join(", ")})</span>
          </div>
        </div>
      )}

      {/* Allergy list */}
      <div className="card">
        <h3 className="section-title">Known Allergies</h3>
        <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
          {allergies.map((a) => (
            <span key={a} style={{ padding: "4px 12px", background: "#fee2e2", color: "#991b1b", borderRadius: 999, fontSize: "0.875rem", fontWeight: 600 }}>
              ⚠ {a}
            </span>
          ))}
        </div>
      </div>

      {/* Medication orders */}
      <div className="card">
        <h3 className="section-title">Medication Orders ({meds.length})</h3>
        {meds.length > 0 ? (
          <div className="dashboard-table-wrap">
            <table className="dashboard-table">
              <thead>
                <tr>
                  <th>Drug Name</th>
                  <th>Dosage</th>
                  <th>Schedule / Route</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {meds.map((m) => (
                  <tr key={m.id}>
                    <td><strong>{m.name}</strong></td>
                    <td>{m.dosage}</td>
                    <td className="muted">{m.schedule}</td>
                    <td>
                      <span className={`dashboard-status ${m.status === "Active" ? "dashboard-status--stable" : ""}`} style={{ fontSize: "0.8rem" }}>
                        {m.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="muted">No medication orders on file.</p>
        )}
      </div>

      {/* Infusion drugs */}
      <div className="card">
        <h3 className="section-title">Active Infusions ({infusions.length})</h3>
        {infusions.length > 0 ? (
          <div className="dashboard-table-wrap">
            <table className="dashboard-table">
              <thead>
                <tr>
                  <th>Drug</th>
                  <th>Rate</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {infusions.map((inf) => (
                  <tr key={inf.id}>
                    <td><strong>{inf.name}</strong></td>
                    <td>{inf.rate}</td>
                    <td>
                      <span style={{ padding: "3px 10px", borderRadius: 999, fontSize: "0.8rem", fontWeight: 700, background: inf.status === "Running" ? "#dcfce7" : "#fef9c3", color: inf.status === "Running" ? "#166534" : "#92400e" }}>
                        {inf.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="muted">No active infusions.</p>
        )}
      </div>

      {/* Past medical history context */}
      <div className="card">
        <h3 className="section-title">Past Medical History (context for prescribing)</h3>
        <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
          {(patient.past_medical_history ?? []).map((h) => (
            <span key={h} className="badge">{h}</span>
          ))}
        </div>
      </div>

    </PatientPageShell>
  );
}
