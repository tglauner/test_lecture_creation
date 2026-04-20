from __future__ import annotations

from datetime import date

from perf_monitor.domain.models import (
    BenchmarkComponent,
    PerformanceSeries,
    PortfolioHolding,
    ReturnPoint,
)


def load_dummy_account_series() -> PerformanceSeries:
    returns = [0.011, -0.004, 0.008, 0.013, -0.007, 0.006, 0.010, -0.002, 0.009, 0.004, -0.003, 0.012]
    points = [
        ReturnPoint(period_end=date(2025, month, 28), periodic_return=monthly)
        for month, monthly in enumerate(returns, start=1)
    ]
    return PerformanceSeries(label="ING Managed Account (Dummy)", points=points)


def load_dummy_benchmark_series() -> PerformanceSeries:
    returns = [0.010, -0.003, 0.007, 0.011, -0.006, 0.007, 0.009, -0.001, 0.008, 0.003, -0.002, 0.010]
    points = [
        ReturnPoint(period_end=date(2025, month, 28), periodic_return=monthly)
        for month, monthly in enumerate(returns, start=1)
    ]
    return PerformanceSeries(label="Underlying Index + ETF Blend (Dummy)", points=points)


def load_dummy_holdings() -> list[PortfolioHolding]:
    return [
        PortfolioHolding(ticker="IWDA", name="iShares MSCI World", weight=0.40),
        PortfolioHolding(ticker="EIMI", name="iShares EM IMI", weight=0.20),
        PortfolioHolding(ticker="AGGH", name="iShares Core Global Aggregate Bond", weight=0.25),
        PortfolioHolding(ticker="CSH", name="Cash", weight=0.15),
    ]


def load_dummy_benchmark_components() -> list[BenchmarkComponent]:
    return [
        BenchmarkComponent(ticker="IWDA", name="MSCI World Proxy", weight=0.45, asset_class="Equity"),
        BenchmarkComponent(ticker="EIMI", name="EM Equity Proxy", weight=0.15, asset_class="Equity"),
        BenchmarkComponent(ticker="AGGH", name="Global Aggregate Bond Proxy", weight=0.30, asset_class="Fixed Income"),
        BenchmarkComponent(ticker="CSH", name="Cash", weight=0.10, asset_class="Cash"),
    ]
