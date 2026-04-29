# Research Context Integration Tech Spec

## Document Status

- Status: Draft v1 (implementation-ready)
- Date: 2026-04-29
- Project: `Agent-Alpha`
- Scope: Add pre-run research distillation and context injection into existing script-first orchestrator runtime.

## 1) Problem Statement

The current runtime is strong at ticker-time analysis, but it does not consume your external multi-day research corpus (phone chats, cross-platform LLM sessions, ad-hoc notes, long reports).

That research is:

- high volume
- unstructured
- variable format/sequence
- mixed confidence (facts + inference + speculation)

The system needs a reliable way to convert this raw research blob into concise, usable context for agent runs without degrading accuracy, stability, or token efficiency.

## 2) Key Product Decision

Use **blob-as-source, brief-as-injection**.

- Keep raw research files untouched as canonical source records.
- Distill them into compact, structured, token-safe briefs before each run.
- Inject distilled context into selected decision stages (not every agent/tool prompt).

This supersedes any assumption that source docs follow a fixed sequence or template.

## 3) Goals

- Accept arbitrary raw research documents with no strict format.
- Produce a deterministic global brief for each run date.
- Optionally produce ticker-specific briefs when source text is ticker-focused.
- Inject context into existing graph flow with minimal architectural disruption.
- Preserve source traceability and confidence tags for every injected claim.
- Extend output reports to explicitly show how external context influenced decisions.

## 4) Non-Goals (Phase 1)

- Full knowledge-graph construction.
- Retrieval over huge historical corpora beyond local run-date scope.
- Autonomous web crawling or fact-checking engines.
- Replacing core analyst data tools with external narrative context.

## 5) High-Level Architecture

## 5.1 New Pipeline Stages

1. **Ingest** raw files from `research/`.
2. **Segment + classify** content into claim types.
3. **Distill** into compact context brief(s).
4. **Inject** brief(s) into selected graph prompts.
5. **Emit trace** into outputs (`metadata.json` + report section).

## 5.2 Existing Runtime Seam (Why this fits now)

Current graph already injects memory context via `past_context` through:

- `tradingagents/graph/propagation.py`
- `tradingagents/agents/managers/portfolio_manager.py`

Add a parallel field (`external_context`) through the same seam pattern.

## 6) Filesystem Contract

Supports both strict inbox flow and direct blob usage.

```text
research/
  inbox/
    YYYY-MM-DD/
      raw/
        <any files: .md .txt .pdf exports>
      manifest.yaml                 # optional in phase 1, recommended
  processed/
    YYYY-MM-DD/
      global_brief.md               # required if context is used
      global_brief.json             # required (machine schema)
      <TICKER>_brief.md             # optional
      source_trace.json             # required for auditability

prompts/
  distill/
    v1_system.md
    v1_segment_and_classify.md
    v1_synthesize_global_brief.md
    v1_synthesize_ticker_brief.md
  inject/
    v1_portfolio_context_block.md
    v1_research_manager_context_block.md
```

Fallback behavior:

- If `research/inbox/...` absent but a raw blob exists (example: `research/Apr29-2026-reseaerch.md`), the distiller may treat that file as the source set for the target date.

## 7) Distillation Data Model

## 7.1 Segment Classification

Each segment extracted from raw source should be tagged with:

- `segment_id`
- `source_path`
- `segment_type` (`fact`, `inference`, `speculative`, `scenario`, `trigger`, `invalidation`, `counterargument`, `prompt_transcript`)
- `confidence` (`high`, `medium`, `low`)
- `tickers` (list, optional)
- `time_horizon` (`short`, `medium`, `long`, `unknown`)
- `summary`

## 7.2 Global Brief JSON (required)

```json
{
  "schema_version": "1.0.0",
  "date": "2026-04-29",
  "source_files": ["research/Apr29-2026-reseaerch.md"],
  "macro_themes": [],
  "scenarios": [
    { "name": "base", "probability": 0.5, "description": "" },
    { "name": "bear", "probability": 0.35, "description": "" },
    { "name": "tail", "probability": 0.15, "description": "" }
  ],
  "trigger_signals": [],
  "invalidation_signals": [],
  "high_confidence_claims": [],
  "low_confidence_claims": [],
  "known_unknowns": [],
  "recommended_monitoring": [],
  "token_budget": 1200
}
```

## 7.3 Source Trace JSON (required)

Map every brief bullet back to source segments.

```json
{
  "brief_item_id": "theme_01",
  "derived_from": [
    {
      "source_path": "research/Apr29-2026-reseaerch.md",
      "line_start": 659,
      "line_end": 673,
      "confidence": "high"
    }
  ]
}
```

## 8) Prompt Template Strategy

## 8.1 Distill Prompts

- `v1_system.md`: role and constraints (no hallucinated facts, keep uncertainty explicit).
- `v1_segment_and_classify.md`: classify and score segments.
- `v1_synthesize_global_brief.md`: produce macro/timing/scenario brief.
- `v1_synthesize_ticker_brief.md`: optional per-ticker addendum.

Required output style:

- compact bullets
- explicit confidence tags
- explicit trigger/invalidation markers
- capped length

## 8.2 Inject Prompts

- `v1_portfolio_context_block.md`
- `v1_research_manager_context_block.md`

Injection block requirements:

- 5-12 bullets
- include uncertainty and low-confidence disclaimers
- include top 3 trigger signals and top 3 invalidators
- include source IDs

## 9) Runtime Integration Design

## 9.1 Graph State Changes

Extend `AgentState` with:

- `external_context`: distilled run-level context text
- `external_context_meta`: short metadata summary (source count, confidence profile, date)

## 9.2 Propagation Changes

Update initial state construction in `tradingagents/graph/propagation.py` to accept optional external context payload.

## 9.3 Prompt Injection Targets

Phase 1 targets:

- `tradingagents/agents/managers/portfolio_manager.py` (required)
- `tradingagents/agents/managers/research_manager.py` (required)

Phase 2 optional:

- bull/bear researcher prompts for richer debate framing

Do not inject raw external blob into:

- low-level analyst tool prompts
- tool-calling loops where token efficiency is critical

## 9.4 Script Flow Changes (`scripts/run_today.py`)

Before running tickers:

1. Resolve run date.
2. Load/create processed brief(s) for date.
3. Attach `external_context` to each ticker invocation.
4. Record context usage in output metadata.

New metadata fields:

- `research_context_used` (bool)
- `research_context_date`
- `research_source_files`
- `research_confidence_profile`

## 10) Report and Output Contract Extensions

Update report generation to add:

`## External Research Context Used`

Fields:

- Summary of context brief
- Confidence profile
- Trigger/invalidation highlights
- Source references

This section complements (not replaces) existing:

- `Confidence and Failure Modes`
- `Evidence and Sources`

## 11) Guardrails

- **Freshness:** warn on stale context older than configurable threshold (default 7 days).
- **Token budget:** enforce hard max for injected context (default 1200 tokens equivalent).
- **Confidence weighting:** low-confidence segments cannot dominate final brief.
- **Contradiction detection:** include explicit `Conflicts with live data` block when detected.
- **Traceability:** no injected bullet without source mapping.
- **Safety:** never include credentials or private tokens from raw files.

## 12) DeepAgents Integration Plan (LangChain)

Use DeepAgents capabilities as a distillation engine, not as a replacement for core graph execution.

## 12.1 Phase 1 (No deepagents dependency required)

- Implement deterministic local distiller with current stack.
- Keep interfaces compatible with future deepagents adapter.

## 12.2 Phase 2 (Optional deepagents adapter)

- Add `distillation_backend = local | deepagents`.
- Use deepagents for long-horizon iterative extraction/synthesis over large blobs.
- Preserve exact same output schema (`global_brief.json`, trace contract).

## 12.3 Compatibility Rule

Regardless of backend, injection and report contracts remain identical.

## 13) Testing Strategy

## 13.1 Unit Tests

- segment classifier tags and confidence behavior
- brief generation length/token limits
- state injection propagation
- metadata enrichment

## 13.2 Contract Tests

- validate `global_brief.json` schema
- validate source trace mapping integrity
- validate output report includes context section when enabled

## 13.3 End-to-End Tests

- run with no research source (graceful fallback)
- run with one raw blob (`research/Apr29-2026-reseaerch.md`)
- run multi-ticker with same global brief
- run with contradictory research + live signals and verify conflict block

## 14) Rollout Plan

## Milestone A (MVP)

- Add research distillation script.
- Inject global brief into PM + Research Manager.
- Add metadata + report section.

## Milestone B

- Add ticker-specific optional briefs.
- Add confidence-weighting and contradiction surfacing.

## Milestone C

- Add deepagents distillation backend.
- Add richer trace and monitoring dashboards.

## 15) Open Decisions

- Whether to require `manifest.yaml` in phase 1 or keep optional.
- Whether to persist full segment corpus under `research/processed/segments.json`.
- Final token budget default by provider/model.
- Whether low-confidence speculative sections should be dropped entirely or summarized as risk notes.

## 16) Recommended Judgment Call (based on latest report analysis)

The earlier integration pattern is still correct, with one critical update:

- Treat raw research as variable “context blob” input.
- Standardize only the **processed outputs**, not the source format.

This preserves your real workflow (messy multi-platform dumps) while keeping runtime quality high and repeatable.
