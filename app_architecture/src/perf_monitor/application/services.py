from __future__ import annotations

from math import sqrt

from perf_monitor.domain.models import (
    AllocationDrift,
    BenchmarkComponent,
    ComparisonResult,
    PerformanceSeries,
    PortfolioHolding,
    ValidationReport,
)


class PerformanceAnalyzer:
    """Application service for account-vs-benchmark analytics and drift checks."""

    def build_validation_report(
        self,
        account_series: PerformanceSeries,
        benchmark_series: PerformanceSeries,
        holdings: list[PortfolioHolding],
        benchmark_components: list[BenchmarkComponent],
    ) -> ValidationReport:
        comparison = self.compare(account_series, benchmark_series)
        drifts = self.compute_allocation_drift(holdings, benchmark_components)

        largest_positive = max(drifts, key=lambda item: item.drift)
        largest_negative = min(drifts, key=lambda item: item.drift)
        mean_absolute_drift = sum(abs(item.drift) for item in drifts) / len(drifts)

        return ValidationReport(
            comparison=comparison,
            largest_positive_drift=largest_positive,
            largest_negative_drift=largest_negative,
            mean_absolute_drift=mean_absolute_drift,
        )

    def compare(self, account: PerformanceSeries, benchmark: PerformanceSeries) -> ComparisonResult:
        if len(account.points) != len(benchmark.points):
            raise ValueError("Account and benchmark series must have equal length.")
        if not account.points:
            raise ValueError("Series cannot be empty.")

        account_returns = [point.periodic_return for point in account.points]
        benchmark_returns = [point.periodic_return for point in benchmark.points]
        active_returns = [a - b for a, b in zip(account_returns, benchmark_returns)]

        cumulative_account = self._cumulative_return(account_returns)
        cumulative_benchmark = self._cumulative_return(benchmark_returns)
        excess = cumulative_account - cumulative_benchmark
        tracking_error = self._annualized_tracking_error(active_returns)
        information_ratio = self._information_ratio(active_returns)

        return ComparisonResult(
            account_name=account.label,
            benchmark_name=benchmark.label,
            cumulative_return_account=cumulative_account,
            cumulative_return_benchmark=cumulative_benchmark,
            excess_return=excess,
            annualized_tracking_error=tracking_error,
            information_ratio=information_ratio,
        )

    @staticmethod
    def compute_allocation_drift(
        holdings: list[PortfolioHolding],
        benchmark_components: list[BenchmarkComponent],
    ) -> list[AllocationDrift]:
        if not holdings or not benchmark_components:
            raise ValueError("Holdings and benchmark components cannot be empty.")

        portfolio_by_ticker = {h.ticker: h.weight for h in holdings}
        benchmark_by_ticker = {b.ticker: b.weight for b in benchmark_components}
        all_tickers = sorted(set(portfolio_by_ticker) | set(benchmark_by_ticker))

        return [
            AllocationDrift(
                ticker=ticker,
                portfolio_weight=portfolio_by_ticker.get(ticker, 0.0),
                benchmark_weight=benchmark_by_ticker.get(ticker, 0.0),
                drift=portfolio_by_ticker.get(ticker, 0.0) - benchmark_by_ticker.get(ticker, 0.0),
            )
            for ticker in all_tickers
        ]

    @staticmethod
    def _cumulative_return(returns: list[float]) -> float:
        growth = 1.0
        for period_return in returns:
            growth *= 1 + period_return
        return growth - 1

    @staticmethod
    def _annualized_tracking_error(active_returns: list[float]) -> float:
        if len(active_returns) == 1:
            return 0.0
        mean_active = sum(active_returns) / len(active_returns)
        squared_dev = [(x - mean_active) ** 2 for x in active_returns]
        sample_std = sqrt(sum(squared_dev) / (len(active_returns) - 1))
        return sample_std * sqrt(12)

    @staticmethod
    def _information_ratio(active_returns: list[float]) -> float:
        mean_monthly_active = sum(active_returns) / len(active_returns)
        annualized_active = mean_monthly_active * 12
        tracking_error = PerformanceAnalyzer._annualized_tracking_error(active_returns)
        if tracking_error == 0:
            return 0.0
        return annualized_active / tracking_error
