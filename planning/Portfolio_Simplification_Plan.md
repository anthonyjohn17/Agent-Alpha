# Product Requirements Document: Portfolio Simplification

## Objective

Define requirements to convert this repository into a focused personal-project system:

- simple trading-agents orchestrator
- script-driven execution for one or many tickers
- defaults to today's date
- outputs comprehensive markdown reports to `outputs/`
- project identity framed as `Multi-Agent-Trading-Agents`

No implementation is performed in this document. This is the approved PRD baseline for later implementation.

## Target Operating Model

One primary workflow:

1. Run script with ticker list.
2. Pipeline executes orchestrated analysis.
3. Reports are written to `outputs/YYYY-MM-DD/<ticker>/report.md`.
4. Optional aggregate summary is written to `outputs/YYYY-MM-DD/index.md`.

## Scope Boundaries

## In Scope

- Remove CLI runtime and related command entrypoint complexity.
- Remove assets and branding-heavy collateral not needed for core operation.
- Remove Docker pathway for the base version.
- Create script-first orchestration entrypoints.
- Define and enforce stable markdown output format.

## Out of Scope (for initial simplification)

- package rename
- service/API deployment surface
- live trading integration
- extensive strategy marketplace
- advanced post-processing intelligence (will be skill-based later)

## Functional Requirements

- Accept input ticker(s):
  - single ticker
  - comma-separated tickers
  - optional file-based ticker list (future extension)
- Default analysis date to local today's date.
- Allow optional override date.
- Continue batch execution if one ticker fails.
- Produce one report per ticker and include run metadata.

## Report Requirements (`report.md`)

Required sections:

1. Run Metadata
2. Analyst Findings
3. Debate Synthesis (bull vs bear)
4. Trader Recommendation
5. Risk Assessment
6. Final Decision
7. Confidence and Failure Modes
8. Supporting Evidence
9. Follow-up Questions

Formatting requirements:

- clean markdown headings
- short paragraphs and bullet lists
- deterministic section order
- no provider-specific raw dumps unless under an appendix heading

## Proposed File/Module Direction

## Remove Candidates

- `cli/`
- `assets/`
- `Dockerfile`
- `docker-compose.yml`
- docs references that are only relevant to removed runtime surfaces

## Keep and Refocus

- `tradingagents/` core logic
- `tests/` (update to match new runtime surface)
- `scripts/` as execution layer

## Additions

- `scripts/run_today.py` (single + multi ticker execution)
- optional `scripts/run_batch.py` (expanded batch features)
- `outputs/` (gitignored output artifact root)
- markdown template/helper for stable report construction

## Execution Plan (Phased)

## Phase 0: Pre-Change Checklist

- Approve deletion inventory.
- Approve markdown output schema.
- Confirm legal/provenance retention rules.
- Confirm minimal dependency set after CLI/Docker removal.

Approval Artifact:

- signed-off checklist in `planning/`.

## Phase 1: Structural Prune

- Remove CLI and related references.
- Remove assets and related references.
- Remove Docker files and docs references.
- Update project metadata/entrypoints to avoid broken commands.

Acceptance Evidence:

- repo imports and starts without removed surfaces.

## Phase 2: Script Runtime

- Add script runner(s) for tickers with today's date default.
- Add robust path creation for outputs.
- Add per-ticker error isolation.

Acceptance Evidence:

- one command produces per-ticker markdown reports under `outputs/`.

## Phase 3: Output Standardization

- Implement stable markdown template and metadata block.
- Add tests to validate required sections/order.
- Add aggregate daily index generation.

Acceptance Evidence:

- machine-parseable and human-readable output set.

## Phase 4: Portfolio Hardening

- Refresh README quickstart around script-first flow.
- Provide one end-to-end example command and expected output tree.
- Add "next skills" section describing advanced research on outputs.

Acceptance Evidence:

- clear portfolio narrative and reproducible demonstration path.

## Acceptance Criteria

- Running a single command with multiple tickers generates markdown reports for each ticker.
- Reports are stored in predictable date/ticker folders.
- Reports are understandable without opening source code.
- No runtime dependency on CLI, assets, or Docker path.
- Core orchestration still functions after simplification.

## Validation Checklist

- Imports resolve after removals.
- Script execution succeeds on at least 3 tickers.
- One intentional ticker failure does not stop the batch.
- `outputs/` structure matches contract.
- Report headings validated by tests.

## Risks and Mitigations

- **Risk:** Hidden dependencies on CLI modules.
  - **Mitigation:** search and remove/replace imports before deletion.
- **Risk:** Existing docs become misleading.
  - **Mitigation:** update README in same change set as structural prune.
- **Risk:** Report format churn blocks future skills.
  - **Mitigation:** lock section schema and add format tests early.
- **Risk:** Over-pruning removes useful debugging paths.
  - **Mitigation:** archive selected materials under `planning/archive-notes` before removal.

## Future Skill Layer (Post-Simplification)

Once output contract is stable, build skills for:

- cross-ticker daily synthesis
- signal quality scoring over time
- contradiction detection across analyst narratives
- recurring thesis tracking and drift analysis
- report-to-research knowledge graph extraction

This keeps the core repo simple while enabling sophisticated analysis through composable skills.
