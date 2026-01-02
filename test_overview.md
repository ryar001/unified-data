# Test Overview

**Date**: 2026-01-02
**Status**: ✅ All Tests Passed (28/28)
**Execution Time**: ~30s

## Summary
The `unified-data` package is tested using `unittest`. The suite comprises unit tests, integration tests against live APIs, and package distribution verification.

### Test Statistics
- **Total Tests**: 28
- **Passed**: 28
- **Failed**: 0
- **Errors**: 0

## Test Suites

### 1. `tests/test_mocked.py`
**Type**: Unit Tests (Mocked)
- **Purpose**: Verifies the core logic of `pull_kline` without making external network requests.
- **Coverage**:
    - Ensures `pull_kline` correctly calls the appropriate adapter based on `MarketType` and `Exchange` params.
    - Verifies handling of returned DataFrames.

### 2. `tests/test_basic.py`
**Type**: Unit Tests (Mocked)
- **Purpose**: Validates internal dispatching and data normalization.
- **Coverage**:
    - Checks that `BTC_USDT` requests route to the Crypto adapter.
    - Checks that `AAPL` requests route to the Stock adapter.

### 3. `tests/test_adapters_live.py`
**Type**: Integration Tests (Live)
- **Purpose**: Tests individual adapter classes (`CCXTAdapter`, `YFinanceAdapter`, `AKShareAdapter`) directly.
- **Coverage**:
    - **AKShare**: Fetches China Stocks and Futures.
    - **CCXT**: Fetches Crypto (Binance).
    - **YFinance**: Fetches US Stocks and Futures.

### 4. `tests/test_e2e.py`
**Type**: End-to-End Tests (Live)
- **Purpose**: Verifies the full user flow using the main `pull_kline` function.

### 5. `tests/test_kline_exchange_column.py`
**Type**: Verification (Live)
- **Purpose**: Ensures the new `exchange` column is correctly added to all results.
- **Coverage**:
    - Verifies default routing results in the correct enum string (e.g., `ccxt`, `yfinance`).

### 6. `tests/test_limit_logic.py` & `tests/test_limit_advanced.py`
**Type**: Verification (Live)
- **Purpose**: Validates the strict `limit` enforcement (default 200).
- **Coverage**:
    - Edge cases: `limit=1`, large limits.
    - Compatibility: Works alongside `start_date` and `end_date` (limit acts as tail).
    - Period support: Verified for intraday intervals.

### 7. `tests/test_top_level_imports.py`
**Type**: Package Verification
- **Purpose**: Confirms that key components (`pull_kline`, `MarketType`, etc.) are exposed at the top-level package for cleaner imports.

### 8. `verify_external.sh`
**Type**: Distribution Simulation
- **Purpose**: Simulates a 3rd party usage scenario by building a wheel and installing it into a fresh virtual environment.
- **Execution**: Runs `tests/test_verify_install.py` from an isolated directory.

## Execution
Tests are executed using `unittest` discovery.

```bash
python -m unittest discover tests
```

## Observations
- **Strict Limits**: Adapters now calculate optimal `start_date` heuristics to fulfill limits efficiently.
- **Unified Import**: Users should now use `from unified_data import pull_kline`.
- **Packaging**: Verified that `uv build` produces valid artifacts installable by 3rd party projects.
