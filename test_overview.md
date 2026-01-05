# Test Overview

**Date**: 2026-01-05
**Status**: ✅ All Tests Passed
**Execution Time**: ~20s

## Summary
The `unified-data` package is tested using `unittest`. The suite comprises unit tests, integration tests against live APIs, and package distribution verification.

### Test Statistics
- **Total Tests**: 35
- **Passed**: 35
- **Failed**: 0
- **Errors**: 0

## Test Suites

### 1. `tests/test_basic.py`
**Type**: Unit Tests (Mocked)
- **Purpose**: Validates internal dispatching and data normalization.
- **Coverage**:
    - Checks that `BTC_USDT` requests route to the Crypto adapter.
    - Checks that `AAPL` requests route to the Stock adapter.
    - Verifies that `pull_kline` returns a `KlineData` object with Status.OK.

### 2. `tests/test_adapters_live.py`
**Type**: Integration Tests (Live)
- **Purpose**: Tests individual adapter classes (`CCXTAdapter`, `YFinanceAdapter`, `AKShareAdapter`) directly.
- **Coverage**:
    - **AKShare**: Fetches China Stocks and Futures.
    - **CCXT**: Fetches Crypto (Binance).
    - **YFinance**: Fetches US Stocks and Futures.

### 3. `tests/test_adapters_error_handling.py`
**Type**: Integration Tests (Error Handling)
- **Purpose**: Verifies robustness against invalid inputs and API errors.
- **Coverage**:
    - **Wrong Symbols**: Ensures adapters handle invalid tickers gracefully (AKShare/YFinance return empty, CCXT raises specific error).

### 4. `tests/test_api_response.py`
**Type**: Unit/Integration Tests
- **Purpose**: Verifies that the public API returns structured `KlineData`.
- **Coverage**:
    - Ensures success returns `KlineData(status=OK, data=df)`.
    - Ensures failure returns `KlineData(status=FAILED, error=msg)`.

### 5. `tests/test_e2e.py`
**Type**: End-to-End Tests (Live)
- **Purpose**: Verifies the full user flow using the main `pull_kline` function.

### 6. `tests/test_kline_exchange_column.py`
**Type**: Verification (Live)
- **Purpose**: Ensures the new `exchange` column is correctly added to all results.

### 7. `tests/test_limits.py`
**Type**: Verification (Live)
- **Purpose**: Validates the strict `limit` enforcement (default 200).
- **Consolidated**: Replaces `test_limit_logic.py` and `test_limit_advanced.py`.
- **Coverage**:
    - Basic limits for all adapters.
    - Edge cases: `limit=1`, large limits, intraday limits.
    - Compatibility: Works alongside `start_date` and `end_date` (limit acts as tail).

### 8. `tests/test_top_level_imports.py`
**Type**: Package Verification
- **Purpose**: Confirms that key components (`pull_kline`, `MarketType`, `KlineData`, etc.) are exposed at the top-level package.

### 9. `tests/test_yfinance_concurrency.py`
**Type**: Concurrency Verification
- **Purpose**: Verifies thread safety and limit enforcement when fetching multiple tickers concurrently.

### 10. `verify_external.sh`
**Type**: Distribution Simulation
- **Purpose**: Simulates a 3rd party usage scenario by building a wheel and installing it into a fresh virtual environment.
- **Execution**: Runs `tests/test_verify_install.py` from an isolated directory.

### 11. Symbol Handling & Robustness
**Type**: Bug Fix & Feature Verification
- **Purpose**: Verified fix for "Length mismatch" bugs and implemented standard symbol conversion.
- **Coverage**:
    - Confirmed `AkshareAdapter` no longer crashes on invalid symbols.
    - Verified `get_exchange_symbol` logic for all adapters (`RB=F` -> `RB0`, `BTC_USDT` -> `BTC/USDT`).

## Execution
Tests are executed using `unittest` discovery.

```bash
python -m unittest discover tests
```

## Observations
- **Strict Limits**: Adapters now calculate optimal `start_date` heuristics to fulfill limits efficiently.
- **Unified Import**: Users should now use `from unified_data import pull_kline`.
- **Robustness**: API now returns `KlineData` object with explicit Status codes instead of raw DataFrames.
