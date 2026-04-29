"""Script-first entrypoint for running one or many ticker analyses."""

from __future__ import annotations

import argparse
import os
from datetime import date, datetime
from pathlib import Path
from typing import Any

from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.reporting import (
    build_report_markdown,
    write_daily_index,
    write_ticker_outputs,
)
from tradingagents.utils import normalize_ticker_symbol


def _load_env() -> None:
    """Load local .env files when python-dotenv is available."""
    try:
        from dotenv import load_dotenv

        load_dotenv(".env")
        load_dotenv(".env.enterprise")
    except Exception:
        # Keep script functional even if dotenv is unavailable.
        pass


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run trading-agent orchestration and write markdown reports."
    )
    parser.add_argument("--ticker", type=str, help="Single ticker, e.g. NVDA")
    parser.add_argument(
        "--tickers",
        type=str,
        help="Comma-separated tickers, e.g. NVDA,MSFT,AAPL",
    )
    parser.add_argument(
        "--date",
        dest="analysis_date",
        type=str,
        default=date.today().isoformat(),
        help="Analysis date in YYYY-MM-DD (default: today)",
    )
    parser.add_argument("--provider", type=str, default="openai")
    parser.add_argument("--deep-model", type=str, default="gpt-5.4")
    parser.add_argument("--quick-model", type=str, default="gpt-5.4-mini")
    parser.add_argument("--debate-rounds", type=int, default=1)
    parser.add_argument(
        "--output-dir",
        type=str,
        default="outputs",
        help="Output folder root (default: outputs)",
    )
    parser.add_argument(
        "--checkpoint",
        action="store_true",
        help="Enable LangGraph checkpoint resume",
    )
    return parser.parse_args()


def _collect_tickers(single: str | None, many: str | None) -> list[str]:
    raw: list[str] = []
    if single:
        raw.append(single)
    if many:
        raw.extend([part for part in many.split(",") if part.strip()])
    if not raw:
        raise ValueError("Provide --ticker or --tickers.")

    deduped: list[str] = []
    seen: set[str] = set()
    for ticker in raw:
        normalized = normalize_ticker_symbol(ticker)
        if normalized and normalized not in seen:
            deduped.append(normalized)
            seen.add(normalized)
    if not deduped:
        raise ValueError("No valid ticker symbols were provided.")
    return deduped


def _build_config(args: argparse.Namespace, output_root: Path) -> dict[str, Any]:
    config = DEFAULT_CONFIG.copy()
    config["llm_provider"] = args.provider
    config["deep_think_llm"] = args.deep_model
    config["quick_think_llm"] = args.quick_model
    config["max_debate_rounds"] = args.debate_rounds
    config["checkpoint_enabled"] = args.checkpoint
    # Keep internal logs under outputs so generated artifacts stay together.
    config["results_dir"] = str(output_root / "_internal_logs")
    config["data_cache_dir"] = str(output_root / "_cache")
    return config


def _metadata_for_run(
    ticker: str,
    args: argparse.Namespace,
    final_rating: str,
    warnings: list[str] | None = None,
) -> dict[str, Any]:
    now = datetime.now().astimezone().isoformat(timespec="seconds")
    run_id = f"{args.analysis_date}-{ticker}-{now[-8:].replace(':', '')}"
    return {
        "schema_version": "1.0.0",
        "run_id": run_id,
        "ticker": ticker,
        "analysis_date": args.analysis_date,
        "run_timestamp": now,
        "provider": args.provider,
        "models": [args.deep_model, args.quick_model],
        "debate_rounds": args.debate_rounds,
        "pipeline_version": "0.1.0",
        "final_rating": final_rating,
        "suggested_weight": "2-3%",
        "overall_confidence": 0.50,
        "status": "success",
        "warnings": warnings or [],
        "errors": [],
    }


def main() -> int:
    args = _parse_args()
    _load_env()
    output_root = Path(args.output_dir)
    output_root.mkdir(parents=True, exist_ok=True)

    tickers = _collect_tickers(args.ticker, args.tickers)
    config = _build_config(args, output_root)
    graph = TradingAgentsGraph(debug=False, config=config)

    rows: list[dict[str, Any]] = []
    for ticker in tickers:
        try:
            final_state, decision = graph.propagate(ticker, args.analysis_date)
            metadata = _metadata_for_run(ticker, args, decision)
            report = build_report_markdown(final_state, metadata)
            paths = write_ticker_outputs(
                output_root=output_root,
                analysis_date=args.analysis_date,
                ticker=ticker,
                report_markdown=report,
                metadata=metadata,
            )
            rows.append(
                {
                    "ticker": ticker,
                    "final_rating": metadata["final_rating"],
                    "overall_confidence": metadata["overall_confidence"],
                    "paths": paths,
                }
            )
            print(f"[ok] {ticker}: {metadata['final_rating']} -> {paths['report']}")
        except Exception as exc:
            print(f"[error] {ticker}: {exc}")
            rows.append(
                {
                    "ticker": ticker,
                    "final_rating": "Error",
                    "overall_confidence": 0.0,
                    "error": str(exc),
                }
            )

    index_path = write_daily_index(output_root, args.analysis_date, rows)
    print(f"[done] daily index: {index_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
