"use client";

import { useEffect, useMemo, useRef, useState, useTransition } from "react";
import type { MedicationRecord, PatientDetail } from "@/types";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000/api";

type Props = {
  patientId: string;
  initialMedications: MedicationRecord[];
  allergies: string[];
};

async function addMedication(
  patientId: string,
  payload: { name: string; dosage?: string; schedule?: string }
): Promise<PatientDetail> {
  const res = await fetch(`${API_BASE_URL}/patients/${patientId}/medications`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const msg = await res.text();
    throw new Error(msg || "Failed to add medication");
  }
  return (await res.json()) as PatientDetail;
}

async function discontinueMedication(
  patientId: string,
  medicationId: number
): Promise<PatientDetail> {
  const res = await fetch(
    `${API_BASE_URL}/patients/${patientId}/medications/${medicationId}/discontinue`,
    {
    method: "POST",
    }
  );
  if (!res.ok) {
    const msg = await res.text();
    throw new Error(msg || "Failed to discontinue medication");
  }
  return (await res.json()) as PatientDetail;
}

function getFocusableElements(container: HTMLElement | null): HTMLElement[] {
  if (!container) return [];
  const nodes = container.querySelectorAll<HTMLElement>(
    [
      "a[href]",
      "button:not([disabled])",
      "textarea:not([disabled])",
      "input:not([disabled])",
      "select:not([disabled])",
      '[tabindex]:not([tabindex="-1"])',
    ].join(",")
  );
  return Array.from(nodes).filter((el) => !el.hasAttribute("disabled"));
}

function Modal({
  title,
  open,
  onClose,
  children,
}: {
  title: string;
  open: boolean;
  onClose: () => void;
  children: React.ReactNode;
}) {
  const dialogRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (!open) return;
    const dialog = dialogRef.current;
    const focusables = getFocusableElements(dialog);
    focusables[0]?.focus();

    function onKeyDown(e: KeyboardEvent) {
      if (e.key === "Escape") {
        e.preventDefault();
        onClose();
        return;
      }
      if (e.key !== "Tab") return;

      const items = getFocusableElements(dialog);
      if (items.length === 0) return;
      const first = items[0];
      const last = items[items.length - 1];
      const active = document.activeElement as HTMLElement | null;

      if (e.shiftKey) {
        if (!active || active === first) {
          e.preventDefault();
          last.focus();
        }
      } else {
        if (active === last) {
          e.preventDefault();
          first.focus();
        }
      }
    }

    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [open, onClose]);

  if (!open) return null;

  return (
    <div className="modal-backdrop" role="presentation" onMouseDown={onClose}>
      <div
        className="modal"
        role="dialog"
        aria-modal="true"
        aria-label={title}
        ref={dialogRef}
        onMouseDown={(e) => e.stopPropagation()}
      >
        <div className="modal-header">
          <h4 className="modal-title">{title}</h4>
          <button className="button button--secondary" onClick={onClose}>
            Close
          </button>
        </div>
        {children}
      </div>
    </div>
  );
}

export function DrugManagement({ patientId, initialMedications, allergies }: Props) {
  const [medications, setMedications] = useState<MedicationRecord[]>(
    initialMedications
  );
  const [name, setName] = useState("");
  const [dosage, setDosage] = useState("");
  const [schedule, setSchedule] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isPending, startTransition] = useTransition();
  const [addOpen, setAddOpen] = useState(false);
  const [confirmId, setConfirmId] = useState<number | null>(null);
  const [showDiscontinued, setShowDiscontinued] = useState(false);

  const conflicts = useMemo(() => {
    const al = allergies.map((a) => a.toLowerCase());
    return medications.filter((m) =>
      al.some(
        (a) =>
          m.name.toLowerCase().includes(a) ||
          a.includes(m.name.toLowerCase().split(" ")[0])
      )
    );
  }, [allergies, medications]);

  const discontinuedCount = useMemo(
    () => medications.filter((m) => m.status === "Discontinued").length,
    [medications]
  );

  const visibleMedications = useMemo(() => {
    if (showDiscontinued) return medications;
    return medications.filter((m) => m.status === "Active");
  }, [medications, showDiscontinued]);

  function onAdd() {
    setError(null);
    const trimmed = name.trim();
    if (!trimmed) {
      setError("Medication name is required.");
      return;
    }
    startTransition(async () => {
      try {
        const updated = await addMedication(patientId, {
          name: trimmed,
          dosage: dosage.trim() || undefined,
          schedule: schedule.trim() || undefined,
        });
        setMedications(updated.medications ?? []);
        setName("");
        setDosage("");
        setSchedule("");
        setAddOpen(false);
      } catch (e) {
        setError(e instanceof Error ? e.message : "Failed to add medication.");
      }
    });
  }

  function onConfirmDiscontinue() {
    if (confirmId == null) return;
    setError(null);
    startTransition(async () => {
      try {
        const updated = await discontinueMedication(patientId, confirmId);
        setMedications(updated.medications ?? []);
        setConfirmId(null);
      } catch (e) {
        setError(
          e instanceof Error ? e.message : "Failed to discontinue medication."
        );
      }
    });
  }

  return (
    <div className="card">
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          gap: 12,
          flexWrap: "wrap",
          marginBottom: 12,
        }}
      >
        <h3 className="section-title" style={{ marginBottom: 0 }}>
          Drug Management
        </h3>
        <button className="button" onClick={() => setAddOpen(true)}>
          Add medication
        </button>
      </div>

      {conflicts.length > 0 && (
        <div className="alert-box">
          <div>
            <strong style={{ color: "#b91c1c" }}>Potential allergy conflict:</strong>{" "}
            <span className="muted">
              {conflicts.map((c) => c.name).join(", ")} (allergies:{" "}
              {allergies.join(", ")})
            </span>
          </div>
        </div>
      )}

      {error && (
        <p className="form-error" role="alert">
          {error}
        </p>
      )}

      <div style={{ marginTop: 16 }}>
        <div
          style={{
            display: "flex",
            alignItems: "baseline",
            justifyContent: "space-between",
            gap: 12,
            flexWrap: "wrap",
            marginBottom: 10,
          }}
        >
          <h4 className="section-title" style={{ marginBottom: 0 }}>
            Current medications ({visibleMedications.length})
          </h4>
          {discontinuedCount > 0 && (
            <label
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: 8,
                fontWeight: 700,
                fontSize: "0.9rem",
                color: "#334155",
              }}
            >
              <input
                type="checkbox"
                checked={showDiscontinued}
                onChange={(e) => setShowDiscontinued(e.target.checked)}
              />
              Show discontinued ({discontinuedCount})
            </label>
          )}
        </div>

        {visibleMedications.length > 0 ? (
          <div className="dashboard-table-wrap">
            <table className="dashboard-table">
              <thead>
                <tr>
                  <th>Drug Name</th>
                  <th>Dosage</th>
                  <th>Schedule / Route</th>
                  <th>Status</th>
                  <th />
                </tr>
              </thead>
              <tbody>
                {visibleMedications.map((m) => (
                  <tr
                    key={m.id}
                    className={
                      m.status === "Discontinued" ? "table-row--muted" : undefined
                    }
                  >
                    <td>
                      <strong>{m.name}</strong>
                    </td>
                    <td>{m.dosage}</td>
                    <td className="muted">{m.schedule}</td>
                    <td>
                      <span
                        className={`dashboard-status ${
                          m.status === "Active" ? "dashboard-status--stable" : ""
                        }`}
                        style={{ fontSize: "0.8rem" }}
                      >
                        {m.status}
                      </span>
                    </td>
                    <td style={{ textAlign: "right" }}>
                      {m.status === "Active" ? (
                        <button
                          className="button button--secondary"
                          onClick={() => setConfirmId(m.id)}
                          disabled={isPending}
                        >
                          Discontinue
                        </button>
                      ) : (
                        <span className="muted">—</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="muted">
            {showDiscontinued
              ? "No medications on file."
              : "No active medications."}
          </p>
        )}
      </div>

      <Modal
        title="Add medication"
        open={addOpen}
        onClose={() => (isPending ? null : setAddOpen(false))}
      >
        <div className="modal-body">
          <label className="form-label">
            Medication name
            <input
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="e.g. Vancomycin"
              className="input"
            />
          </label>
          <div className="form-grid">
            <label className="form-label">
              Dosage
              <input
                value={dosage}
                onChange={(e) => setDosage(e.target.value)}
                placeholder="e.g. 1 g IV"
                className="input"
              />
            </label>
            <label className="form-label">
              Schedule / route
              <input
                value={schedule}
                onChange={(e) => setSchedule(e.target.value)}
                placeholder="e.g. q8h"
                className="input"
              />
            </label>
          </div>
        </div>
        <div className="modal-actions">
          <button
            className="button button--secondary"
            onClick={() => setAddOpen(false)}
            disabled={isPending}
          >
            Cancel
          </button>
          <button className="button" onClick={onAdd} disabled={isPending}>
            {isPending ? "Saving…" : "Save"}
          </button>
        </div>
      </Modal>

      <Modal
        title="Discontinue medication"
        open={confirmId != null}
        onClose={() => (isPending ? null : setConfirmId(null))}
      >
        <div className="modal-body">
          <p style={{ margin: 0 }}>
            Are you sure you want to discontinue this medication?
          </p>
        </div>
        <div className="modal-actions">
          <button
            className="button button--secondary"
            onClick={() => setConfirmId(null)}
            disabled={isPending}
          >
            Cancel
          </button>
          <button
            className="button button--danger"
            onClick={onConfirmDiscontinue}
            disabled={isPending}
          >
            {isPending ? "Discontinuing…" : "Discontinue"}
          </button>
        </div>
      </Modal>
    </div>
  );
}

