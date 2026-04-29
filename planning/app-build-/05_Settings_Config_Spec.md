# Settings and Customization Spec

## Purpose

Define a robust settings system that lets users customize APIs, models, runtime behavior, and platform controls safely in a SaaS environment.

## Configuration Domains

1. Provider Credentials
2. Model Selection Defaults
3. Runtime Execution Defaults
4. Safety + Policy Guardrails
5. Feature Flags
6. Notification Preferences (V2)

## Multi-Level Settings Hierarchy

Priority order (highest to lowest):

1. Per-run overrides
2. User personal defaults
3. Tenant defaults
4. System defaults

Resolution behavior:

- Effective config is computed at run start and frozen as a run snapshot.
- Snapshot is persisted for reproducibility and auditability.

## Provider Credentials

Credential types:

- OpenAI API key
- Anthropic API key
- Azure OpenAI endpoint/key
- future providers via adapter model

Rules:

- secrets are write-only (never retrievable in full)
- UI always displays masked values
- rotation flow supports "add new -> validate -> activate"
- each credential has health check status and last validation timestamp

## Model and Runtime Defaults

Config fields:

- `defaultProvider`
- `defaultDeepModel`
- `defaultQuickModel`
- `defaultDebateRounds`
- `defaultExecutionPreset`
- `maxTickersPerRun` (tenant policy)
- `maxConcurrentRuns` (tenant policy)

## Safety and Policy Controls

- block disallowed models/providers by tenant policy
- enforce per-role capabilities (who can edit credentials/policies)
- require re-authentication for sensitive changes
- immutable audit event creation on every settings mutation

## Feature Flags

Flag categories:

- `ui.experimental`
- `runtime.experimental`
- `agent.experimental`

Rules:

- flags default off
- tenant-scoped rollout with optional percentage rollout (later)
- each flag includes owner, rationale, and expiration/review date

## Customization UX Requirements

- Settings grouped by clear tabs:
  - Credentials
  - Models
  - Runtime
  - Policies
  - Experimental
- "Effective settings preview" before save
- "Impact warning" for changes affecting future runs
- one-click "restore tenant defaults" for user-level overrides

## API Contracts (Conceptual)

- `GET /settings/effective?scope=runPreview`
- `PATCH /settings/user`
- `PATCH /settings/tenant`
- `POST /settings/credentials/validate`
- `POST /settings/credentials/rotate`
- `GET /settings/audit-log`

## Data Model (Conceptual)

- `Credential` (encrypted reference, provider, status)
- `UserSettings`
- `TenantSettings`
- `TenantPolicy`
- `FeatureFlag`
- `SettingsAuditEvent`

## Validation and Error Handling

- validate provider/model compatibility pre-save
- validate credential format + test connectivity
- reject unsafe policy changes that violate system invariants
- return field-level errors with deterministic error codes

## Enterprise Controls

- optional SSO-enforced tenant mode
- IP allowlist support (future)
- policy lock mode where only org owner can mutate sensitive settings
- exportable settings audit report for compliance review

## Test Requirements

- unit tests for merge/resolution logic across hierarchy levels
- integration tests for credential rotation and validation flow
- permission tests across roles for sensitive settings endpoints
- regression tests for event/audit emission completeness
