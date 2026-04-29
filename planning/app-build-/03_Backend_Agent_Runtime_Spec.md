# Backend + Agent Runtime Technical Spec

## Purpose

Define the backend contracts and runtime model needed to execute trading-agent runs from a SaaS UI with enterprise-grade reliability.

## API Surface (MVP)

### Auth + Tenant

- `POST /auth/login`
- `POST /auth/logout`
- `GET /me`
- `GET /tenants/:tenantId`
- `GET /tenants/:tenantId/members`

### Runs

- `POST /tenants/:tenantId/runs`
- `GET /tenants/:tenantId/runs`
- `GET /tenants/:tenantId/runs/:runId`
- `POST /tenants/:tenantId/runs/:runId/cancel`
- `POST /tenants/:tenantId/runs/:runId/retry`
- `GET /tenants/:tenantId/runs/:runId/events` (SSE)

### Reports

- `GET /tenants/:tenantId/reports`
- `GET /tenants/:tenantId/reports/:reportId`
- `GET /tenants/:tenantId/reports/:reportId/content`

### Settings + Credentials

- `GET /tenants/:tenantId/settings`
- `PATCH /tenants/:tenantId/settings`
- `POST /tenants/:tenantId/credentials`
- `PATCH /tenants/:tenantId/credentials/:credentialId`
- `DELETE /tenants/:tenantId/credentials/:credentialId`

### Admin

- `GET /tenants/:tenantId/audit-events`
- `PATCH /tenants/:tenantId/policies`
- `GET /tenants/:tenantId/usage`

## Run Creation Contract

Request shape:

- `tickers: string[]`
- `date?: string` (defaults to today)
- `provider?: string`
- `deepModel?: string`
- `quickModel?: string`
- `debateRounds?: number`
- `executionPreset?: "balanced" | "fast" | "deep"`
- `idempotencyKey?: string`

Validation rules:

- deduplicate tickers and normalize casing
- enforce tenant quota and concurrent run limits
- verify required credentials for selected provider
- ensure model selection is allowed by tenant policy

## Runtime States

Run-level states:

- `queued`
- `starting`
- `running`
- `partial_success`
- `completed`
- `failed`
- `canceled`

Ticker-level states:

- `pending`
- `running`
- `completed`
- `failed`

## Event Stream Schema

Common fields:

- `eventId`
- `runId`
- `tenantId`
- `type`
- `timestamp`
- `traceId`

Event types:

- `RUN_QUEUED`
- `RUN_STARTED`
- `TICKER_STARTED`
- `STAGE_STARTED`
- `STAGE_COMPLETED`
- `TICKER_COMPLETED`
- `TICKER_FAILED`
- `RUN_COMPLETED`
- `RUN_FAILED`
- `RUN_CANCELED`

## Worker Execution Design

1. Load run job and tenant settings snapshot.
2. Resolve credential references from secure vault.
3. Build execution context for orchestration core.
4. Execute ticker loop with per-ticker error isolation.
5. Persist artifacts and publish event stream updates.
6. Finalize run summary and metrics.

## Integration With Existing Core

Use an adapter layer instead of calling scripts directly:

- `OrchestrationRunner` interface:
  - `run_single_ticker(config) -> TickerResult`
  - `run_multi_ticker(config) -> RunResult`

Concrete adapters:

- `ScriptCompatibleRunner` (initial bridge)
- `NativeModuleRunner` (preferred long-term direct integration)

This follows DIP and allows migration without breaking external contracts.

## Data Persistence Expectations

- store run request, normalized config, and settings snapshot
- store per-ticker outputs and errors
- persist artifact metadata with schema version
- keep immutable audit records for administrative actions

## Security and Compliance Controls

- credentials stored encrypted; API returns masked values only
- tenant-scoped data access middleware on every endpoint
- action-level authorization checks for settings/admin endpoints
- redact sensitive fields in logs and event payloads

## Observability Requirements

- structured logs with `tenantId`, `runId`, `traceId`
- metrics:
  - run duration p50/p95
  - failure rates by provider/model
  - queue depth and worker throughput
- traces from request -> queue -> worker -> artifact persist

## Testing Strategy

- unit tests for validation, policy checks, and state transitions
- integration tests for run creation -> queue -> completion
- contract tests for event stream payload shape
- failure injection tests (provider timeout, invalid key, queue issues)

## Open Decisions

- final backend framework (FastAPI vs NestJS) based on team preference
- queue technology choice based on hosting environment
- report storage strategy: DB blob vs object storage URL pointer
