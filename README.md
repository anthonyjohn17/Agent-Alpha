# Multi-Agent-Trading-Agents

Script-first trading-agents orchestrator for generating comprehensive daily markdown reports per ticker.

## What This Repo Does

- Runs a multi-agent analysis pipeline for one or many tickers.
- Defaults to today's date unless overridden.
- Writes standardized reports to `outputs/YYYY-MM-DD/<TICKER>/report.md`.
- Writes machine-readable metadata to `outputs/YYYY-MM-DD/<TICKER>/metadata.json`.
- Optionally aggregates a daily summary at `outputs/YYYY-MM-DD/index.md`.

This repository is for research and educational use only. It is not financial advice.

## Quickstart

### 1) Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install .
```

### 2) Configure API keys

Copy and edit `.env.example`:

```bash
cp .env.example .env
```

Set at least one provider key (for example `OPENAI_API_KEY`).

### 3) Run

Single ticker, today:

```bash
python scripts/run_today.py --ticker NVDA
```

Multiple tickers, today:

```bash
python scripts/run_today.py --tickers NVDA,MSFT,AAPL
```

Custom date:

```bash
python scripts/run_today.py --tickers NVDA,AMD --date 2026-04-29
```

## Output Layout

```text
outputs/
  2026-04-29/
    index.md
    NVDA/
      report.md
      metadata.json
    MSFT/
      report.md
      metadata.json
```

Report structure follows `redesign/Output_Schema.md` to keep future skill ingestion stable.

## Main Runtime Options

`scripts/run_today.py` supports:

- `--ticker`
- `--tickers`
- `--date` (defaults to local today)
- `--provider` (default: `openai`)
- `--deep-model` (default: `gpt-5.4`)
- `--quick-model` (default: `gpt-5.4-mini`)
- `--debate-rounds` (default: `1`)
- `--output-dir` (default: `outputs`)
- `--checkpoint` (enable resume from LangGraph checkpoints)

## Project Structure

- `tradingagents/`: core agent graph, orchestration, dataflows, LLM clients.
- `scripts/`: script entrypoints for batch and daily execution.
- `tests/`: unit/integration/smoke tests.
- `redesign/`: planning docs for simplification, output schema, and future skills.

## Development

Run tests:

```bash
pytest
```

Focused tests:

```bash
pytest tests/test_output_schema.py tests/test_ticker_symbol_handling.py
```

## Legal and Attribution

- License is Apache-2.0 (`LICENSE`).
- Historical project lineage and prior contributions are retained in `CHANGELOG.md`.

## Roadmap (Near-Term)

- Improve report confidence scoring and risk quantification.
- Add stronger structured evidence extraction in report sections.
- Add skills that synthesize across many generated reports.
