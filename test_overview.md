# Test Overview

**Date**: 2025-12-31
**Status**: ✅ All Tests Passed (14/14)
**Execution Time**: ~22.8s

## Summary
The `unified-data` package is tested using `unittest`. The suite comprises both unit tests (using mocks) and integration/end-to-end tests (hitting live APIs).

### Test Statistics
- **Total Tests**: 14
- **Passed**: 14
- **Failed**: 0
- **Errors**: 0

## Test Suites

### 1. `tests/test_mocked.py`
**Type**: Unit Tests (Mocked)
- **Purpose**: Verifies the core logic of `pull_kline` without making external network requests.
- **Coverage**:
    - Ensures `pull_kline` correctly calls the appropriate adapter based on `MarketType` and `Exchange` params.
    - Verifies handling of returned DataFrames.
    - uses `unittest.mock` to simulate `ccxt`, `yfinance`, and `akshare`.

### 2. `tests/test_basic.py`
**Type**: Unit Tests (Mocked)
- **Purpose**: Validates internal dispatching and data normalization.
- **Coverage**:
    - Checks that `BTC_USDT` requests route to the Crypto adapter.
    - Checks that `AAPL` requests route to the Stock adapter.
    - Verifies that returned columns match the expected enum values.

### 3. `tests/test_adapters_live.py`
**Type**: Integration Tests (Live)
- **Purpose**: Tests the individual adapter classes (`CCXTAdapter`, `YFinanceAdapter`, `AKShareAdapter`) directly against their respective live APIs.
- **Coverage**:
    - **AKShare**: Fetches China Stocks (`000001`) and Futures (Front Month).
    - **CCXT**: Fetches Crypto (`BTC/USDT`) from Binance.
    - **YFinance**: Fetches US Stocks (`AAPL`) and Futures (`GC=F`).

### 4. `tests/test_e2e.py`
**Type**: End-to-End Tests (Live)
- **Purpose**: Verifies the full user flow using the main public `pull_kline` function.
- **Coverage**:
    - Ensures that the user-facing API correctly handles standardized inputs (e.g. `BTC_USDT`) and returns populated Polars DataFrames from real sources.
    - Covers all supported market types: Crypto, Stock, Futures.

## Execution
Tests were executed using the `uv` package manager to handle dependencies in a virtual environment.

```bash
uv run python -m unittest discover tests
```

## Observations
- **Live Tests**: Requires active internet connection. Pass/fail results may depend on external API availability (e.g. AKShare, Yahoo Finance).
- **Dependencies**: The project relies on `polars`, `ccxt`, `yfinance`, and `akshare`.
