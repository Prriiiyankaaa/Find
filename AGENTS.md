# Repository Guidelines For Agents

This is the single committed instruction file for AI coding agents working on Find. Keep shared agent guidance here instead of adding duplicate tool-specific files such as `AGENT.md`, `CODEX.md`, `CLAUDE.md`, `.cursorrules`, `.windsurfrules`, or `.github/copilot-instructions.md` unless a maintainer explicitly asks for one.

## Agent Compatibility And Placement

- Keep this file at the repository root as `AGENTS.md`.
- Codex, Cursor, Windsurf, opencode, GitHub Copilot agent/CLI, and other AGENTS.md-compatible tools can use this root file as project-level guidance.
- Claude Code commonly uses `CLAUDE.md`; for this repository, ask Claude to read or attach `AGENTS.md` rather than creating a separate committed `CLAUDE.md`.
- Cursor and Windsurf also support their own rule directories, but this repo should use root `AGENTS.md` for the shared baseline to avoid conflicting instructions.
- If a tool supports extra local or user-level rules, keep those personal files outside the repo. Do not commit personal agent memories or machine-specific rules.
- If future scoped rules are needed, prefer additional `AGENTS.md` files inside a specific directory only when the guidance truly applies only to that directory.

## Start Here

1. Read `README.md` for product scope, architecture, and run modes.
2. Read `CONTRIBUTING.md` for branch, PR, and review process.
3. Check the linked issue before editing. If the PR has no linked issue, keep the change blocked until the maintainer confirms scope.
4. Keep the branch focused on one issue. Do not bundle opportunistic refactors, unrelated docs, formatting churn, or cleanup.

## Project Structure & Module Organization

Find is a local-first AI image intelligence app. Key paths:

- `backend/src/find_api/` - FastAPI API, SQLAlchemy models, Redis/RQ jobs, MinIO helpers, and ML wrappers.
- `frontend/src/app/` - Next.js App Router UI.
- `frontend/src/lib/` - React Query API client, media URL helpers, and shared utilities.
- `docker-compose.yml` - PostgreSQL/pgvector, Redis, MinIO, API, worker, and web orchestration.
- `.env.example` - documented local configuration. Keep real `.env` files private.
- `.github/workflows/ci.yml` - frontend and backend CI checks.

Avoid generated paths such as `frontend/.next/`, `frontend/node_modules/`, `.ruff_cache/`, `__pycache__/`, and model weights.

Understand the user-visible flow before editing behavior: upload, worker processing, status polling, gallery, search, clustering, people, preview modal, and feedback.

## Build, Test, and Development Commands

From the repository root:

```bash
docker compose up --build
```

Starts the full local stack. The default full-stack ML workflow is optimized for NVIDIA GPU support.

Frontend:

```bash
cd frontend
pnpm install
pnpm dev
pnpm check
pnpm build
```

`pnpm dev` runs Next.js, `pnpm check` runs Biome, and `pnpm build` verifies production output.

Backend:

```bash
cd backend
uv sync
uv run uvicorn find_api.main:app --reload
uv run rq worker --url redis://localhost:6379 high default low
uv run ruff check .
uv run ruff format --check .
uv run pytest tests/ -v
```

Run the API and worker separately when not using Docker.

Prefer the light stack for routine UI, API, docs, and workflow work:

```bash
docker compose -f docker-compose.light.yml up --build
```

Use the full stack only when the change needs real ML behavior.

## Coding Style & Naming Conventions

Frontend code uses TypeScript strict mode, 2-space indentation, double quotes, and Biome formatting. Keep shared API types and functions in `frontend/src/lib/api.ts`.

Backend code targets Python 3.12 and is checked with Ruff. Use `snake_case` for Python functions/modules and `PascalCase` for SQLAlchemy model classes. Keep routers thin; put storage, queue, database, and ML logic in their existing modules.

For cross-stack changes, verify the API contract in `frontend/src/lib/api.ts` and the matching FastAPI router before changing either side.

## Testing Guidelines

Run the automated test suite before opening a PR: `pnpm check && pnpm build` for frontend work and `uv run ruff check . && uv run ruff format --check . && uv run pytest tests/` for backend work. For integration changes, manually verify upload, job status polling, gallery, search, and clustering.

## Commit & Pull Request Guidelines

Recent commits use concise prefixes such as `feat:`, `docs:`, `refactor:`, `update:`, and `Fix CI:`. Follow that style with an imperative summary.

Pull requests should include a clear description, linked issue when relevant, testing notes, screenshots or recordings for UI changes, and documentation updates for API, environment, or workflow changes.

## Security & Configuration Tips

Do not commit `.env`, MinIO data, database files, downloaded model weights, or secrets. Keep `EMBEDDING_DIM` aligned with the configured CLIP/SigLIP model and pgvector columns.

Find is local-first and privacy-focused. Do not add cloud calls, hosted model APIs, telemetry, analytics, or external uploads for user images, captions, OCR text, embeddings, faces, feedback, or storage data unless the linked issue explicitly asks for that architecture.

Treat these as sensitive data:

- uploaded images and thumbnails
- object storage contents and keys
- captions, OCR text, EXIF metadata, embeddings, and face/person data
- user feedback and personalization signals
- database dumps, logs, and `.env` values

Security rules for agents:

- Never hardcode credentials, public buckets, API keys, or local absolute paths.
- Keep real secrets out of examples; update `.env.example` only with safe placeholder values.
- Do not print raw secrets, signed URLs, tokens, or private file paths in logs or error messages.
- Use existing sanitized error helpers for user-facing backend errors.
- Do not weaken GitHub Actions, upload validation, ZIP safety checks, dependency policy, or secret scanning to make a PR pass.
- Do not add new dependencies for small tasks unless the repo already uses that library or the issue justifies it.
- For destructive actions such as delete, reprocess, recluster, migration, or storage cleanup, preserve existing data unless a verified replacement is ready.
- Keep hidden/vault, face recognition, and personalization work local-only by default.

## Agent Review Checklist

Before finishing a change, verify:

- The diff matches the assigned issue and does not touch unrelated files.
- Generated files, caches, model weights, Docker volumes, and local databases are not included.
- Frontend text is visible in both dark and light mode when UI is touched.
- Backend changes include focused tests when they affect API behavior, storage, queues, models, or migrations.
- Docs changes describe the current project accurately and do not invent commands or architecture.
- PR notes say what was tested and what was not tested.
