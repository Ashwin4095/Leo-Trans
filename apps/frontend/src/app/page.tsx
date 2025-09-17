import Link from "next/link";

export default function Home() {
  return (
    <div className="mx-auto flex min-h-screen w-full max-w-5xl flex-col gap-12 px-6 py-16">
      <header className="space-y-3">
        <p className="text-sm font-semibold uppercase tracking-wide text-indigo-600">
          Leo Localization Platform
        </p>
        <h1 className="text-4xl font-bold text-gray-900">
          Human-in-the-loop Thai copy adaptation built for marketing teams.
        </h1>
        <p className="max-w-3xl text-base text-gray-600">
          Submit English source content, generate culturally aware Thai drafts, and shepherd
          feedback between editors and reviewers. Follow the implementation roadmap to bring the full
          workflow online.
        </p>
      </header>

      <section className="grid gap-6 md:grid-cols-2">
        <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
          <h2 className="text-xl font-semibold text-gray-900">Glossary & Style Controls</h2>
          <p className="mt-2 text-sm text-gray-600">
            Maintain the shared terminology canon that guides every translation. Terms are enforced
            during prompt construction so Thai copy stays consistent with brand voice.
          </p>
          <Link
            href="/admin/glossary"
            className="mt-4 inline-flex items-center text-sm font-medium text-indigo-600 hover:text-indigo-500"
          >
            Manage glossary →
          </Link>
        </div>

        <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
          <h2 className="text-xl font-semibold text-gray-900">Submission Workspace</h2>
          <p className="mt-2 text-sm text-gray-600">
            Submit English assets, generate Thai drafts with glossary injection, and move work from
            editing to reviewer approval with clear status tracking.
          </p>
          <Link
            href="/submissions"
            className="mt-4 inline-flex items-center text-sm font-medium text-indigo-600 hover:text-indigo-500"
          >
            View submissions →
          </Link>
        </div>

        <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
          <h2 className="text-xl font-semibold text-gray-900">Next Milestones</h2>
          <ul className="mt-2 space-y-2 text-sm text-gray-600">
            <li>• Wire LLM providers with prompt templates and glossary injection.</li>
            <li>• Add editor workbench with side-by-side draft comparisons.</li>
            <li>• Ship reviewer approval flow with audit-ready logging.</li>
          </ul>
        </div>

        <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
          <h2 className="text-xl font-semibold text-gray-900">Analytics & Exports</h2>
          <p className="mt-2 text-sm text-gray-600">
            Review submission throughput, approval rate, and token usage, then export approved copy
            for delivery formats like CSV, DOCX, or social text.
          </p>
          <Link
            href="/metrics"
            className="mt-4 inline-flex items-center text-sm font-medium text-indigo-600 hover:text-indigo-500"
          >
            View metrics →
          </Link>
        </div>
      </section>

      <footer className="mt-auto border-t border-gray-200 pt-6 text-sm text-gray-500">
        <p>
          Implementation currently covers Phase 0–1 scaffolding. Continue with the roadmap in
          <code className="ml-1 rounded bg-gray-100 px-1 py-0.5">IMPLEMENTATION_PLAN.md</code> for
          feature build-out.
        </p>
      </footer>
    </div>
  );
}
