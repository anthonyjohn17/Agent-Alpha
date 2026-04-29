# PRD: Trading Agents SaaS Studio

## Product Vision

Build a modern SaaS web application where users can:

- discover and understand each agent in the system
- run single or multi-ticker analyses live from the UI
- watch run progress in real time
- review historical reports and performance traces
- manage provider APIs, models, and behavior settings safely

The app should feel like a polished AI operations product, not a script wrapper.

## Product Goals

1. Transform the existing script-first engine into a reusable app platform.
2. Provide live, explainable execution with clear status and output.
3. Support tenant-level customization (providers, models, runtime options).
4. Enable production deployment with enterprise-grade controls and observability.

## Non-Goals (Initial Release)

- direct brokerage execution / live trading
- social community features
- plugin marketplace for third-party agents
- advanced billing metering beyond plan-based quotas

## Target Users

- Independent traders and researchers evaluating multi-agent analyses.
- Portfolio owners who need daily repeatable research runs.
- Technical users who want model/provider configurability without code edits.
- Admin/operators managing multiple tenants or teams.

## Core User Journeys

### 1) Onboard and Configure

User signs in, creates workspace, adds API keys, picks default models/provider, and runs a first sample analysis.

### 2) Live Analysis Run

User selects ticker(s), date, and runtime settings, then launches a run and observes stage-by-stage progress with live logs/events.

### 3) Report Review and Comparison

User opens generated report(s), compares across dates/tickers, and views confidence/risk sections with structured metadata.

### 4) Admin and Policy

Admin configures organization defaults, API key policy, execution limits, and feature flags for safe operations.

## Feature Set (MVP)

1. Authentication and workspace/tenant model.
2. Dashboard with run history and quick launch.
3. Agent Gallery:
   - list of agents
   - responsibilities and outputs
   - execution role in pipeline
4. Run Builder:
   - ticker(s), date, provider, model, debate rounds
   - presets and validation
5. Live Run Console:
   - progress timeline
   - streaming events/logs
   - cancel/retry controls
6. Reports:
   - markdown rendering
   - metadata panel
   - historical list and filters
7. Settings:
   - API keys and provider credentials
   - model defaults
   - runtime constraints and feature flags
8. Admin:
   - role-based permissions
   - tenant limits (max concurrent runs, daily quota)

## Nice-to-Have (V2)

- report diff view across dates
- watchlists and scheduled runs
- alerting (email/slack/webhook)
- deeper analytics (run cost, token usage, latency per agent)

## Functional Requirements

- A user can launch and monitor a run without terminal access.
- A run can process one or many tickers.
- System captures stage status (queued/running/failed/completed/canceled).
- Generated artifacts remain compatible with existing output contract.
- Settings changes apply to subsequent runs with audit history.
- Failures are isolated per ticker and surfaced in UI.

## Non-Functional Requirements

- **Availability:** 99.9% target for API and app.
- **Performance:** first dashboard render < 2 seconds at p50.
- **Scalability:** horizontal worker scale for concurrent run demand.
- **Security:** encrypted secrets, least-privilege access, tenant isolation.
- **Observability:** traceable runs with logs/metrics/event correlation IDs.
- **Reliability:** resumable jobs and idempotent run creation.

## Data and Compliance Considerations

- Never expose raw API keys in UI or logs.
- Encrypt all secrets at rest using a managed KMS.
- Maintain immutable audit logs for settings and admin actions.
- Preserve report lineage: who ran what, when, with which config.

## Success Metrics

- Time-to-first-successful-run after signup < 10 minutes.
- >90% of runs launched through UI (not manual scripts).
- Run failure rate due to config/setup errors < 5%.
- Mean time to diagnose failed run < 10 minutes.

## Risks

- Tight coupling to current script execution model can limit scalability.
- Provider API variability can create fragile run behavior.
- Poor settings ergonomics can increase support burden.
- Streaming complexity (websocket/SSE) can degrade UX if not robust.

## Acceptance Criteria (MVP)

- Users can configure API providers from settings and run analyses live.
- Run console shows real-time lifecycle and final artifacts.
- Reports are viewable and searchable in app history.
- Tenant admins can manage policy and limits from a dedicated section.
- Core workflows are covered by integration and end-to-end tests.
