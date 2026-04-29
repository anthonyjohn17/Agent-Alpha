# Product Overview: Agent Alpha

This document summarizes the system behavior, operating model, and constraints of the Agent Alpha project in product-spec language.

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
* A research manager
* A trader
* A risk management debate team
* A portfolio manager

Each one is powered by an LLM, and they all **talk to each other**, forming a layered decision-making pipeline.

---

## System Workflow

### 1. Analyst Layer (Parallel Intelligence)

The system starts with four analyst agents:

* **Fundamentals analyst**  
  Pulls company financial statements and fundamentals to estimate underlying business strength

* **Sentiment analyst**  
  Extracts public mood and positioning signal

* **News analyst**  
  Tracks macro and company-specific developments

* **Technical analyst**  
  Interprets price action and indicator-based trend behavior

Each produces a **full written report**, and importantly, the system does *not* merge them into one early “average.” Their disagreements are treated as valuable signal.

---

### 2. Research Layer (Structured Conflict)

Two researcher agents are introduced:

* One is **structurally bullish**
* The other is **structurally bearish**

They take analyst reports and **debate across multiple rounds**. Debate duration is configurable. They cite data points and actively challenge each other’s conclusions.

The system intentionally **manufactures disagreement**, because that tension often produces stronger reasoning.

---

### 3. Decision Layer

After the debate:

* The **research manager** synthesizes outputs into an investment plan
* The **trader agent** turns that plan into a transaction proposal
* The **risk debate team** pressure-tests exposure and downside
* The **portfolio manager** makes the final call

Final recommendations now align to a consistent five-tier scale:

* Buy
* Overweight
* Hold
* Underweight
* Sell

---

## Orchestration Engine

The system runs on LangGraph, where:

* Each agent is a node in a directed graph
* Routing logic controls debate and risk discussion flow
* Runs can be checkpointed and resumed when enabled

There is also a **persistent decision log**:

* Every final trade decision is stored in markdown
* On future runs:
  * The system resolves pending entries with realized return
  * Compares outcome against SPY to compute alpha
  * Generates a concise reflection on what worked or failed
  * Injects that lesson into subsequent runs

This enables the system to **learn from prior decision history**.

---

## Output Contract and Runtime Surface (Refactor Update)

The runtime is now script-first around `scripts/run_today.py`.

Per ticker, the system writes:

* `outputs/YYYY-MM-DD/<TICKER>/report.md`
* `outputs/YYYY-MM-DD/<TICKER>/metadata.json`

For batch runs, it also writes:

* `outputs/YYYY-MM-DD/index.md`

It supports:

* Single or multi-ticker runs (`--ticker`, `--tickers`)
* Date override (`--date`)
* Provider and model selection (`--provider`, `--deep-model`, `--quick-model`)
* Debate rounds (`--debate-rounds`)
* Checkpoint resume (`--checkpoint`)

Supported providers include OpenAI, Google, Anthropic, xAI, DeepSeek, Qwen, GLM, OpenRouter, Ollama, and Azure.

---

## Positioning Relative to Other Trading Systems

Most trading frameworks fall into two camps:

1. **Rigid rule-based systems**  
   Example: moving averages, mechanical triggers

2. **Black-box ML models**  
   Output: buy/sell signals with limited explanation

This project sits in the middle.

Each decision is **transparent and auditable**:

* analyst reports are readable
* bull vs bear debate outcomes are reviewable
* trader/risk/portfolio rationale is explicit
* report and metadata outputs are standardized

The system does not only output recommendations; it also **shows its reasoning trail**.

---

## Primary User Segments

This system is suitable for:

* **Quant researchers**  
  A practical reference for multi-agent LLM system design

* **Hobbyist traders**  
  Structured AI-driven analysis with reproducible outputs

* **Fintech founders/builders**  
  A forkable, extensible architecture

* **Agent engineers**  
  A concrete example of debate-driven orchestration with memory

---

## Tradeoffs and Constraints

There are important caveats:

* **Token and latency costs can add up quickly** across analysts, debates, and decision layers
* **Not financial advice** and not a substitute for professional fiduciary judgment
* **No live trading integration** in the current architecture
* **Output quality remains model/provider dependent**

---

## Product Summary

From a product architecture perspective, this project serves as a **reference pattern for multi-agent LLM systems**:

* Modular
* Transparent
* Debate-driven
* Stateful
* Auditable

It functions both as a trading-analysis tool and as a **reference architecture** for resilient multi-agent reasoning systems.
