Objective
Take English media, content, and written text, and translate it into Thai while maintaining meaning, tone, and cultural relevance.

Responsibilities

Translation Accuracy

Ensure that all English content is translated into Thai with precise meaning.

Avoid direct, word-for-word translations—focus on natural, fluent Thai.

Copywriting Adaptation

Rewrite and adapt translated text so it reads smoothly for Thai audiences.

Maintain persuasive, engaging, and professional tone depending on the context (ads, articles, captions, scripts, etc.).

Cultural Sensitivity

Adjust idioms, expressions, and references so they resonate with Thai culture.

Ensure the final output sounds like it was originally written in Thai.

Consistency

Follow brand voice guidelines (formal, casual, friendly, authoritative, etc.).

Keep terminology and messaging consistent across all translated materials.

Deliverables

Polished Thai-language copies of English media and text (social media posts, ads, articles, presentations, etc.).

Optional: Provide side-by-side English/Thai versions for review if requested.

Requirements

Strong command of English and native-level Thai writing skills.

Experience in copywriting, not just translation.

Ability to localize text for Thai audiences while keeping original intent.

Product Requirements Document (PRD)

Overview
Translate English media and text into Thai with natural, persuasive, and culturally resonant copy that maintains original meaning and intent.

Goals
- High-quality Thai output preserving meaning and tone
- Copywriting adaptation tailored to channel/context (ads, social, long-form)
- Consistency with brand voice and terminology
- Fast turnaround with clear human-in-the-loop review workflow

Users
- Content Managers
- Thai Copywriters/Translators
- Reviewers/Editors
- Marketing Stakeholders

Primary Use Cases
- Translate social captions, ads, articles, scripts, and presentations
- Localize idioms and cultural references
- Optional side-by-side English/Thai versions for review
- Enforce glossary and style guide

Scope (v1)
- Upload or paste English text (or transcripts)
- Generate Thai draft using LLM with rules and glossary
- Human edit and adaptation workflow with comments
- Reviewer approval and version history
- Export to common formats/channels

Out of Scope (initial)
- Automatic speech-to-text for media
- Non-Thai target languages
- Large-scale SEO localization
- Deep CMS integrations (planned for later phases)

User Workflow
1. Submit English content
2. System produces Thai draft (LLM + glossary/style constraints)
3. Editor adapts copy; reviewer provides feedback
4. Approval; export/publish
5. Track quality and turnaround metrics

Quality Requirements
- Accuracy ≥ 95% on sampled reviews
- Tone/style match per brand guide
- Cultural sensitivity and flagged-terms checks
- Draft turnaround < 5 minutes for ≤ 2k words

Success Metrics
- Post-edit distance (LLM draft → final)
- Reviewer rework time and approval rate
- Glossary compliance rate
- Turnaround time per item

Risks & Mitigations
- Hallucinations → constrained prompts, retrieval/context, mandatory review
- Cultural missteps → curated guidelines, sensitive-term lints, human QA
- Inconsistency → glossary memory, templates, reviewer checklists
- Privacy → data retention controls, PII redaction, access policies

Release Plan
- v0: Manual input, draft generation, manual review
- v1: Glossary, templates, versioning, exports, metrics
- v2: CMS integrations, collaboration, automated QA checks

Acceptance Criteria
- Given English input, system outputs a Thai draft aligned to style guide
- Editors can revise with comments and track versions
- Glossary terms are suggested/enforced during drafting
- Exports function for target channels (e.g., CSV, DOCX, social)

Proposed Tech Stack

Application
- Frontend: Next.js (React) with TypeScript and Tailwind CSS
- Backend: Node.js (NestJS) or Python (FastAPI) for AI orchestration services
- Authentication: NextAuth/OAuth with JWT sessions

AI/Language
- LLM: OpenAI (GPT-4.1/GPT-4o) or Anthropic Claude for translation + copy adaptation
- MT fallback: Google Cloud Translate for baseline translation and backstops
- Orchestration: LangChain or lightweight custom prompting pipelines
- Memory: Glossary/style guide stored in DB with optional embeddings (pgvector)

Data
- Database: PostgreSQL
- Cache/Queue: Redis (rate limiting, job queues)
- Object Storage: S3-compatible (uploads/exports)

Ops
- Deployment: Vercel (frontend), Fly.io/Render/AWS (backend)
- CI/CD: GitHub Actions
- Observability: Sentry, OpenTelemetry, Prometheus/Grafana

Security & Compliance
- Secrets: Vercel/Cloud provider secrets manager
- Data: PII redaction and configurable retention
- Access: Role-based access control and audit logs

Optional Integrations (future)
- Notion/Google Docs imports
- CMS connectors (Contentful, WordPress)
- TMS (Phrase, Transifex)

Implementation Plan

Phase 0 – Foundations (Week 0-1)
- Confirm brand voice, glossary sources, and reviewer SLAs with stakeholders.
- Stand up project scaffolding (Next.js frontend, API service, PostgreSQL, Redis, S3 buckets).
- Configure secrets management, linting, formatting, CI skeleton, and monitoring hooks (Sentry/OpenTelemetry).

Phase 1 – Knowledge Base & Controls (Week 1-2)
- Import initial glossary/style guides into PostgreSQL with admin tooling for updates.
- Implement glossary API endpoints and caching with Redis; expose CRUD in internal admin UI.
- Define prompt templates and guardrails referencing glossary entries and brand tone metadata.

Phase 2 – Draft Generation Pipeline (Week 2-3)
- Integrate LLM provider (OpenAI/Claude) with retry, cost logging, and fallbacks to Google Translate.
- Build translation request service that orchestrates retrieval of glossary/style context and produces Thai drafts.
- Add sensitive-term linting and configurable blocked-word checks post-generation.

Phase 3 – Editor & Reviewer Workflow (Week 3-5)
- Implement submission UI for uploading/pasting English content (plain text + file upload to S3).
- Deliver editing workspace with side-by-side draft/final views, comment threads, and version diffing (PostgreSQL history tables).
- Create reviewer approval flow with status transitions, notifications, and audit logging.

Phase 4 – Quality, Metrics & Exports (Week 5-6)
- Capture post-edit distance, turnaround time, glossary compliance metrics; expose dashboards/reports.
- Implement export adapters for CSV, DOCX, and social channel templates with field mapping.
- Add reviewer checklist enforcement and automated QA sampling hooks.

Phase 5 – Hardening & Launch (Week 6-7)
- Load test key endpoints, validate latency and throughput targets, and run security review.
- Finalize RBAC roles, data retention policies, and PII redaction verification.
- Pilot with select content managers, collect feedback, iterate, and prepare public rollout communications.
