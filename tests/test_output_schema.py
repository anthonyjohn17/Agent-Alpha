import pytest

from tradingagents.reporting import build_report_markdown


@pytest.mark.unit
def test_report_contains_required_headings():
    final_state = {
        "market_report": "Trend is positive.",
        "sentiment_report": "Sentiment remains constructive.",
        "news_report": "No major negative catalysts.",
        "fundamentals_report": "Revenue growth remains strong.",
        "investment_debate_state": {"judge_decision": "Bull case stronger than bear case."},
        "trader_investment_plan": "Prefer staged entries.",
        "risk_debate_state": {"judge_decision": "Manage position size due to volatility."},
        "final_trade_decision": "Final rating: Overweight. Suggested portfolio weight: 2-3%.",
    }
    metadata = {
        "run_id": "2026-04-29-NVDA-001",
        "ticker": "NVDA",
        "analysis_date": "2026-04-29",
        "run_timestamp": "2026-04-29T15:02:11-04:00",
        "provider": "openai",
        "models": ["gpt-5.4", "gpt-5.4-mini"],
        "debate_rounds": 2,
        "pipeline_version": "0.1.0",
        "final_rating": "Overweight",
        "suggested_weight": "2-3%",
        "overall_confidence": 0.5,
        "warnings": [],
    }

    report = build_report_markdown(final_state, metadata)

    assert "# Multi-Agent-Trading-Agents Report: NVDA (2026-04-29)" in report
    assert "## 1) Run Metadata" in report
    assert "## 3) Analyst Findings" in report
    assert "## 7) Final Decision" in report
    assert "## 9) Evidence and Sources" in report
    assert "## 10) Follow-up Questions" in report
