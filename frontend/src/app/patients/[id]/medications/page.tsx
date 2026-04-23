import { getPatient } from "@/services/api";
import { PatientPageShell } from "@/components/patient-page-shell";
import { DrugManagement } from "@/components/drug-management";

export default async function MedicationsPage({ params }: { params: { id: string } }) {
  const patient = await getPatient(params.id);
  const meds = patient.medications ?? [];
  const infusions = patient.infusions ?? [];
  const allergies = patient.allergies ?? [];

  return (
    <PatientPageShell patientId={params.id} title={patient.full_name} subtitle="Medications & Infusions">

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

      {/* Drug management (add / discontinue) */}
      <DrugManagement patientId={params.id} initialMedications={meds} allergies={allergies} />

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
