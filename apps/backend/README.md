# Leo Backend

FastAPI service orchestrating translation and localization workflows for Leo.

## Local Development

```bash
uvicorn app.main:app --reload
```

Create a `.env` file (auto-loaded via `pydantic-settings`) with any secrets you need, for example:

```env
LEO_OPENAI_API_KEY="sk-..."          # enables primary LLM generation
LEO_GOOGLE_TRANSLATE_API_KEY="..."    # optional MT fallback
LEO_BLOCKED_TERMS='["urgent"]'        # JSON array for flagged-term linting
```

Install dependencies using your preferred tool, for example:

```bash
pip install -e .[dev]
```

Then run the async test suite:

```bash
pytest
```

## API Overview

- `GET /health` – service heartbeat
- `POST /translate` – generate Thai draft (also used internally for submissions)
- `CRUD /glossary` – glossary management endpoints
- `POST /submissions` – create a submission and auto-generate Thai draft
- `GET /submissions` – list submissions by status; `PUT /submissions/{id}` to update editor/reviewer fields
- `GET /submissions/{id}/export?format=csv|docx|social` – export localized copy for downstream channels
- `GET /metrics/overview` – aggregate submission volume, approval rate, tokens, and spend (optional `days` filter)
