from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class PortfolioHolding:
    """Holding as reported by a managed account statement."""

    ticker: str
    name: str
    weight: float


@dataclass(frozen=True)
class BenchmarkComponent:
    """Component in the target benchmark blend used for validation."""

    ticker: str
    name: str
    weight: float
    asset_class: str


@dataclass(frozen=True)
class ReturnPoint:
    """Periodic return represented as decimal (0.01 = 1%)."""

    period_end: date
    periodic_return: float


@dataclass(frozen=True)
class PerformanceSeries:
    """Time series linked to an instrument or portfolio name."""

    label: str
    points: list[ReturnPoint]


@dataclass(frozen=True)
class ComparisonResult:
    """Summary metrics used by reporting and alerting layers."""

    account_name: str
    benchmark_name: str
    cumulative_return_account: float
    cumulative_return_benchmark: float
    excess_return: float
    annualized_tracking_error: float
    information_ratio: float


@dataclass(frozen=True)
class AllocationDrift:
    """Difference between managed portfolio weights and benchmark proxy weights."""

    ticker: str
    portfolio_weight: float
    benchmark_weight: float
    drift: float


@dataclass(frozen=True)
class ValidationReport:
    """Single object that powers CLI, APIs, and persistence outputs."""

    comparison: ComparisonResult
    largest_positive_drift: AllocationDrift
    largest_negative_drift: AllocationDrift
    mean_absolute_drift: float
