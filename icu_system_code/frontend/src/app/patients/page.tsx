import { PatientSummaryCard } from "@/components/patient-summary";
import { getPatients } from "@/services/api";

export default async function PatientsPage() {
  const patients = await getPatients();

  return (
    <main className="card">
      <h1 className="section-title">Patients</h1>
      <p className="muted">
        Starter page for doctor search and patient chart access.
      </p>
      <div className="patient-list">
        {patients.map((patient) => (
          <PatientSummaryCard key={patient.id} patient={patient} />
        ))}
      </div>
    </main>
  );
}
