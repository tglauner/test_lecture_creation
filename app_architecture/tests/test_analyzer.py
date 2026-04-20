from perf_monitor.application.services import PerformanceAnalyzer
from perf_monitor.infrastructure.dummy_data import (
    load_dummy_account_series,
    load_dummy_benchmark_components,
    load_dummy_benchmark_series,
    load_dummy_holdings,
)


def test_build_validation_report_contains_expected_metrics() -> None:
    analyzer = PerformanceAnalyzer()
    report = analyzer.build_validation_report(
        account_series=load_dummy_account_series(),
        benchmark_series=load_dummy_benchmark_series(),
        holdings=load_dummy_holdings(),
        benchmark_components=load_dummy_benchmark_components(),
    )

    assert report.comparison.cumulative_return_account > report.comparison.cumulative_return_benchmark
    assert report.comparison.excess_return > 0
    assert report.comparison.annualized_tracking_error >= 0
    assert report.comparison.information_ratio != 0


def test_allocation_drift_has_expected_extremes() -> None:
    analyzer = PerformanceAnalyzer()
    drifts = analyzer.compute_allocation_drift(
        holdings=load_dummy_holdings(),
        benchmark_components=load_dummy_benchmark_components(),
    )

    by_ticker = {item.ticker: item.drift for item in drifts}
    assert round(by_ticker["IWDA"], 4) == -0.05
    assert round(by_ticker["CSH"], 4) == 0.05
