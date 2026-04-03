import Link from "next/link";

import { getPatients } from "@/services/api";

type SearchParams = { q?: string };

export default async function DashboardPage({
  searchParams,
}: {
  searchParams: SearchParams;
}) {
  const q = searchParams.q?.trim() || undefined;
  const patients = await getPatients(q);

  const total = patients.length;
  const critical = patients.filter((p) => p.clinical_status === "Critical").length;
  const stable = patients.filter((p) => p.clinical_status === "Stable").length;

  return (
    <main className="dashboard-main">
      <form className="dashboard-search" action="/dashboard" method="get">
        <input
          type="search"
          name="q"
          className="dashboard-search-input"
          placeholder="Search patient ID, name, or diagnosis"
          defaultValue={q ?? ""}
          aria-label="Search patients"
        />
        <button type="submit" className="dashboard-search-btn">
          Search
        </button>
        {q ? (
          <Link href="/dashboard" className="dashboard-search-reset">
            Show all
          </Link>
        ) : null}
      </form>

      <div className="dashboard-stats">
        <div className="dashboard-stat-card">
          <div className="dashboard-stat-label">Total Patients</div>
          <div className="dashboard-stat-value">{total}</div>
        </div>
        <div className="dashboard-stat-card">
          <div className="dashboard-stat-label">Critical</div>
          <div className="dashboard-stat-value">{critical}</div>
        </div>
        <div className="dashboard-stat-card">
          <div className="dashboard-stat-label">Stable</div>
          <div className="dashboard-stat-value">{stable}</div>
        </div>
      </div>

      <div className="dashboard-table-wrap">
        <table className="dashboard-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Age</th>
              <th>Gender</th>
              <th>Status</th>
              <th>Latest HR</th>
              <th>Latest SpO₂</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {patients.map((patient) => (
              <tr key={patient.id}>
                <td>{patient.display_id}</td>
                <td>{patient.full_name}</td>
                <td>{patient.age}</td>
                <td>{patient.gender}</td>
                <td>
                  <span
                    className={
                      patient.clinical_status === "Critical"
                        ? "dashboard-status dashboard-status--critical"
                        : "dashboard-status dashboard-status--stable"
                    }
                  >
                    {patient.clinical_status}
                  </span>
                </td>
                <td>{patient.latest_hr.toFixed(1)}</td>
                <td>{patient.latest_spo2.toFixed(1)}</td>
                <td>
                  <Link
                    href={`/patients/${patient.id}`}
                    className="dashboard-link"
                  >
                    View
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </main>
  );
}
