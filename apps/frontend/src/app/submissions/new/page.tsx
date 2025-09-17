"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

import { SubmissionCreate, createSubmission } from "@/lib/api";

const initialForm: SubmissionCreate = {
  title: "",
  source_text: "",
  tone: "",
  audience: "",
  channel: "",
};

export default function NewSubmissionPage() {
  const router = useRouter();
  const [form, setForm] = useState<SubmissionCreate>({ ...initialForm });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (field: keyof SubmissionCreate) =>
    (event: FormEvent<HTMLInputElement | HTMLTextAreaElement>) => {
      const value = (event.target as HTMLInputElement | HTMLTextAreaElement).value;
      setForm((prev) => ({ ...prev, [field]: value }));
    };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!form.title.trim() || !form.source_text.trim()) {
      setError("Title and source content are required");
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const submission = await createSubmission({
        ...form,
        title: form.title.trim(),
        source_text: form.source_text.trim(),
        tone: form.tone?.trim() || undefined,
        audience: form.audience?.trim() || undefined,
        channel: form.channel?.trim() || undefined,
      });
      router.push(`/submissions/${submission.id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create submission");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mx-auto flex w-full max-w-4xl flex-col gap-8 px-6 py-12">
      <header className="space-y-2">
        <h1 className="text-3xl font-semibold text-gray-900">New Submission</h1>
        <p className="text-sm text-gray-600">
          Paste English source content. The system will generate a Thai draft with glossary guidance
          so editors can refine before review.
        </p>
      </header>

      <form className="space-y-6" onSubmit={handleSubmit}>
        <div className="flex flex-col gap-1">
          <label className="text-sm font-medium text-gray-700" htmlFor="title">
            Title
          </label>
          <input
            id="title"
            className="rounded border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none"
            value={form.title}
            onInput={handleChange("title")}
            placeholder="Campaign headline or reference"
          />
        </div>

        <div className="grid gap-4 md:grid-cols-3">
          <div className="flex flex-col gap-1">
            <label className="text-sm font-medium text-gray-700" htmlFor="tone">
              Tone (optional)
            </label>
            <input
              id="tone"
              className="rounded border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none"
              value={form.tone}
              onInput={handleChange("tone")}
              placeholder="e.g. energetic"
            />
          </div>
          <div className="flex flex-col gap-1">
            <label className="text-sm font-medium text-gray-700" htmlFor="audience">
              Audience (optional)
            </label>
            <input
              id="audience"
              className="rounded border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none"
              value={form.audience}
              onInput={handleChange("audience")}
              placeholder="e.g. Millennial shoppers"
            />
          </div>
          <div className="flex flex-col gap-1">
            <label className="text-sm font-medium text-gray-700" htmlFor="channel">
              Channel (optional)
            </label>
            <input
              id="channel"
              className="rounded border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none"
              value={form.channel}
              onInput={handleChange("channel")}
              placeholder="e.g. social"
            />
          </div>
        </div>

        <div className="flex flex-col gap-1">
          <label className="text-sm font-medium text-gray-700" htmlFor="source_text">
            English source content
          </label>
          <textarea
            id="source_text"
            className="min-h-[220px] rounded border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none"
            value={form.source_text}
            onInput={handleChange("source_text")}
            placeholder="Paste the copy that needs Thai localization"
          />
        </div>

        {error && <p className="text-sm text-red-600">{error}</p>}

        <div className="flex gap-3">
          <button
            type="submit"
            className="inline-flex items-center rounded bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-indigo-500 disabled:cursor-not-allowed disabled:bg-indigo-300"
            disabled={loading}
          >
            {loading ? "Generating draft…" : "Create submission"}
          </button>
        </div>
      </form>
    </div>
  );
}
