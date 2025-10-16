# Lecture 067 — Cross-Currency Interest Rate Curves

## Learning Objectives
- Explain why cross-currency interest rate curves are required for modern multi-currency valuation frameworks.
- Describe the instruments, quoting conventions, and market data needed to construct cross-currency discount and forecast curves.
- Execute the bootstrapping workflow that simultaneously calibrates domestic and foreign curves with basis adjustments.
- Evaluate modeling and risk management considerations, including collateral agreements, curve extrapolation, and stress testing.

## 1. Setting the Stage: Why Cross-Currency Curves Matter
- **Post-crisis market evolution**: Since 2008, collateralized trading and central clearing separated funding rates from risk-free benchmarks. Multi-currency derivatives now require discount curves tied to collateral currencies, plus forecast curves for each floating index.
- **Valuation neutrality**: Consistent valuation requires that forward FX rates implied by discount curves match the cross-currency swap (CCS) market. Inconsistencies manifest as arbitrage or mis-priced trades.
- **Business drivers**: Treasury funding, structured product issuance, and global client hedging all depend on reliable cross-currency curve sets. Errors cascade into pricing, liquidity management, and regulatory capital metrics.

## 2. Market Instruments and Conventions
### 2.1 Building Blocks
- **FX spots and forwards**: Provide the anchor for relative value between currencies. Spot FX sets the notional exchange, while FX forwards inform the short end of the basis when liquid.
- **Interest rate swaps (IRS)**: Domestic fixed-versus-floating swaps calibrate single-currency curves (OIS and IBOR-based) that feed into cross-currency construction.
- **Cross-currency swaps**: Deliver periodic notional exchanges and floating payments in two currencies. Variants include fixed/floating, floating/floating (most common), and basis swaps exchanging different tenor indices (e.g., USD SOFR vs. EUR €STR).
- **Basis swaps and basis spreads**: Market quotes are typically expressed as spreads added to the floating leg in one currency to equate present values under par conditions.

### 2.2 Quoting Mechanics
- **Reset and payment calendars**: Align with each index’s business day conventions; mismatches require detailed schedule generation.
- **Day count conventions**: Common combinations include ACT/360 vs. ACT/365F, influencing accrual factors and curve calibration.
- **Collateral currency assumption**: Determine which discount curve applies. A USD collateralized EUR-USD CCS uses a USD OIS discount curve for both legs while forecasting respective floating cash flows on EUR €STR and USD SOFR indices.
- **Quote types**: Market may quote spreads on either leg, mid-market basis plus bid/ask, or via all-in forward points. Understanding the quoting axis is essential for clean data ingestion.

## 3. Data Preparation and Curve Segmentation
- **Instrument taxonomy**: Classify instruments by maturity and liquidity (e.g., short-dated FX forwards, intermediate CCS, long-dated mark-to-market swaps).
- **Market data alignment**: Ensure consistency of fixing histories, holiday calendars, and FX spot cut-off times.
- **Curve segmentation**: Maintain separate curves for discounting (per collateral currency) and forecasting (per floating index). Cross-currency curves often require linked bootstraps because basis spreads depend on both sets.
- **Initial guesses**: Use anchored single-currency curves and simple basis interpolations to initialize the joint solve.

## 4. Bootstrapping Workflow
### 4.1 Conceptual Overview
1. **Lock collateral discount curves**: Start with overnight indexed swap (OIS) curves for each collateral currency, reflecting CSA terms.
2. **Construct domestic forecast curves**: Build single-currency IBOR or RFR curves using IRS and basis swaps (e.g., SOFR vs. term SOFR).
3. **Incorporate cross-currency instruments**: Use CCS quotes to solve for basis adjustments that align foreign-leg discounting with domestic collateral assumptions.
4. **Iterate to convergence**: Because discount factors and forward FX rates interact, iterative methods (Gauss–Seidel, Newton-Raphson, or simultaneous solvers) are common.

### 4.2 Detailed Steps
- **Step A — Short-end calibration**
  - Combine spot FX, overnight FX swap points, and short-dated CCS (if available) to pin near-term basis spreads.
  - Apply collateral adjustments: if collateral differs from either currency, discount short cash flows on the collateral curve, not the domestic curve.
- **Step B — Intermediate maturities**
  - Use liquid tenors (1Y–10Y) where basis quotes are most reliable. Solve for forward basis spreads such that present value of both legs equals zero when discounting on collateral curves.
  - Impose smoothness constraints (e.g., cubic spline or monotone convex interpolation) while preserving no-arbitrage conditions.
- **Step C — Long-end extrapolation**
  - For sparse data beyond 15–20 years, impose asymptotic assumptions (mean-reverting basis, constant forward spreads) consistent with economic narratives.
  - Stress-test sensitivity to alternative extrapolations, as valuation of long-dated trades is highly sensitive.
- **Step D — Consistency checks**
  - Verify triangular relationships: FX forward implied by discount curves should match market forward; cross-check with FX option-implied carry where possible.
  - Ensure cashflow present values vanish under par assumptions within numerical tolerance.

## 5. Modeling Considerations
- **Collateral optionality**: Many CSAs allow currency switches. Modeling requires scenario-dependent discount curves or valuation adjustments (COLVA/Funding VA).
- **Central clearing nuances**: CCPs specify discounting methodology (e.g., LCH uses SONIA discounting for GBP cleared trades). House valuations must align with CCP margining.
- **Interest rate benchmark reform**: Transition from LIBOR to RFRs alters floating leg definitions and available historical data. Maintain curve variants for legacy trades referencing fallback rates.
- **Curve construction tools**: Industry practice leverages bootstrapping engines (QuantLib, in-house libraries) with automatic differentiation to supply sensitivities for risk aggregation.
- **Numerical stability**: Guard against oscillations by using robust interpolation (log-linear on discount factors, monotone splines on forward basis) and damping iterations when quotes are noisy.

## 6. Risk Management and Hedging
### 6.1 Sensitivity Measures
- **Curve DV01s**: Separate sensitivities by currency, curve segment, and collateral assumption to reflect hedge ratios accurately.
- **FX-IR interplay**: Cross-gamma between FX spot and interest rate curves matters for margin and VaR; incorporate multi-factor risk models.
- **Basis bucket risk**: Monitor exposures to specific basis tenors (e.g., 5Y EURUSD basis) since liquidity can dry up quickly under stress.

### 6.2 Hedging Tactics
- **Micro hedging**: Use offsetting CCS trades or FX swaps to neutralize individual trade sensitivities.
- **Macro hedging**: Align structural funding positions with treasury issuance (e.g., issuing EUR debt swapped back to USD to exploit favorable basis).
- **Liquidity management**: Track collateral demands from currency moves; maintain diversified funding to avoid wrong-way risk with counterparties.

### 6.3 Stress Testing and Scenario Analysis
- Simulate historical dislocations (e.g., 2008 USD funding squeeze, 2020 COVID liquidity shock) to assess P&L and collateral swings.
- Combine parallel shifts, steepeners, and FX shocks to gauge worst-case exposures under integrated scenarios.
- Evaluate knock-on effects on valuation adjustments (CVA/FVA/MVA) given correlated moves in credit spreads and funding basis.

## 7. Case Study: EUR/USD Cross-Currency Basis
- **Market snapshot**: Discuss how the EURUSD basis typically trades negative (USD demand for funding) and widens during funding stress.
- **Data ingestion**: Acquire spot FX, FX forwards, EUR €STR OIS curve, USD SOFR OIS curve, EUR IRS, USD IRS, and market CCS spreads for tenors 1Y–30Y.
- **Bootstrapping illustration**: Walk through calibrating a USD-collateralized curve set. Show how a -20 bp 5Y basis quote shifts the USD discount factor adjustment relative to EUR.
- **Risk interpretation**: Examine DV01 decomposition for a 10Y EUR payer CCS hedging USD liabilities. Highlight sensitivity to EUR curve, USD curve, basis curve, and FX spot.
- **Reporting**: Present dashboards showing curve shapes, basis term structure, and hedging recommendations for treasury stakeholders.

## 8. Implementation Notes for Analytics Teams
- **Workflow automation**: Schedule daily curve builds with validation gates for stale or missing quotes.
- **Data governance**: Maintain golden sources, audit trails, and model documentation to satisfy regulatory expectations (e.g., SR 11-7 in the US, ECB TRIM guidelines).
- **Version control and reproducibility**: Tag curve builds with code commit hashes, market data timestamps, and configuration metadata.
- **Operational resilience**: Build fallbacks for illiquid markets—e.g., proxy basis using related currency pairs, or switch to broker quotes when screens are empty.

## 9. Studio Exercises and Further Reading
### 9.1 Hands-on Activities
- **Curve bootstrapping lab**: Students implement a simplified EURUSD CCS bootstrap using provided market data, comparing linear vs. log-linear interpolation outcomes.
- **Stress test builder**: Construct a scenario generator that perturbs basis spreads independently from domestic curves and observes P&L for a multi-currency swap portfolio.
- **Collateral switch analysis**: Evaluate the impact of switching CSA collateral from USD to EUR on a set of cross-currency trades.

### 9.2 Discussion Questions
1. What economic forces drive persistent negative USD basis spreads, and how might central bank facilities influence them?
2. How does the choice of interpolation method affect hedging effectiveness for long-dated CCS positions?
3. In what situations would a firm intentionally maintain an open basis exposure?

### 9.3 Suggested Reading
- BIS Quarterly Review articles on global dollar funding markets.
- “Multi-Curve Framework for Interest Rate Derivatives” (Henrard, 2014) — chapters on cross-currency modeling.
- ISDA collateral and valuation adjustment best-practice papers.
- Central bank speeches on FX swap market functioning (e.g., ECB, Federal Reserve).

### 9.4 Preparation for Next Lecture
- Review valuation adjustments (CVA, FVA, MVA) and how cross-currency curves feed into exposure profiles.
- Gather recent market data snapshots (spot, forwards, CCS spreads) for a chosen currency pair to use in the next session’s exercises.

