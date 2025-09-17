"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";

import {
  Submission,
  SubmissionListResponse,
  SubmissionStatus,
  fetchSubmissions,
} from "@/lib/api";

const statusLabels: Record<SubmissionStatus, string> = {
  editing: "Editing",
  in_review: "In Review",
  approved: "Approved",
  needs_changes: "Needs Changes",
};

const statusOrder: SubmissionStatus[] = ["editing", "in_review", "needs_changes", "approved"];

export default function SubmissionsPage() {
  const [submissions, setSubmissions] = useState<Submission[]>([]);
  const [statusFilter, setStatusFilter] = useState<SubmissionStatus | "all">("all");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadSubmissions = async (status?: SubmissionStatus) => {
    setLoading(true);
    setError(null);
    try {
      const response: SubmissionListResponse = await fetchSubmissions(status);
      setSubmissions(response.items);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load submissions");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void loadSubmissions();
  }, []);

  useEffect(() => {
    if (statusFilter === "all") {
      void loadSubmissions();
    } else {
      void loadSubmissions(statusFilter);
    }
  }, [statusFilter]);

  const grouped = useMemo(() => {
    const map = new Map<SubmissionStatus, Submission[]>();
    for (const status of statusOrder) {
      map.set(status, []);
    }
    submissions.forEach((item) => {
      map.get(item.status)?.push(item);
    });
    return map;
  }, [submissions]);

  return (
    <div className="mx-auto flex w-full max-w-5xl flex-col gap-8 px-6 py-12">
      <header className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-3xl font-semibold text-gray-900">Submission Workspace</h1>
          <p className="text-sm text-gray-600">
            Track English source uploads, generated Thai drafts, and reviewer decisions.
          </p>
        </div>
        <Link
          href="/submissions/new"
          className="inline-flex items-center rounded bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-indigo-500"
        >
          New submission
        </Link>
      </header>

      <div className="flex flex-wrap gap-3 text-sm">
        <button
          type="button"
          onClick={() => setStatusFilter("all")}
          className={`rounded-full border px-3 py-1 ${
            statusFilter === "all"
              ? "border-indigo-500 bg-indigo-50 text-indigo-700"
              : "border-gray-200 text-gray-600 hover:border-indigo-200 hover:text-indigo-600"
          }`}
        >
          All
        </button>
        {statusOrder.map((status) => (
          <button
            key={status}
            type="button"
            onClick={() => setStatusFilter(status)}
            className={`rounded-full border px-3 py-1 ${
              statusFilter === status
                ? "border-indigo-500 bg-indigo-50 text-indigo-700"
                : "border-gray-200 text-gray-600 hover:border-indigo-200 hover:text-indigo-600"
            }`}
          >
            {statusLabels[status]}
          </button>
        ))}
      </div>

      {error && <div className="rounded border border-red-200 bg-red-50 p-4 text-sm text-red-700">{error}</div>}

      {loading ? (
        <div className="text-sm text-gray-500">Loading submissions…</div>
      ) : submissions.length === 0 ? (
        <div className="rounded border border-dashed border-gray-300 p-8 text-center text-sm text-gray-500">
          No submissions yet. Create your first draft to kick off the workflow.
        </div>
      ) : (
        <div className="grid gap-4">
          {statusOrder
            .filter((status) => statusFilter === "all" || statusFilter === status)
            .map((status) => {
              const items = grouped.get(status) ?? [];
              if (items.length === 0) return null;
              return (
                <section key={status} className="rounded-lg border border-gray-200 bg-white shadow-sm">
                  <div className="border-b border-gray-200 px-4 py-3 text-sm font-semibold text-gray-800">
                    {statusLabels[status]}
                  </div>
                  <ul className="divide-y divide-gray-100">
                    {items.map((item) => (
                      <li
                        key={item.id}
                        className="flex flex-col gap-2 px-4 py-3 md:flex-row md:items-center md:justify-between"
                      >
                        <div>
                          <p className="text-sm font-medium text-gray-900">{item.title}</p>
                          <p className="text-xs text-gray-500">
                            Tone: {item.tone ?? "default"} · Channel: {item.channel ?? "unspecified"}
                          </p>
                        </div>
                        <div className="flex items-center gap-3">
                          <p className="text-xs text-gray-500">
                            Updated {new Date(item.updated_at).toLocaleString()}
                          </p>
                          <Link
                            href={`/submissions/${item.id}`}
                            className="text-sm font-medium text-indigo-600 hover:text-indigo-500"
                          >
                            Open
                          </Link>
                        </div>
                      </li>
                    ))}
                  </ul>
                </section>
              );
            })}
        </div>
      )}
    </div>
  );
}
