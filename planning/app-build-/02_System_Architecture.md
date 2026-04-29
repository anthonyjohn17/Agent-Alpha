# System Architecture Spec: Trading Agents SaaS Studio

## Architecture Goals

- Preserve the existing `tradingagents/` core domain logic.
- Add an application platform layer for UI/API/worker orchestration.
- Enforce tenant-aware security, settings isolation, and observability.
- Allow provider/model/runtime extension without destabilizing core flows.

## High-Level Topology

1. **Web App (Frontend)**
   - SaaS dashboard, run builder, live console, reports, settings/admin.
2. **API Service (Backend)**
   - auth, tenant/workspace, run lifecycle, settings, report retrieval.
3. **Worker Service**
   - executes runs asynchronously using current orchestration core.
4. **Message Broker / Queue**
   - decouples API from long-running execution.
5. **Primary DB**
   - tenants, users, runs, settings, audit logs, report metadata.
6. **Object Storage**
   - report files and artifacts (optionally mirrored from `outputs/` model).
7. **Realtime Channel**
   - SSE/WebSocket stream for live run state and logs.
8. **Observability Stack**
   - logs, metrics, traces, alerts.

## Core Architectural Patterns (Skill-Informed)

- **SRP + RDD:** separate auth, run orchestration, settings, reporting services.
- **DIP:** worker depends on interfaces for provider/model integrations.
- **Adapter Pattern:** normalize provider-specific LLM clients into common contracts.
- **Strategy Pattern:** pluggable execution profiles (speed, depth, cost mode).
- **Observer/Event Pattern:** publish run events for UI streaming and audit.

## Service Boundaries

### API Service Modules

- `AuthModule` (session/JWT, roles)
- `TenantModule` (workspace lifecycle, membership)
- `RunModule` (create/start/cancel/retry/status)
- `SettingsModule` (provider credentials, model defaults, flags)
- `ReportModule` (list/get/report metadata and markdown payload)
- `AdminModule` (quotas, policy, audit access)

### Worker Modules

- `RunDispatcher` (consumes queue jobs)
- `RunExecutor` (invokes orchestration pipeline)
- `ArtifactPublisher` (stores outputs and metadata)
- `RunEventPublisher` (streams lifecycle events)
- `FailureClassifier` (normalizes error categories)

## Data Model (Conceptual)

- `Tenant`
- `User`
- `Membership` (role per tenant)
- `ApiCredential` (encrypted secret references only)
- `RunJob` (input config, status, timestamps, owner)
- `RunTickerResult` (per ticker status/error/artifacts)
- `ReportArtifact` (storage pointer, schema version, metadata)
- `TenantSettings` (runtime defaults + policy)
- `AuditEvent` (actor, action, before/after, trace id)

## Run Lifecycle

1. User submits run config in UI.
2. API validates config + tenant policy + required credentials.
3. API creates `RunJob` and enqueues message.
4. Worker dequeues and emits `RUN_STARTED`.
5. Worker executes per ticker and emits granular stage events.
6. Artifacts are stored and metadata persisted.
7. Worker emits completion/failure events.
8. UI updates live console and persists final run state.

## Deployment View

- Frontend: static hosting + CDN.
- API and Worker: containerized services (same codebase, separate process roles).
- Queue: managed broker.
- DB: managed relational database.
- Storage: managed object store.
- Secrets: managed secret vault + KMS.
- Observability: centralized log/trace/metric platform.

## Security Model

- Tenant isolation enforced at service and query layer.
- RBAC roles: `owner`, `admin`, `editor`, `viewer`.
- Secrets encrypted, rotated, and redacted in output.
- Rate limiting per user and per tenant.
- Signed artifact URLs with short TTL.

## Reliability and Recovery

- Idempotent run submission via idempotency key.
- Retries for transient provider/network failures.
- Dead-letter queue for persistent failures.
- Run resume support (aligned with existing checkpoint concepts).
- Circuit breaker around provider calls.

## Technology Recommendation

- **Frontend:** Next.js + TypeScript + Tailwind + component system.
- **Backend API:** FastAPI (or NestJS) with async support.
- **Worker:** Python worker sharing `tradingagents/` execution code.
- **Queue:** Redis Streams / RabbitMQ / managed queue.
- **DB:** PostgreSQL.
- **Realtime:** SSE first (simpler infra), optional WebSocket upgrade.

## Why This Fits Current Repo

- Existing Python orchestration remains the domain heart.
- Report schema and output contracts are already strong.
- System evolves from script-first to app-first with minimal core churn.
- New boundaries keep enterprise concerns separate from agent logic.
