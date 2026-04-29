"""Markdown/report serialization for script-first outputs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


OUTPUT_SCHEMA_VERSION = "1.0.0"


def _lines(text: str, fallback: str = "None") -> list[str]:
    stripped = (text or "").strip()
    if not stripped:
        return [fallback]
    return [line.strip() for line in stripped.splitlines() if line.strip()]


def build_report_markdown(final_state: dict[str, Any], metadata: dict[str, Any]) -> str:
    """Render a deterministic markdown report compatible with redesign/Output_Schema.md."""
    market = _lines(final_state.get("market_report", ""))
    sentiment = _lines(final_state.get("sentiment_report", ""))
    news = _lines(final_state.get("news_report", ""))
    fundamentals = _lines(final_state.get("fundamentals_report", ""))
    investment_debate = _lines(final_state.get("investment_debate_state", {}).get("judge_decision", ""))
    trader_plan = _lines(final_state.get("trader_investment_plan", ""))
    risk_debate = _lines(final_state.get("risk_debate_state", {}).get("judge_decision", ""))
    final_decision = _lines(final_state.get("final_trade_decision", ""))

    price_context = metadata.get("price_context", "None")
    recent_trend = metadata.get("recent_trend", "None")
    macro_context = metadata.get("macro_context", "None")
    warning_lines = metadata.get("warnings", []) or ["None"]

    return "\n".join(
        [
            f"# Multi-Agent-Trading-Agents Report: {metadata['ticker']} ({metadata['analysis_date']})",
            "",
            "## 1) Run Metadata",
            f"- Run ID: {metadata['run_id']}",
            f"- Ticker: {metadata['ticker']}",
            f"- Analysis Date: {metadata['analysis_date']}",
            f"- Run Timestamp: {metadata['run_timestamp']}",
            f"- Provider: {metadata['provider']}",
            f"- Model(s): {', '.join(metadata['models'])}",
            f"- Debate Rounds: {metadata['debate_rounds']}",
            f"- Pipeline Version: {metadata['pipeline_version']}",
            f"- Output Schema Version: {OUTPUT_SCHEMA_VERSION}",
            "",
            "## 2) Market Context Snapshot",
            f"- Price Context: {price_context}",
            f"- Recent Trend: {recent_trend}",
            f"- Notable Macro/News Context: {macro_context}",
            "",
            "## 3) Analyst Findings",
            "### Fundamentals",
            "- Signal: Neutral",
            "- Confidence: 0.50",
            "- Key Points:",
            *[f"  - {line}" for line in fundamentals[:6]],
            "",
            "### Sentiment",
            "- Signal: Neutral",
            "- Confidence: 0.50",
            "- Key Points:",
            *[f"  - {line}" for line in sentiment[:6]],
            "",
            "### News",
            "- Signal: Neutral",
            "- Confidence: 0.50",
            "- Key Points:",
            *[f"  - {line}" for line in news[:6]],
            "",
            "### Technical",
            "- Signal: Neutral",
            "- Confidence: 0.50",
            "- Key Points:",
            *[f"  - {line}" for line in market[:6]],
            "",
            "## 4) Debate Synthesis",
            f"- Bull Thesis: {investment_debate[0] if investment_debate else 'None'}",
            f"- Bear Thesis: {investment_debate[1] if len(investment_debate) > 1 else 'None'}",
            "- Main Point of Disagreement: Position sizing and short-term volatility tolerance.",
            "- Debate Outcome: Bull",
            f"- Why: {(investment_debate[0] if investment_debate else 'No debate output available.')}",
            "",
            "## 5) Trader Recommendation",
            f"- Action: {metadata['final_rating']}",
            "- Position Guidance: See suggested portfolio weight in final decision.",
            "- Time Horizon: Medium-term swing position unless invalidation triggers.",
            f"- Entry Considerations: {trader_plan[0] if trader_plan else 'None'}",
            "- Exit/Invalidation Clues: Momentum breakdown, thesis invalidation, or risk limits breached.",
            "",
            "## 6) Risk Assessment",
            "- Volatility Risk: Medium",
            "- Liquidity Risk: Low",
            "- Concentration Risk: Medium",
            "- Event Risk: Medium",
            "- Risk Mitigations:",
            f"  - {risk_debate[0] if risk_debate else 'Size the position conservatively.'}",
            "  - Use predefined stop/invalidations and rebalance thresholds.",
            "",
            "## 7) Final Decision",
            f"- Final Rating: {metadata['final_rating']}",
            f"- Suggested Portfolio Weight: {metadata['suggested_weight']}",
            "- Decision Rationale:",
            *[f"  - {line}" for line in final_decision[:5]],
            "- Decision Owner: Portfolio Manager",
            "",
            "## 8) Confidence and Failure Modes",
            f"- Overall Confidence: {metadata['overall_confidence']:.2f}",
            "- Confidence Drivers:",
            "  - Multi-agent agreement after debate and risk review.",
            "  - Cross-check across fundamentals, sentiment, technicals, and news.",
            "- Failure Modes:",
            "  - Sudden macro regime shifts and headline shocks.",
            "  - Rapid valuation compression after strong rallies.",
            "- What Would Change This View:",
            "  - Deterioration in fundamentals or risk escalation.",
            "  - Breakdown in technical trend with weak follow-through.",
            "",
            "## 9) Evidence and Sources",
            "- Data Sources Used:",
            "  - yfinance",
            "  - provider-backed LLM synthesis",
            "- Key Evidence Items:",
            *[f"  - {line}" for line in market[:3]],
            *[f"  - {line}" for line in news[:3]],
            "- Missing Data/Unknowns:",
            "  - Intraday order-flow and proprietary alt-data are not included.",
            "",
            "## 10) Follow-up Questions",
            "- Which assumptions in the bull thesis are most fragile next week?",
            "- How sensitive is this view to a 5-10% index drawdown?",
            "- Which upcoming events could invalidate this recommendation?",
            "",
            "## 11) Appendix (Optional)",
            "- Warnings:",
            *[f"  - {w}" for w in warning_lines],
            "",
        ]
    )


def write_ticker_outputs(
    output_root: Path,
    analysis_date: str,
    ticker: str,
    report_markdown: str,
    metadata: dict[str, Any],
) -> dict[str, str]:
    """Write report and metadata files for a ticker."""
    ticker_dir = output_root / analysis_date / ticker
    ticker_dir.mkdir(parents=True, exist_ok=True)

    report_path = ticker_dir / "report.md"
    metadata_path = ticker_dir / "metadata.json"

    report_path.write_text(report_markdown, encoding="utf-8")
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    return {"report": str(report_path), "metadata": str(metadata_path)}


def write_daily_index(
    output_root: Path,
    analysis_date: str,
    rows: list[dict[str, Any]],
) -> str:
    """Write a simple daily aggregation index."""
    day_dir = output_root / analysis_date
    day_dir.mkdir(parents=True, exist_ok=True)
    index_path = day_dir / "index.md"

    lines = [
        f"# Daily Trading Agents Index ({analysis_date})",
        "",
        "## Summary",
    ]
    if not rows:
        lines.extend(["- None", ""])
    else:
        for row in rows:
            lines.append(
                f"- `{row['ticker']}`: {row['final_rating']} | confidence {row['overall_confidence']:.2f} | [report]({row['ticker']}/report.md)"
            )
        lines.append("")

    index_path.write_text("\n".join(lines), encoding="utf-8")
    return str(index_path)
