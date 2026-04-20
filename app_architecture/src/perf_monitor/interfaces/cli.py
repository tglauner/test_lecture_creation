from __future__ import annotations

import argparse
import json
from dataclasses import asdict

from perf_monitor.application.services import PerformanceAnalyzer
from perf_monitor.infrastructure.dummy_data import (
    load_dummy_account_series,
    load_dummy_benchmark_components,
    load_dummy_benchmark_series,
    load_dummy_holdings,
)


def _fmt_pct(value: float) -> str:
    return f"{value * 100:.2f}%"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="ING account validation scaffold (dummy data).")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()

    analyzer = PerformanceAnalyzer()
    report = analyzer.build_validation_report(
        account_series=load_dummy_account_series(),
        benchmark_series=load_dummy_benchmark_series(),
        holdings=load_dummy_holdings(),
        benchmark_components=load_dummy_benchmark_components(),
    )

    if args.output == "json":
        print(json.dumps(asdict(report), indent=2, default=str))
        return

    print("=== ING Managed Account Validation (Dummy Data) ===")
    print(f"Account:   {report.comparison.account_name}")
    print(f"Benchmark: {report.comparison.benchmark_name}")
    print("-")
    print(f"Cumulative return (account):   {_fmt_pct(report.comparison.cumulative_return_account)}")
    print(f"Cumulative return (benchmark): {_fmt_pct(report.comparison.cumulative_return_benchmark)}")
    print(f"Excess return:                 {_fmt_pct(report.comparison.excess_return)}")
    print(f"Tracking error (annualized):   {_fmt_pct(report.comparison.annualized_tracking_error)}")
    print(f"Information ratio:             {report.comparison.information_ratio:.2f}")
    print("-")
    print(
        "Largest overweight: "
        f"{report.largest_positive_drift.ticker} ({_fmt_pct(report.largest_positive_drift.drift)})"
    )
    print(
        "Largest underweight: "
        f"{report.largest_negative_drift.ticker} ({_fmt_pct(report.largest_negative_drift.drift)})"
    )
    print(f"Mean absolute allocation drift: {_fmt_pct(report.mean_absolute_drift)}")


if __name__ == "__main__":
    main()
