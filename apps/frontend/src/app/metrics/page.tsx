"use client";

import { useEffect, useState } from "react";

import { MetricsOverview, fetchMetricsOverview } from "@/lib/api";

const statusLabels: Record<string, string> = {
  editing: "Editing",
  in_review: "In Review",
  approved: "Approved",
  needs_changes: "Needs Changes",
};

export default function MetricsPage() {
  const [metrics, setMetrics] = useState<MetricsOverview | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [days, setDays] = useState<number | undefined>();

  const loadMetrics = async (window?: number) => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchMetricsOverview(window);
      setMetrics(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load metrics");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void loadMetrics();
  }, []);

  return (
    <div className="mx-auto flex w-full max-w-5xl flex-col gap-8 px-6 py-12">
      <header className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
        <div>
          <p className="text-xs font-semibold uppercase tracking-wide text-indigo-600">Analytics</p>
          <h1 className="text-3xl font-semibold text-gray-900">Quality & Throughput Metrics</h1>
          <p className="text-sm text-gray-600">
            Track submission volume, reviewer approval rate, and token usage to monitor production
            health.
          </p>
        </div>
        <div className="flex gap-2 text-sm">
          {[undefined, 7, 30].map((window) => {
            const label = window ? `${window}d` : "All time";
            const isActive = days === window || (!days && window === undefined);
            return (
              <button
                key={label}
                type="button"
                onClick={() => {
                  setDays(window);
                  void loadMetrics(window);
                }}
                className={`rounded-full border px-3 py-1 ${
                  isActive
                    ? "border-indigo-500 bg-indigo-50 text-indigo-700"
                    : "border-gray-200 text-gray-600 hover:border-indigo-200 hover:text-indigo-600"
                }`}
              >
                {label}
              </button>
            );
          })}
        </div>
      </header>

      {error && <div className="rounded border border-red-200 bg-red-50 p-4 text-sm text-red-700">{error}</div>}
      {loading && <div className="text-sm text-gray-500">Loading metrics…</div>}

      {metrics && (
        <div className="grid gap-6 md:grid-cols-3">
          <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
            <p className="text-xs uppercase text-gray-500">Total submissions</p>
            <p className="mt-2 text-3xl font-semibold text-gray-900">{metrics.total_submissions}</p>
          </div>
          <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
            <p className="text-xs uppercase text-gray-500">Approval rate</p>
            <p className="mt-2 text-3xl font-semibold text-gray-900">
              {(metrics.approval_rate * 100).toFixed(1)}%
            </p>
          </div>
          <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
            <p className="text-xs uppercase text-gray-500">Submissions with warnings</p>
            <p className="mt-2 text-3xl font-semibold text-gray-900">
              {metrics.submissions_with_warnings}
            </p>
          </div>

          <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm md:col-span-2">
            <p className="text-xs uppercase text-gray-500">Status distribution</p>
            <ul className="mt-3 space-y-2 text-sm text-gray-700">
              {Object.entries(metrics.submissions_by_status).map(([status, count]) => (
                <li key={status} className="flex items-center justify-between">
                  <span>{statusLabels[status] ?? status}</span>
                  <span className="font-medium">{count}</span>
                </li>
              ))}
            </ul>
          </div>

          <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
            <p className="text-xs uppercase text-gray-500">Token usage</p>
            <p className="mt-2 text-2xl font-semibold text-gray-900">
              {metrics.total_tokens.toLocaleString()}
            </p>
            <p className="text-xs text-gray-500">
              Avg / submission: {metrics.average_tokens ? metrics.average_tokens.toFixed(1) : "–"}
            </p>
          </div>

          <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
            <p className="text-xs uppercase text-gray-500">Estimated spend</p>
            <p className="mt-2 text-2xl font-semibold text-gray-900">
              ${metrics.total_cost_usd.toFixed(2)}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
