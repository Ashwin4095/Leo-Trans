"use client";

import { FormEvent, useEffect, useMemo, useState } from "react";

import {
  GlossaryEntry,
  GlossaryEntryCreate,
  createGlossaryEntry,
  deleteGlossaryEntry,
  fetchGlossary,
} from "@/lib/api";

const emptyForm: GlossaryEntryCreate = {
  source_term: "",
  thai_term: "",
  part_of_speech: "",
  context: "",
  notes: "",
  is_sensitive: false,
};

export default function GlossaryAdminPage() {
  const [entries, setEntries] = useState<GlossaryEntry[]>([]);
  const [form, setForm] = useState<GlossaryEntryCreate>({ ...emptyForm });
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const filteredEntries = useMemo(() => {
    if (!search) return entries;
    const lowered = search.toLowerCase();
    return entries.filter(
      (entry) =>
        entry.source_term.toLowerCase().includes(lowered) ||
        entry.thai_term.toLowerCase().includes(lowered)
    );
  }, [entries, search]);

  const loadGlossary = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetchGlossary();
      setEntries(response.items);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load glossary");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void loadGlossary();
  }, []);

  const handleInputChange = (field: keyof GlossaryEntryCreate) =>
    (event: FormEvent<HTMLInputElement | HTMLTextAreaElement>) => {
      const target = event.target as HTMLInputElement | HTMLTextAreaElement;
      const value =
        target.type === "checkbox" ? (target as HTMLInputElement).checked : target.value;
      setForm((prev) => ({ ...prev, [field]: value }));
    };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!form.source_term.trim() || !form.thai_term.trim()) {
      setError("Source and Thai terms are required");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      await createGlossaryEntry({
        ...form,
        source_term: form.source_term.trim(),
        thai_term: form.thai_term.trim(),
        part_of_speech: form.part_of_speech?.trim() || undefined,
        context: form.context?.trim() || undefined,
        notes: form.notes?.trim() || undefined,
      });
      setForm({ ...emptyForm });
      await loadGlossary();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create entry");
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm("Remove this glossary entry?")) return;
    setLoading(true);
    setError(null);
    try {
      await deleteGlossaryEntry(id);
      await loadGlossary();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete entry");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mx-auto flex w-full max-w-5xl flex-col gap-8 p-8">
      <header className="space-y-2">
        <h1 className="text-3xl font-semibold text-gray-900">Glossary Management</h1>
        <p className="text-sm text-gray-600">
          Maintain the English → Thai terminology map. These terms are enforced during prompt
          generation to keep copy consistent.
        </p>
      </header>

      <section className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
        <form className="grid grid-cols-1 gap-4 md:grid-cols-2" onSubmit={handleSubmit}>
          <div className="flex flex-col gap-1">
            <label className="text-sm font-medium text-gray-700" htmlFor="source_term">
              English term
            </label>
            <input
              id="source_term"
              className="rounded border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none"
              value={form.source_term}
              onInput={handleInputChange("source_term")}
              placeholder="e.g. limited time"
            />
          </div>

          <div className="flex flex-col gap-1">
            <label className="text-sm font-medium text-gray-700" htmlFor="thai_term">
              Thai equivalent
            </label>
            <input
              id="thai_term"
              className="rounded border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none"
              value={form.thai_term}
              onInput={handleInputChange("thai_term")}
              placeholder="e.g. ช่วงเวลาจำกัด"
            />
          </div>

          <div className="flex flex-col gap-1">
            <label className="text-sm font-medium text-gray-700" htmlFor="part_of_speech">
              Part of speech (optional)
            </label>
            <input
              id="part_of_speech"
              className="rounded border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none"
              value={form.part_of_speech}
              onInput={handleInputChange("part_of_speech")}
              placeholder="noun, verb, phrase"
            />
          </div>

          <div className="flex flex-col gap-1 md:col-span-2">
            <label className="text-sm font-medium text-gray-700" htmlFor="context">
              Usage context
            </label>
            <textarea
              id="context"
              className="min-h-[60px] rounded border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none"
              value={form.context}
              onInput={handleInputChange("context")}
              placeholder="Where should this translation be used?"
            />
          </div>

          <div className="flex flex-col gap-1 md:col-span-2">
            <label className="text-sm font-medium text-gray-700" htmlFor="notes">
              Reviewer notes
            </label>
            <textarea
              id="notes"
              className="min-h-[60px] rounded border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none"
              value={form.notes}
              onInput={handleInputChange("notes")}
              placeholder="Additional guidance for copywriters"
            />
          </div>

          <div className="flex items-center gap-2 text-sm text-gray-700">
            <input
              id="is_sensitive"
              type="checkbox"
              checked={form.is_sensitive ?? false}
              onInput={handleInputChange("is_sensitive")}
              className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
            />
            <label htmlFor="is_sensitive">Flag as sensitive term</label>
          </div>

          <div className="md:col-span-2">
            <button
              type="submit"
              className="inline-flex items-center rounded bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:cursor-not-allowed disabled:bg-indigo-300"
              disabled={loading}
            >
              {loading ? "Saving..." : "Add term"}
            </button>
          </div>
        </form>
      </section>

      <section className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
        <div className="mb-4 flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
          <h2 className="text-lg font-semibold text-gray-900">Current glossary</h2>
          <input
            className="w-full rounded border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none md:w-64"
            placeholder="Search terms"
            value={search}
            onInput={(event) => setSearch((event.target as HTMLInputElement).value)}
          />
        </div>

        {error && <p className="mb-4 text-sm text-red-600">{error}</p>}

        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200 text-left text-sm">
            <thead className="bg-gray-50 text-xs uppercase text-gray-500">
              <tr>
                <th className="px-4 py-2">English</th>
                <th className="px-4 py-2">Thai</th>
                <th className="px-4 py-2">Context</th>
                <th className="px-4 py-2">Sensitive</th>
                <th className="px-4 py-2 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200 bg-white">
              {loading && entries.length === 0 ? (
                <tr>
                  <td className="px-4 py-3 text-center text-sm text-gray-500" colSpan={5}>
                    Loading glossary…
                  </td>
                </tr>
              ) : filteredEntries.length === 0 ? (
                <tr>
                  <td className="px-4 py-3 text-center text-sm text-gray-500" colSpan={5}>
                    No terms yet. Add your first entry above.
                  </td>
                </tr>
              ) : (
                filteredEntries.map((entry) => (
                  <tr key={entry.id}>
                    <td className="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
                      {entry.source_term}
                    </td>
                    <td className="whitespace-nowrap px-4 py-2 text-gray-700">
                      {entry.thai_term}
                    </td>
                    <td className="px-4 py-2 text-gray-500">
                      {entry.context ?? "—"}
                    </td>
                    <td className="px-4 py-2 text-gray-500">
                      {entry.is_sensitive ? "Yes" : "No"}
                    </td>
                    <td className="px-4 py-2 text-right">
                      <button
                        className="text-sm font-medium text-red-600 hover:text-red-500"
                        onClick={() => void handleDelete(entry.id)}
                        disabled={loading}
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
