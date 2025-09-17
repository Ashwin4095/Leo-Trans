"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { useParams } from "next/navigation";

import {
  Submission,
  SubmissionStatus,
  SubmissionUpdate,
  exportSubmission,
  fetchSubmission,
  updateSubmission,
} from "@/lib/api";

const statusOptions: { value: SubmissionStatus; label: string }[] = [
  { value: "editing", label: "Editing" },
  { value: "in_review", label: "In Review" },
  { value: "needs_changes", label: "Needs Changes" },
  { value: "approved", label: "Approved" },
];

export default function SubmissionDetailPage() {
  const params = useParams<{ id: string }>();
  const submissionId = params?.id;
  const [submission, setSubmission] = useState<Submission | null>(null);
  const [editorText, setEditorText] = useState("");
  const [status, setStatus] = useState<SubmissionStatus>("editing");
  const [reviewerNotes, setReviewerNotes] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);
  const [saveResult, setSaveResult] = useState<string | null>(null);
  const [exporting, setExporting] = useState<"csv" | "docx" | "social" | null>(null);

  useEffect(() => {
    if (!submissionId) return;
    const load = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await fetchSubmission(submissionId);
        setSubmission(data);
        setEditorText(data.thai_final ?? "");
        setStatus(data.status);
        setReviewerNotes(data.reviewer_notes ?? "");
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load submission");
      } finally {
        setLoading(false);
      }
    };
    void load();
  }, [submissionId]);

  const warnings = useMemo(() => submission?.warnings ?? [], [submission]);

  const handleSave = async () => {
    if (!submissionId) return;
    setSaving(true);
    setSaveResult(null);
    try {
      const payload: SubmissionUpdate = {
        thai_final: editorText.trim() || undefined,
        status,
        reviewer_notes: reviewerNotes.trim() || undefined,
      };
      const updated = await updateSubmission(submissionId, payload);
      setSubmission(updated);
      setSaveResult("Changes saved");
    } catch (err) {
      setSaveResult(err instanceof Error ? err.message : "Failed to save submission");
    } finally {
      setSaving(false);
    }
  };

  const handleExport = async (format: "csv" | "docx" | "social") => {
    if (!submissionId) return;
    setExporting(format);
    try {
      await exportSubmission(submissionId, format);
    } catch (err) {
      setSaveResult(err instanceof Error ? err.message : "Export failed");
    } finally {
      setExporting(null);
    }
  };

  if (loading) {
    return <div className="p-6 text-sm text-gray-500">Loading submission…</div>;
  }

  if (error) {
    return (
      <div className="p-6 text-sm text-red-600">
        {error} · <Link href="/submissions" className="underline">Return to list</Link>
      </div>
    );
  }

  if (!submission) {
    return null;
  }

  return (
    <div className="mx-auto flex w-full max-w-5xl flex-col gap-10 px-6 py-12">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs font-medium uppercase tracking-wide text-indigo-600">Submission</p>
          <h1 className="text-3xl font-semibold text-gray-900">{submission.title}</h1>
        </div>
        <Link href="/submissions" className="text-sm font-medium text-indigo-600 hover:text-indigo-500">
          Back to submissions
        </Link>
      </div>

      <section className="grid gap-6 md:grid-cols-[1.1fr_0.9fr]">
        <article className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
          <h2 className="text-sm font-semibold uppercase tracking-wide text-gray-500">English Source</h2>
          <p className="mt-3 whitespace-pre-line text-sm text-gray-700">{submission.source_text}</p>

          <div className="mt-6 border-t border-gray-100 pt-4">
            <h3 className="text-sm font-semibold uppercase tracking-wide text-gray-500">Generated draft</h3>
            <pre className="mt-2 max-h-64 overflow-auto rounded bg-gray-50 p-3 text-xs leading-relaxed text-gray-700">
{submission.thai_draft}
            </pre>
          </div>

          {submission.translation_prompt && (
            <details className="mt-4 rounded border border-gray-200 bg-gray-50 p-3 text-xs text-gray-600">
              <summary className="cursor-pointer text-sm font-medium text-gray-700">Prompt details</summary>
              <pre className="mt-2 whitespace-pre-wrap text-xs">{submission.translation_prompt}</pre>
            </details>
          )}
        </article>

        <aside className="flex flex-col gap-6">
          <section className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
            <h2 className="text-base font-semibold text-gray-900">Editor workspace</h2>
            <textarea
              className="mt-3 min-h-[200px] w-full rounded border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none"
              value={editorText}
              onInput={(event) => setEditorText((event.target as HTMLTextAreaElement).value)}
              placeholder="Refine the Thai copy here"
            />
            <label className="mt-4 block text-sm font-medium text-gray-700" htmlFor="status">
              Workflow status
            </label>
            <select
              id="status"
              className="mt-1 w-full rounded border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none"
              value={status}
              onChange={(event) => setStatus(event.target.value as SubmissionStatus)}
            >
              {statusOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>

            <label className="mt-4 block text-sm font-medium text-gray-700" htmlFor="reviewer_notes">
              Reviewer notes
            </label>
            <textarea
              id="reviewer_notes"
              className="mt-1 min-h-[100px] w-full rounded border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none"
              value={reviewerNotes}
              onInput={(event) => setReviewerNotes((event.target as HTMLTextAreaElement).value)}
              placeholder="Leave review feedback or context"
            />

            <button
              type="button"
              onClick={handleSave}
              className="mt-4 inline-flex items-center rounded bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-indigo-500 disabled:cursor-not-allowed disabled:bg-indigo-300"
              disabled={saving}
            >
              {saving ? "Saving…" : "Save changes"}
            </button>
            {saveResult && <p className="mt-2 text-xs text-gray-500">{saveResult}</p>}
          </section>

          <section className="rounded-lg border border-amber-200 bg-amber-50 p-6 text-sm text-amber-800">
            <h2 className="text-sm font-semibold uppercase tracking-wide">Warnings</h2>
            {warnings.length === 0 ? (
              <p className="mt-2 text-sm">No warnings triggered.</p>
            ) : (
              <ul className="mt-2 list-disc space-y-1 pl-4">
                {warnings.map((warning) => (
                  <li key={warning}>{warning}</li>
                ))}
              </ul>
            )}
          </section>

          <section className="rounded-lg border border-gray-200 bg-white p-6 text-xs text-gray-600 shadow-sm">
            <dl className="space-y-2">
              <div className="flex items-center justify-between">
                <dt className="font-medium text-gray-700">Provider</dt>
                <dd>{submission.provider_name ?? "placeholder"}</dd>
              </div>
              <div className="flex items-center justify-between">
                <dt className="font-medium text-gray-700">Usage tokens</dt>
                <dd>{submission.usage_tokens ?? "–"}</dd>
              </div>
              <div className="flex items-center justify-between">
                <dt className="font-medium text-gray-700">Estimated cost</dt>
                <dd>{submission.cost_usd ? `$${submission.cost_usd.toFixed(4)}` : "–"}</dd>
              </div>
              <div className="flex items-center justify-between">
                <dt className="font-medium text-gray-700">Glossary terms</dt>
                <dd>{submission.glossary_terms.length ? submission.glossary_terms.join(", ") : "–"}</dd>
              </div>
              <div className="flex items-center justify-between">
                <dt className="font-medium text-gray-700">Updated</dt>
                <dd>{new Date(submission.updated_at).toLocaleString()}</dd>
              </div>
            </dl>
            <div className="mt-4 flex flex-wrap gap-2">
              {(["csv", "docx", "social"] as const).map((format) => (
                <button
                  key={format}
                  type="button"
                  onClick={() => void handleExport(format)}
                  className="rounded border border-gray-300 px-3 py-1 text-xs font-medium text-gray-700 hover:border-indigo-300 hover:text-indigo-600"
                  disabled={exporting !== null}
                >
                  {exporting === format ? "Exporting…" : `Export ${format.toUpperCase()}`}
                </button>
              ))}
            </div>
          </section>
        </aside>
      </section>
    </div>
  );
}
