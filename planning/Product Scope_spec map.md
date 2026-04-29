# Product Scope and Specification Map: Minimal Agent-Alpha Orchestrator

## Scope Statement

- This specification map is scoped to the target state:
  - remove CLI surface
  - remove assets/demo/branding-heavy components
  - remove Docker options
  - keep a clean orchestrator core
  - run scripts for arbitrary ticker(s) using today's date by default
  - generate comprehensive markdown reports into `outputs/`
- This document is requirements-only. No production code changes are performed here.

## Product Goal

Create a lean personal-project repo that does one thing very well:

1. Accept one or many tickers.
2. Run the orchestrated analysis pipeline.
3. Emit human-readable, portfolio-ready markdown reports in `outputs/`.
4. Provide stable artifacts that later skills can parse for deeper research and meta-analysis.

## Target Product Identity

## Core Shape

- **Orchestrator-first** Python package (`tradingagents/` kept initially for compatibility).
- **Script-first interface** (no interactive CLI dependency).
- **Output contract-first design** (markdown schema in `outputs/` is the backbone for follow-on skills).

## Not In Scope for the Base Version

- interactive terminal UX
- social/community announcement plumbing
- screenshots/marketing assets
- containerized runtime path for now
- broad feature expansion before stabilization

## Keep / Remove / Defer Matrix

## Keep (Base System)

- `tradingagents/` core orchestration, agents, graph logic, provider abstraction.
- `tests/` as baseline quality safety net.
- legal/provenance files: `LICENSE`, selected historical records.

## Remove (Simplification Wave)

- `cli/` package and command entrypoint wiring.
- `assets/` demo/branding media.
- Docker-focused runtime files and docs references (`Dockerfile`, `docker-compose.yml`) if not needed for personal workflow.
- external announcement/social integrations tied to old identity.

## Defer (After Minimal System Is Stable)

- package rename (`tradingagents` -> new package name).
- deep semantic role renaming.
- API/service layer.
- strategy plugin marketplace-level complexity.

## Legal and Attribution Guardrails (Still Required)

- Preserve `LICENSE` and required Apache-2.0 obligations.
- Keep meaningful provenance where appropriate (e.g., fork lineage notes).
- Review logo/image provenance before deleting or redistributing branded assets.
- If public release: verify dependency-license carry-through before packaging distribution artifacts.

## Recommended Architecture for the Minimal Version

## Runtime Surface

- One or two script entrypoints under `scripts/`:
  - `run_today.py` (defaults to today's date)
  - optional `run_range.py` (batch runs)
- Optional thin reusable module:
  - `tradingagents/orchestrator_runner.py` for script/programmatic reuse.

## Input Contract

- `--ticker AAPL` or `--tickers AAPL,MSFT,NVDA`
- date defaults to local "today" if omitted
- provider/model parameters optional with sane defaults

## Output Contract (Critical for Future Skills)

- `outputs/YYYY-MM-DD/<ticker>/report.md`
- optional companion machine-readable files:
  - `outputs/YYYY-MM-DD/<ticker>/report.json`
  - `outputs/YYYY-MM-DD/<ticker>/metadata.json`

Minimum markdown sections to standardize:

1. Run Metadata
2. Analyst Summaries
3. Bull vs Bear Debate Highlights
4. Trader Proposal
5. Risk Review
6. Final Recommendation
7. Confidence and Key Risks
8. Evidence and Citations
9. Next Actions / Watchlist

This schema is the key enabler for downstream research skills.

## Recommended Execution Specification

## Phase 0 - Decision Lock (Requirements Gate)

- Confirm the exact "remove now" list:
  - `cli/`, `assets/`, Docker files, CLI docs references
- Confirm minimal runtime dependencies required post-removal.
- Confirm canonical output schema for markdown reports.

## Phase 1 - Surgical Simplification

- Remove CLI and related command entrypoint bindings.
- Remove assets and unused branding/community references.
- Remove Docker pathway and related docs if not needed.
- Keep orchestration internals and tests intact where possible.

Success criteria:

- repo boots without CLI/Docker/assets dependencies
- no dead imports from removed modules
- tests for core graph still run (or are cleanly updated)

## Phase 2 - Script-First Execution

- Introduce simple scripts for:
  - single ticker run
  - multi-ticker run for today's date
- Ensure predictable outputs path creation and naming.
- Add graceful error handling per ticker so batch runs continue.

Success criteria:

- one command can run N tickers and produce N markdown reports
- outputs are deterministic in location and readable in one pass

## Phase 3 - Report Quality and Stability

- Harden markdown template for readability and consistency.
- Add basic validation:
  - required report headings present
  - metadata completeness
- Add snapshot tests against report format.

Success criteria:

- output docs are portfolio-presentable without manual cleanup
- format remains stable across runs/releases

## Phase 4 - Skill-Ready Layer

- Define a parsing contract for future "research-on-reports" skills.
- Add optional index file:
  - `outputs/YYYY-MM-DD/index.md` summarizing all tickers
- Add hooks for post-processing skills (no heavy logic yet).

Success criteria:

- downstream skills can reliably ingest outputs without brittle parsing

## Phase 5 - Portfolio Polish

- Rewrite README to emphasize:
  - simple orchestrator usage
  - example output reports
  - extension path into advanced skills
- Keep architecture diagram lightweight and text-first.

Success criteria:

- a reviewer can clone, run one command, inspect `outputs/`, and understand value in under 10 minutes

## Risk Register (for This Specific Pivot)

- **High:** removing CLI may break existing entrypoint assumptions and tests.
- **High:** deleting Docker files may remove an environment many examples rely on.
- **Medium:** aggressive deletion can remove useful provenance or legal signals.
- **Medium:** output markdown schema drift can undermine future skill automation.
- **Low:** package renaming deferred avoids major breakage now.

## Why This Plan Is Best for Your Goal

- It optimizes for **clarity and demonstrable value** over feature breadth.
- It creates a **stable artifact layer** (`outputs/*.md`) that is ideal for advanced skills.
- It avoids early high-risk refactors (package rename, deep semantic rewiring).
- It yields a portfolio story with clean progression:
  - base orchestrator -> standardized reports -> research augmentation skills.

## Suggested `planning/` Document Set

- `planning/Possibility_map.md` (this file): scope and chosen direction.
- `planning/Portfolio_Simplification_Plan.md`: execution requirements and acceptance criteria.
- `planning/Output_Schema.md`: markdown contract and parser expectations for future skills.

## Decision Snapshot

- Recommended path: **Minimal Orchestrator Pivot (script-first, output-first)**.
- Project naming direction: **Agent-Alpha** (distribution/project identity).
- Immediate next planning artifact: finalize exact deletion inventory and report schema before any write-capable implementation pass.

## Evidence Anchors Used

- `README.md`
- `pyproject.toml`
- `cli/` (entrypoint and UX surface)
- `assets/`
- `Dockerfile`
- `docker-compose.yml`
- `tradingagents/graph/setup.py`
- `tests/`
