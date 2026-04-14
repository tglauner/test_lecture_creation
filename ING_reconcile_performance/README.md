# ING_reconcile performance

This repository/module will contain a Python script that connects to:

1. **ING bank account data** (via API export endpoint), and
2. **Google Sheets** (via Google Sheets API),

then reconciles actual ING account movements/balances against the expected performance data.

## Planned scope

- Pull actual account transactions and balances from ING API.
- Pull expected performance records from a Google Sheet.
- Match and reconcile by date/reference/amount.
- Produce a reconciliation output (matched, unmatched, and differences).
- Generate a summary report for review.

## Tech stack

- Python 3.11+
- Google Sheets API
- REST API client for ING endpoint

## Next implementation steps

- Add API authentication handling for ING and Google.
- Implement data extraction and normalization.
- Add reconciliation logic and tolerance rules.
- Export reconciliation results back to Google Sheets.
