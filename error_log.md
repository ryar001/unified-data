# Adapter Error Handling Report

**Date:** 2026-01-03
**Tests Performed:** Wrong Symbol / API Error Simulation

## Summary

We tested how each adapter handles invalid inputs (specifically `wrong symbol` or `404 Not Found`).

| Adapter | Scenario | Expected Behavior | Actual Outcome | Status |
| :--- | :--- | :--- | :--- | :--- |
| **AKShare** | Invalid Symbol (`INVALID_DESC_999`) | Return Empty DataFrame | Caught `Length mismatch`, returned Empty DF | ✅ PASS |
| **CCXT** | Invalid Symbol (`INVALID/COINPAIR`) | Raise Exception | Raised `ccxt.BadSymbol` ("binance does not have market symbol...") | ✅ PASS |
| **YFinance** | Invalid Symbol (`INVALID_TICKER_XYZ`) | Return Empty DataFrame | Logged HTTP 404, returned Empty DF | ✅ PASS |

## Detailed Logs

### AKShare
- **Input:** `INVALID_DESC_999`
- **Output:** Empty `polars.DataFrame` (shape: `0x0`)
- **Internal Error:** `AKShare Error: Length mismatch: Expected axis has 0 elements, new values have 8 elements`
- **Note:** The adapter catches the internal AKShare library error and gracefully returns an empty DataFrame.

### CCXT
- **Input:** `INVALID/COINPAIR`
- **Output:** Raised `ccxt.base.errors.BadSymbol`
- **Log:** `CCXT Error: binance does not have market symbol INVALID/COINPAIR`
- **Note:** The adapter properly propagates the exchange error, allowing callers to handle specific exchange issues.

### YFinance
- **Input:** `INVALID_TICKER_XYZ`
- **Output:** Empty `polars.DataFrame` (shape: `0x0`)
- **Log:** 
  ```
  ERROR:yfinance:HTTP Error 404: ... "Quote not found for symbol: INVALID_TICKER_XYZ"
  WARNING:yfinance_adapter:No data returned for INVALID_TICKER_XYZ
  ```
- **Note:** YFinance logs the 404 internally but returns an empty structure, which the adapter converts to an empty DataFrame.

## Conclusion
All adapters behave robustly. 
- **AKShare** and **YFinance** favor returning "No Data" (Empty DataFrame) for bad inputs.
- **CCXT** favors raising explicit exceptions for bad symbols.

Caller code should be prepared for both strategies (check for empty DF, and catch exceptions).
