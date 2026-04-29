# Product Overview: Trading Agents

This document summarizes the system behavior, operating model, and constraints of the Trading Agents project in product-spec language.

---

## Core Concept: Simulated Multi-Agent Investment Workflow

At its core, this project is a **multi-agent LLM framework** that mirrors internal hedge-fund workflows. Instead of a single algorithm producing an output, specialized roles **interact, debate, and collaborate** before a final decision is produced.

A single run launches a miniature firm composed of:

* A fundamentals analyst
* A sentiment analyst
* A news analyst
* A technical analyst
* A bullish researcher
* A bearish researcher
* A trader
* A risk management team
* A portfolio manager

Each one is powered by an LLM, and they all **talk to each other**, forming a layered decision-making pipeline.


---

## System Workflow

### 1. Analyst Layer (Parallel Intelligence)

The system starts with four analyst agents running simultaneously:

* **Fundamentals analyst**
  Pulls company filings, performs ratio analysis, and estimates intrinsic value

* **Sentiment analyst**
  Scrapes platforms like Reddit and X to measure public mood

* **News analyst**
  Tracks macroeconomic signals and breaking events

* **Technical analyst**
  Runs indicators like MACD, RSI, and Bollinger Bands

Each produces a **full written report**, and importantly, the system does *not* merge them into a single output. Their disagreements are treated as valuable signal.

---

### 2. Research Layer (Structured Conflict)

Two researcher agents are introduced:

* One is **structurally bullish**
* The other is **structurally bearish**

They take analyst reports and **debate across multiple rounds**. Debate duration is configurable. They cite specific data points and actively challenge each other’s conclusions.

The system intentionally **manufactures disagreement**, because that tension produces stronger reasoning.

---

### 3. Decision Layer

After the debate:

* The **trader agent** reads everything and decides:

  * Timing
  * Position size
  * Trade proposal

* The **risk management team** evaluates:

  * Volatility
  * Liquidity

* The **portfolio manager** makes the final call:

  * Approve → trade goes to simulated exchange
  * Reject → process ends with a written explanation

---

## Orchestration Engine

The system runs on LangGraph, where:

* Each agent is a node in a directed graph
* Each transition is checkpointed
* runs can resume if they stop midway

There is also a **persistent decision log**:

* Every trade decision is stored in markdown
* On future runs:

  * The system retrieves past results
  * Compares performance against SPY
  * Computes alpha
  * Generates a reflection on what worked or failed
  * Injects that insight into the next decision

This enables the system to **learn from prior decision history**.

---

## Positioning Relative to Other Trading Systems

Most trading frameworks fall into two camps:

1. **Rigid rule-based systems**
   Example: moving averages, mechanical triggers

2. **Black-box ML models**
   Output: buy/sell signals with no explanation

This project sits right in the middle.

Each decision is **transparent and auditable**:

* analyst reports are readable
* bull vs bear debate outcomes are reviewable
* proposed/rejected trade rationale is explicit

The system does not only output recommendations; it also **shows its reasoning trail**.

---

## Runtime Setup and Compatibility

Current setup flow:

1. Clone the repo
2. Create a Python environment
3. Install dependencies
4. Set API key
5. Run CLI (legacy runtime surface)

The CLI currently supports:

* Stock ticker
* Analysis date
* LLM provider
* Number of debate rounds

It supports a wide range of models:

* OpenAI GPT
* Google Gemini
* Anthropic Claude
* xAI Grok
* DeepSeek
* Qwen
* TLM
* OpenRouter
* Ollama (local models)

---

## Recent Release Notes (v0.2.4)

The latest release (April 25) introduced major upgrades:

* **Structured output decision agents**
  Uses Pydantic schemas for clean parsing and fewer failures

* **New providers added**
  DeepSeek, Qwen, GLM, Azure OpenAI

* **Docker support**
  With multi-stage builds

* **Five-tier rating system**

  * Buy
  * Overweight
  * Hold
  * Underweight
  * Sell

This rating is now consistent across researchers, portfolio manager, and logs.

---

## Primary User Segments

This system is suitable for:

* **Quant researchers**
  A clean reference for multi-agent LLM system design

* **Hobbyist traders**
  Can spin up AI-driven analysis in ~10 minutes

* **Fintech founders**
  A forkable, extensible foundation

* **Indie hackers**
  One of the clearest real-world examples of agent orchestration

---

## Tradeoffs and Constraints

There are some important caveats:

* **Token costs add up quickly**
  Each run involves:

  * 4 analysts
  * Multiple debate rounds
  * Trader + portfolio manager

* **Not financial advice**
  The authors explicitly warn against blindly following outputs

* **No live trading integration**
  The exchange is simulated (backtesting only)

---

## Product Summary

From a product architecture perspective, this project serves as a **reference pattern for multi-agent LLM systems**:

* Modular
* Transparent
* Debate-driven
* Stateful
* Auditable

It functions both as a trading-analysis tool and as a **reference architecture** for multi-agent reasoning systems.

---
