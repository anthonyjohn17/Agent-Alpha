# Agent-Alpha

Script-first multi-agent trading analysis orchestrator with deterministic report outputs.

Agent-Alpha runs a LangGraph pipeline for one or many tickers, then writes stable markdown + JSON artifacts designed for both human review and machine ingestion.

This repository is for research and educational use only. It is not financial advice.

## What Changed In The Refactor

- Runtime consolidated around `scripts/run_today.py` for daily usage.
- Graph internals split into focused modules (`setup`, `propagation`, `conditional_logic`, `reflection`).
- Reporting standardized in `tradingagents/reporting.py` with stable section headings.
- Optional checkpoint/resume support added for interrupted runs.
- Decision memory loop now supports deferred outcome resolution and reflection reuse.
- Structured decision agents now feed a consistent five-tier rating scale.

## Quickstart

### 1) Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install .
```

### 2) Configure environment

```bash
cp .env.example .env
```

Set at least one provider key (for example `OPENAI_API_KEY`).

- `OPENAI_API_KEY`
- `GOOGLE_API_KEY`
- `ANTHROPIC_API_KEY`
- provider-specific keys for OpenAI-compatible backends as needed

### 3) Run the orchestrator

Single ticker (today):

```bash
python scripts/run_today.py --ticker NVDA
```

Multiple tickers (today):

```bash
python scripts/run_today.py --tickers NVDA,MSFT,AAPL
```

Custom date:

```bash
python scripts/run_today.py --tickers NVDA,AMD --date 2026-04-29
```

Enable checkpoint resume:

```bash
python scripts/run_today.py --ticker NVDA --checkpoint
```

## Runtime Options

`scripts/run_today.py` supports:

- `--ticker`
- `--tickers`
- `--date` (default: local today)
- `--provider` (default: `openai`)
- `--deep-model` (default: `gpt-5.4`)
- `--quick-model` (default: `gpt-5.4-mini`)
- `--debate-rounds` (default: `1`)
- `--output-dir` (default: `outputs`)
- `--checkpoint` (resume from LangGraph checkpoints)

Provider support in the current LLM client factory:

- OpenAI-compatible: `openai`, `xai`, `deepseek`, `qwen`, `glm`, `ollama`, `openrouter`
- Native adapters: `google`, `anthropic`, `azure`

## Output Layout

```text
outputs/
  YYYY-MM-DD/
    index.md
    <TICKER>/
      report.md
      metadata.json
  _internal_logs/
  _cache/
```

- `report.md` follows the schema contract in `planning/Output_Schema.md`.
- `metadata.json` stores parseable run metadata (run ID, provider, models, final rating, confidence, status).
- `index.md` aggregates per-ticker outcomes for the day.

## Decision Memory Loop

Agent-Alpha keeps an append-only decision log and updates prior pending decisions once outcome data is available:

- computes raw return and alpha vs SPY after holding window
- generates compact reflection text
- injects lessons into future runs (same ticker and cross-ticker context)

This creates a lightweight learning loop without training new model weights.

## Project Structure

- `tradingagents/`: agents, graph orchestration, LLM clients, reporting, utilities
- `scripts/`: script entrypoints and smoke checks
- `tests/`: unit/integration/smoke tests
- `planning/`: product/technical docs and output contract
- `research/`: research notes and run analysis artifacts

## Development

Run all tests:

```bash
pytest
```

Run focused regression tests for core refactor guarantees:

```bash
pytest tests/test_output_schema.py tests/test_ticker_symbol_handling.py
```

Run structured-output smoke test against a real provider:

```bash
python scripts/smoke_structured_output.py openai
```

## License

Apache-2.0 (`LICENSE`).

## Near-Term Roadmap

- Improve confidence calibration and risk quantification fields.
- Expand structured evidence extraction from analyst outputs.
- Add portfolio-level synthesis across many daily ticker reports.
