"""Compatibility wrapper around run_today for batch-style usage."""

from run_today import main


if __name__ == "__main__":
    raise SystemExit(main())
