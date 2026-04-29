# Output Schema Specification (for Future Skills)

## Purpose

Define a strict, durable output contract for the simplified trading-agents orchestrator so that:

- humans can quickly read daily analysis reports
- downstream skills can parse reports reliably without brittle heuristics
- outputs are stable across runs, models, and future refactors

This specification is implementation-agnostic and serves as the output contract for implementation.

## Design Principles

- **Parseable first:** markdown remains human-friendly but follows deterministic structure.
- **Stable ordering:** required sections always appear in the same sequence.
- **Evidence-aware:** every recommendation includes supporting evidence and uncertainty.
- **Batch-ready:** supports one report per ticker plus optional daily index.
- **Skill-ready:** section headers and key labels are machine-locatable.

## Directory and File Contract

## Root

- `outputs/`

## Daily folder

- `outputs/YYYY-MM-DD/`

## Per ticker folder

- `outputs/YYYY-MM-DD/<TICKER>/`

## Required files

- `outputs/YYYY-MM-DD/<TICKER>/report.md`
- `outputs/YYYY-MM-DD/<TICKER>/metadata.json`

## Optional files

- `outputs/YYYY-MM-DD/<TICKER>/report.json`
- `outputs/YYYY-MM-DD/index.md`
- `outputs/YYYY-MM-DD/run_manifest.json`

## Naming Rules

- ticker folder is uppercase ticker symbol as provided by runtime normalization.
- date uses ISO local date format `YYYY-MM-DD`.
- one ticker has exactly one canonical `report.md` per run date unless version suffixing is enabled.

## `report.md` Canonical Structure

Sections below are **required**, **ordered**, and must use exactly the heading text shown.

1. `# Multi-Agent-Trading-Agents Report: <TICKER> (<YYYY-MM-DD>)`
2. `## 1) Run Metadata`
3. `## 2) Market Context Snapshot`
4. `## 3) Analyst Findings`
5. `## 4) Debate Synthesis`
6. `## 5) Trader Recommendation`
7. `## 6) Risk Assessment`
8. `## 7) Final Decision`
9. `## 8) Confidence and Failure Modes`
10. `## 9) Evidence and Sources`
11. `## 10) Follow-up Questions`
12. `## 11) Appendix (Optional)`

If a section has no content, emit the heading and the line `- None`.

## Section-Level Field Requirements

## 1) Run Metadata

Required labeled bullets:

- `- Run ID: <string>`
- `- Ticker: <string>`
- `- Analysis Date: <YYYY-MM-DD>`
- `- Run Timestamp: <ISO-8601>`
- `- Provider: <string>`
- `- Model(s): <comma-separated>`
- `- Debate Rounds: <int>`
- `- Pipeline Version: <string>`
- `- Output Schema Version: <semver>`

## 2) Market Context Snapshot

Required bullets:

- `- Price Context: <summary>`
- `- Recent Trend: <summary>`
- `- Notable Macro/News Context: <summary or None>`

Should be concise and factual, not a recommendation.

## 3) Analyst Findings

Required subsections (heading level 3):

- `### Fundamentals`
- `### Sentiment`
- `### News`
- `### Technical`

Each subsection requires:

- `- Signal: <Bullish|Neutral|Bearish>`
- `- Confidence: <0.00-1.00>`
- `- Key Points:`
  - at least 2 bullets unless data unavailable

## 4) Debate Synthesis

Required fields:

- `- Bull Thesis: <summary>`
- `- Bear Thesis: <summary>`
- `- Main Point of Disagreement: <summary>`
- `- Debate Outcome: <Bull|Bear|Inconclusive>`
- `- Why: <summary>`

## 5) Trader Recommendation

Required fields:

- `- Action: <Buy|Overweight|Hold|Underweight|Sell>`
- `- Position Guidance: <text>`
- `- Time Horizon: <text>`
- `- Entry Considerations: <text>`
- `- Exit/Invalidation Clues: <text>`

## 6) Risk Assessment

Required fields:

- `- Volatility Risk: <Low|Medium|High>`
- `- Liquidity Risk: <Low|Medium|High>`
- `- Concentration Risk: <Low|Medium|High>`
- `- Event Risk: <Low|Medium|High>`
- `- Risk Mitigations:`
  - at least 2 bullets

## 7) Final Decision

Required fields:

- `- Final Rating: <Buy|Overweight|Hold|Underweight|Sell>`
- `- Suggested Portfolio Weight: <text>`
- `- Decision Rationale: <2-5 bullet points>`
- `- Decision Owner: <Portfolio Manager|System>`

## 8) Confidence and Failure Modes

Required fields:

- `- Overall Confidence: <0.00-1.00>`
- `- Confidence Drivers: <bullets>`
- `- Failure Modes: <bullets>`
- `- What Would Change This View: <bullets>`

## 9) Evidence and Sources

Required:

- `- Data Sources Used: <bullets>`
- `- Key Evidence Items: <bullets>`
- `- Missing Data/Unknowns: <bullets or None>`

Do not include API keys, raw credentials, or sensitive environment data.

## 10) Follow-up Questions

Required:

- 3 to 7 actionable research questions.

These are designed for future skills to pick up and extend.

## 11) Appendix (Optional)

Allowed:

- model warnings
- debug snippets
- extra tables

Not allowed:

- stack traces in main sections
- unstructured raw dumps replacing required fields

## `metadata.json` Contract

`metadata.json` is required for robust skill ingestion and should mirror key report primitives.

Minimum schema:

```json
{
  "schema_version": "1.0.0",
  "run_id": "string",
  "ticker": "NVDA",
  "analysis_date": "2026-04-29",
  "run_timestamp": "2026-04-29T15:00:00-04:00",
  "provider": "openai",
  "models": ["gpt-5.4", "gpt-5.4-mini"],
  "debate_rounds": 2,
  "final_rating": "Overweight",
  "suggested_weight": "2-3%",
  "overall_confidence": 0.74,
  "status": "success",
  "warnings": [],
  "errors": []
}
```

## Empirical Baseline from Your NVDA Terminal Run

The schema captures patterns seen in your real run output so future reports preserve useful signal.

Observed in terminal:

- final decision style included rating + weight guidance
- concise "key data the agents worked from" bullets
- debate outcome context ("bull case won")
- warning channel about model-catalog mismatch

Example lines captured:

- `Final Decision: OVERWEIGHT (BUY) — 2-3% portfolio position`
- `Key data the agents worked from: ...`
- `Bull case won the debate: ...`
- model warning notes about known model list

Schema implications:

- retain explicit `Final Rating` + `Suggested Portfolio Weight` fields
- require structured evidence bullets
- add controlled warning capture in appendix and `metadata.json`

## Optional `index.md` Daily Aggregation Contract

For batch runs, `outputs/YYYY-MM-DD/index.md` should include:

1. Date-level summary header
2. table-like bullet list of all tickers with final rating and confidence
3. top bullish and bearish convictions
4. cross-ticker risk notes
5. link list to each ticker `report.md`

This file improves portfolio review and supports cross-ticker synthesis skills.

## Parsing Rules for Future Skills

- Skills should locate sections by exact heading text.
- Skills should parse labeled bullets before falling back to free text.
- Missing required section = hard validation failure.
- Missing required field = soft failure with warning, unless critical field:
  - `Run ID`, `Ticker`, `Analysis Date`, `Final Rating`, `Overall Confidence`
- Numeric confidence fields must parse as float in `[0.0, 1.0]`.

## Validation Levels

- **Level 1 (Structure):** required headings exist and are ordered.
- **Level 2 (Fields):** required labeled bullets present.
- **Level 3 (Semantics):** enums valid, confidence parseable, no secrets leaked.
- **Level 4 (Cross-file):** `report.md` and `metadata.json` agree on core fields.

## Versioning Policy

- `Output Schema Version` follows semver.
- Breaking heading/field changes increment major.
- Additive optional fields increment minor.
- typo/clarification fixes increment patch.

Recommended initial version: `1.0.0`.

## Backward Compatibility Guidance

- keep deprecated fields for one minor cycle with note in appendix
- publish migration note in `planning/` when heading names change
- maintain stable enum vocabulary for ratings and risks

## Security and Privacy Constraints

- never emit raw API keys, tokens, or full environment dumps
- redact provider identifiers only if needed for public sharing mode
- avoid embedding local absolute paths in public report mode

## Golden Example (Minimal Conforming Snippet)

```md
# Multi-Agent-Trading-Agents Report: NVDA (2026-04-29)

## 1) Run Metadata
- Run ID: 2026-04-29-NVDA-001
- Ticker: NVDA
- Analysis Date: 2026-04-29
- Run Timestamp: 2026-04-29T15:02:11-04:00
- Provider: openai
- Model(s): gpt-5.4, gpt-5.4-mini
- Debate Rounds: 2
- Pipeline Version: 0.1.0
- Output Schema Version: 1.0.0

## 7) Final Decision
- Final Rating: Overweight
- Suggested Portfolio Weight: 2-3%
- Decision Rationale:
  - Bull thesis dominated due to AI infrastructure leadership.
  - Fundamentals remained strong despite near-term volatility risk.
- Decision Owner: Portfolio Manager
```

## Open Decisions (To Finalize Before Implementation)

- Should `report.json` be required from day one or deferred?
- Should ratings remain five-tier only, or permit `Buy (Strong)` style modifiers?
- Should `index.md` include rank ordering by confidence by default?
- Should warning capture be public by default or hidden behind debug mode?

## Implementation Note

When coding begins, this file should be treated as the source of truth for:

- report template generation
- parser logic in future skills
- validation tests for output integrity
