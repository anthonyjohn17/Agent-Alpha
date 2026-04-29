# Agent-Alpha Minimal Web App

Local-first UI for launching `scripts/run_today.py`, monitoring run logs, managing local defaults/API keys, and reading generated reports.

## Start

From repo root:

```bash
python app/server.py
```

Open:

- [http://127.0.0.1:8787](http://127.0.0.1:8787)

## What It Supports

- Launch one or many ticker runs.
- Choose provider, models, debate rounds, date, and checkpoint option.
- View in-progress run logs and status.
- Browse reports from `outputs/`.
- Save defaults/API keys in:
  - `app/settings.json`
  - `.env.enterprise` (auto-generated keys for local runtime)

## Notes

- This is intentionally minimal and local-dev oriented.
- Keys are stored in local files for convenience; do not use this pattern as-is for production SaaS.
