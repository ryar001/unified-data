# Test Overview

**Date**: 2026-01-13
**Status**: ✅ All Tests Passed
**Execution Time**: ~20s

## Summary
The `unified-data` package is tested using `unittest`. The suite comprises unit tests, integration tests against live APIs, and package distribution verification. Recent updates refactored CCXT architecture and consolidated redundant tests.

### Test Statistics
- **Total Tests**: ~45
- **Passed**: All
- **Failed**: 0
- **Errors**: 0

## Test Suites

### 1. `tests/test_ccxt_strategies.py`
**Type**: Unit Tests (Mocked)
**Purpose**: Verifies the strategy pattern implementation for CCXT adapters.
**Coverage**:
    - **Binance**: Symbol/Period conversion validation.
    - **Coinbase**: Smart symbol resolution (e.g., fallback from `.../USDT` to `.../USD` if the former is missing).

### 2. `tests/test_adapters_live.py`
**Type**: Integration Tests (Live)
**Purpose**: Tests individual adapter classes directly.
**Coverage**:
    - **AKShare**: Fetches China Stocks and Futures.
    - **CCXT**: Fetches Crypto (Binance AND Coinbase).
    - **YFinance**: Fetches US Stocks and Futures.

### 3. `tests/test_e2e.py`
**Type**: End-to-End Tests (Live)
**Purpose**: Verifies the full user flow using the main `pull_kline` function.
**Coverage**:
    - **Flow**: Validates data retrieval for all market types (Stock, Crypto, Futures).
    - **Columns**: Ensures `exchange` and `symbol` columns are correct.
    - **Error Handling**: Verifies correct `Statuc.FAILED` responses for invalid inputs (merged from `test_api_response.py`).

### 4. `tests/test_adapters_error_handling.py`
**Type**: Integration Tests (Error Handling)
**Purpose**: Verifies robustness against invalid inputs and API errors.
**Coverage**:
    - **Wrong Symbols**: Ensures adapters handle invalid tickers gracefully.

### 5. `tests/test_limits.py`
**Type**: Verification (Live)
**Purpose**: Validates the strict `limit` enforcement (default 200).
**Coverage**:
    - Basic limits for all adapters.
    - Edge cases: `limit=1`, large limits, intraday limits.
    - Compatibility: Works alongside `start_date` and `end_date` (limit acts as tail).

### 6. `tests/test_timeframes.py`
**Type**: Unit & Integration Tests
**Purpose**: Verifies period standardization and conversion.
**Coverage**:
    - **Conversion**: Tests `to_exchange_period` for all adapters.
    - **Live Fetch**: Integration tests for standard periods (`1d`, `1w`, `1M`) across all adapters.

### 7. `tests/test_ws_smoke.py`
**Type**: Websocket Smoke Tests
**Purpose**: Basic verification of Websocket adapter instantiation and connectivity (if applicable).

### 8. `tests/test_yfinance_concurrency.py`
**Type**: Concurrency Verification
**Purpose**: Verifies thread safety and limit enforcement when fetching multiple tickers concurrently.

### 9. `tests/test_top_level_imports.py`
**Type**: Package Verification
**Purpose**: Confirms that key components (`pull_kline`, `MarketType`, `KlineData`, etc.) are exposed at the top-level package.

### 10. `tests/test_verify_install.py`
**Type**: Installation Verification
**Purpose**: Simple script to verify package imports in a clean environment.

## Removed / Merged Tests
- `tests/test_basic.py`: Merged/Superseded by `test_e2e.py` and adapter tests.
- `tests/test_api_response.py`: Merged into `test_e2e.py`.
- `tests/test_kline_exchange_column.py`: Checks merged into `test_e2e.py`.
- `tests/test_ccxt_coinbase.py`: Merged into `test_adapters_live.py`.

## Execution
Tests are executed using `unittest` discovery.

```bash
uv run -m unittest discover tests
```

## Observations
- **Architecture**: CCXT now uses a strategy pattern with `CoinbaseStrategy` defaulting to smart USDT->USD fallback.
- **Default Routing**: `Exchange.CCXT` now routes to `CoinbaseStrategy` by default.
- **Robustness**: API returns structured `KlineData` with explicit Status codes.
