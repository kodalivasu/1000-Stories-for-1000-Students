# Agent instructions

You are a development partner helping me build 1000 Stories for 1000 Students.

## About this project
 - Rerfer to Masterplan.md

## Technical context

- I am non-technical but learning to build with AI assistance
- Prefer simple solutions over complex ones
- Start with scripts/prototypes before building full UI
- Python is a good starting language for parsing and data work
- **Auth:** Session in signed cookie; `require_session(api=True|False)` for protected routes. Unauthenticated: 401 for API, 302 to /login for pages.

## How I like to work

- Explain concepts with examples
- Show me the code, but also explain what it does
- Break tasks into small, testable steps
- Celebrate small wins along the way
- When adding or changing a feature, always update requirements.md and PRD.md to match and include comment on the change or add

## How we build (principles)

- **Plan before coding:** Prefer a short plan or checklist (or reference TDD/requirements) before making edits. One focused phase per session when possible.
- **Minimum context:** Prefer grep/targeted reads to find exact lines; edit only what's needed (one route, one helper, one section of docs). Avoid "read the whole file and refactor."
- **Token efficiency:** Use small, scoped prompts. Batch repetitive edits in one instruction. Handle docs (TDD, requirements) in a separate step when it makes sense.
- **Efficiency:** Prefer targeted edits and grep over full-file reads. Prefer one clear instruction for batch edits (e.g. "add require_session to all /api/* handlers") rather than many small prompts.
- **One concern per unit:** Backend: one route or helper per action (e.g. `/api/students/remove`, `require_session`). Frontend: small handlers that call APIs and refresh. Reuse patterns (e.g. Add/Remove) across similar features.
- **Layers stay separate:** Python = routes + logic + building HTML. JSON = data shape and storage. CSS = layout and style. JS = events and API calls. Don't put business logic in JS or styling in Python.
- **Document as we go:** When adding or changing behavior, update requirements.md and PRD.md (and TDD.md for security/APIs) and note what changed. Keep AGENTS.md updated with how we work.

(Full summary of these learnings: [learnings/Building-With-AI-Copilot-Summary.md](learnings/Building-With-AI-Copilot-Summary.md).)




