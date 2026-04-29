# Latest State Alignment (Apr 29, 2026)

## Why This Update Exists

The original `app-build-` specs were created before the latest repo enhancements. This document updates implementation assumptions so the first web app build aligns with the current `Agent-Alpha` architecture.

## Confirmed Current-State Facts

- Project identity is now `Agent-Alpha`.
- Primary runtime is `scripts/run_today.py`.
- Supported runtime options include:
  - `--ticker`, `--tickers`, `--date`
  - `--provider`, `--deep-model`, `--quick-model`
  - `--debate-rounds`, `--output-dir`, `--checkpoint`
- Output contract is stable:
  - `outputs/YYYY-MM-DD/<TICKER>/report.md`
  - `outputs/YYYY-MM-DD/<TICKER>/metadata.json`
  - `outputs/YYYY-MM-DD/index.md`
- Planning now includes `Research_Context_Integration_Tech_Spec.md` for external context injection.

## Scope Adjustment for First App Build

For this implementation pass, build a **minimal local web app** (not full multi-tenant SaaS yet) that provides:

1. Run launcher for one/many tickers.
2. Live run logs/status while script executes.
3. Report browser + report reader.
4. Settings panel for:
   - default provider/models/debate rounds/checkpoint
   - local API key management for `.env.enterprise` in development

This creates a practical bridge from script-first to productized UX without forcing premature platform complexity.

## Deferred from Initial Build

- multi-tenant auth and RBAC
- remote worker queue and distributed runtime
- billing/usage metering
- hosted secrets vault

## Architecture Decision for This Build

- Use a lightweight Python web server in `app/` that shells into `scripts/run_today.py`.
- Preserve existing orchestrator code unchanged.
- Persist app settings to `app/settings.json`.
- Sync API key settings into `.env.enterprise` for local runtime compatibility.

## Phase-2 Upgrade Path

When moving from local app to SaaS:

- swap subprocess runner for queue-backed worker service
- replace local settings + `.env.enterprise` with encrypted secret storage
- add auth, tenant scoping, and policy controls
- keep frontend information architecture mostly unchanged

## Build Success Criteria (This Pass)

- User can launch a run in UI and see execution logs.
- User can review generated reports in UI.
- User can update run defaults from settings.
- User can set provider API keys from settings for local development flow.
