# Leo Localization Platform

End-to-end workflow for translating English content into culturally resonant Thai copy. This repository houses both the customer-facing frontend and the AI-assisted orchestration backend.

## Repository Layout

- `apps/frontend` – Next.js (TypeScript + Tailwind) client for content submission, editing, and review workflows.
- `apps/backend` – FastAPI service that will orchestrate glossary retrieval, LLM prompts, and reviewer handoffs.
- `IMPLEMENTATION_PLAN.md` – Detailed multi-phase roadmap guiding delivery.
- `READLEO.md` – Product requirements and context for the Leo initiative.

## Getting Started

### Frontend (Next.js)
```bash
cd apps/frontend
npm install  # already run by scaffolding, re-run if dependencies change
npm run dev
```
The development server runs on `http://localhost:3000` by default.
Set `NEXT_PUBLIC_API_BASE_URL` in `.env.local` if the FastAPI service is not running on
`http://localhost:8000`.

Key routes:
- `/` – overview and quick links.
- `/admin/glossary` – terminology management interface.
- `/submissions` – submission workspace with status filters.
- `/submissions/new` – upload English source content and generate a Thai draft.
- `/submissions/[id]` – editor/reviewer workspace for a specific submission.
- `/metrics` – analytics dashboard summarising throughput, approvals, warnings, and spend.

### Backend (FastAPI)
```bash
cd apps/backend
pip install -e .[dev]
uvicorn app.main:app --reload
```
The API serves `http://localhost:8000`, with `/docs` exposing the automatic Swagger UI. The
service boots with SQLite by default (`LEO_DATABASE_URL`), auto-creates tables, and seeds starter
glossary terms unless `LEO_SEED_INITIAL_GLOSSARY=false`.
Provide `LEO_OPENAI_API_KEY` to enable LLM-powered Thai drafts (default model: `gpt-4.1-mini`).
Optionally configure `LEO_GOOGLE_TRANSLATE_API_KEY` for machine-translation fallback while the
primary provider is unavailable. Add JSON-formatted blocked terms via `LEO_BLOCKED_TERMS` (e.g.
`["urgent"]`) to surface reviewer warnings when certain phrases appear.

## Tooling & Conventions

- Node 20.x and Python 3.10+ are recommended.
- ESLint and Tailwind style conventions ship with the frontend scaffold; run `npm run lint` inside `apps/frontend`.
- Ruff + Pytest are configured as optional dev dependencies for the backend; run `ruff check app` and `pytest` when the environment is installed.
- Environment variables use the `LEO_` prefix (see `app/core/config.py`). Add a local `.env` file for secrets such as `LEO_OPENAI_API_KEY`.
- Glossary CRUD endpoints live at `/glossary`; the frontend admin surface is available at
  `http://localhost:3000/admin/glossary` once both services are running.
- Translation responses now include the rendered LLM prompt, provider metadata, and any sensitive
  term warnings so reviewers can quickly assess draft quality.
- Submission APIs (`/submissions`) create records with generated drafts, track editor/reviewer
  status changes, and surface warnings in the UI.
- Metrics endpoint (`/metrics/overview`) powers the dashboard, and `/submissions/{id}/export`
  produces CSV, DOCX, or social-ready text for downstream delivery.

## Next Steps

Implementation is currently in **Phase 0** of `IMPLEMENTATION_PLAN.md`: scaffolding the core services, configuring automation, and aligning on glossary inputs. Follow the plan file to continue feature build-out in subsequent phases.
# Leo-Trans
