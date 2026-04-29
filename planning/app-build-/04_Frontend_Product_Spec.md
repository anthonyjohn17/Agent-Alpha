# Frontend Product + UX Spec (SaaS Style)

## Experience Goals

- Premium SaaS look and feel (clean hierarchy, fast interactions, strong typography).
- High trust interface for decision-support workflows.
- Immediate clarity on what agents do and what each run produces.
- Live execution confidence through transparent progress and event logs.

## App Information Architecture

Primary navigation:

1. Dashboard
2. Run Builder
3. Live Runs
4. Reports
5. Agent Gallery
6. Settings
7. Admin (role-gated)

## Page Specifications

### Dashboard

- summary cards:
  - active runs
  - success rate (7d)
  - average runtime
  - most used models/providers
- recent runs table with quick actions
- launch run CTA and "resume last config"

### Run Builder

- input controls:
  - ticker chips
  - date selector
  - provider/model selectors
  - advanced options (debate rounds, preset, checkpoints)
- validation inline with clear correction guidance
- preset templates:
  - fast daily
  - deep single-ticker
  - balanced portfolio scan

### Live Runs

- run list with status filters
- run detail panel:
  - stage timeline
  - per-ticker progress
  - streaming events/logs
  - cancel/retry controls

### Reports

- historical report explorer (tenant-scoped)
- markdown report render with metadata side panel
- compare mode (V2) for date-over-date analysis

### Agent Gallery

- each agent card includes:
  - role in pipeline
  - inputs/outputs
  - dependencies and failure modes
- expandable details tied to actual runtime stages

### Settings

- credentials vault UI (masked values, rotate/delete)
- model defaults and provider priority
- runtime defaults and guardrails
- feature flags and experimental toggles

## Design System Direction

- neutral dark/light themes with accessible contrast
- 8px spacing grid and consistent elevation scale
- reusable primitives:
  - cards
  - panels
  - timeline steps
  - status badges
  - empty/loading/error states

## Real-Time UX Behaviors

- optimistic transition to "queued" after run submit
- live timeline updates via SSE
- sticky key metrics at top of run detail
- reconnect banner and fallback polling when stream drops

## State Management

- server state: query library (cache + stale handling)
- client state: minimal global store for view state
- event stream reducer for deterministic timeline updates

## Accessibility and Quality

- keyboard-first navigation for all core workflows
- AA color contrast target
- semantic landmarks and aria labels
- clear focus order in forms and live console

## Frontend Technical Stack (Recommended)

- Next.js App Router
- TypeScript strict mode
- Tailwind + UI component primitives
- query/cache library for API state
- markdown renderer with sanitization

## Frontend Testing Strategy

- unit tests for key components and state reducers
- integration tests for run launch and status updates
- end-to-end tests for:
  - configure credentials
  - launch run
  - observe completion
  - view report

## Performance Requirements

- LCP < 2.5s on dashboard at p75
- no layout shift in run timeline updates
- virtualized event log rendering for long runs

## Brand and Messaging Direction

- Position as an "Agent Research Studio" for disciplined market analysis.
- Emphasize traceability, repeatability, and configurable intelligence.
- Keep legal disclaimer visible wherever final recommendations are displayed.
