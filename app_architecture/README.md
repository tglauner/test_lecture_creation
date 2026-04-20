# ING Validation App Architecture (Starter)

This app is a long-term validation scaffold for an ING-managed brokerage account (robo-advisor) against its underlying index + ETF benchmark blend.

## Architecture

- `domain`: immutable portfolio, benchmark, and report models.
- `application`: use-case service (`PerformanceAnalyzer`) for return analytics and allocation-drift checks.
- `infrastructure`: data adapters (dummy adapter today; future ING statement parser/CSV reader/DB adapter).
- `interfaces`: CLI (text or JSON output).

## Current analytics

- Cumulative return (account and benchmark)
- Excess return
- Annualized tracking error
- Information ratio
- Allocation drift vs benchmark weights

## Run

```bash
PYTHONPATH=src python -m perf_monitor.interfaces.cli
PYTHONPATH=src python -m perf_monitor.interfaces.cli --output json
PYTHONPATH=src python -m pytest tests -q
```

## Planned next adapters

1. `infrastructure/ing_statement_parser.py`
2. `infrastructure/benchmark_mapper.py`
3. `infrastructure/repository_sqlite.py`
4. Scheduler + alerting integration

## Note about target macOS path

If you want these files copied into your Dropbox project path on your Mac mini, run this from the repository root on that machine:

```bash
mkdir -p "/Users/tglauner/Library/CloudStorage/Dropbox/2) TG Investments and Research/Projects/ing_validation"
cp -R app_architecture/* "/Users/tglauner/Library/CloudStorage/Dropbox/2) TG Investments and Research/Projects/ing_validation/"
```

## GitHub repository setup

This project can be pushed to your GitHub repository:

`https://github.com/tglauner/ing_validation.git`

From the repository root:

```bash
git remote add origin https://github.com/tglauner/ing_validation.git
git push -u origin work
```
