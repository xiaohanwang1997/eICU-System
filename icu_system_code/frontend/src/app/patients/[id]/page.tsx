import { PatientDetailTabs } from "@/components/patient-detail-tabs";
import { buildHeartRateTrend } from "@/lib/vitals-trend";
import { getPatient } from "@/services/api";

export default async function PatientDetailPage({
  params,
}: {
  params: { id: string };
}) {
  const patient = await getPatient(params.id);
  const hrTrend = buildHeartRateTrend(patient.vitals.heart_rate, patient.id);

  return (
    <main className="patient-detail-page">
      <PatientDetailTabs patient={patient} hrTrend={hrTrend} />
    </main>
  );
}
