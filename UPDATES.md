**Date**: 2026-01-05

**Warnings**:
*   No breakpoints found.

**What's New**:
*   `error_log.md`: Documented adapter error handling test results for wrong symbols and API errors.
*   `reproduce_issue.py`: Added a script to reproduce a specific AKShare adapter error.
*   `src/unified_data/models/enums.py`: Introduced `Status` enum for API responses (`OK`, `FAILED`).
*   `src/unified_data/models/types.py`: Defined `KlineData` dataclass for structured API responses, including status, data (DataFrame), and error message.
*   `tests/test_adapters_error_handling.py`: New tests to verify adapter behavior with invalid symbols (AKShare, CCXT, YFinance).
*   `tests/test_api_response.py`: New tests to validate the `KlineData` object structure and status codes in API responses for success and failure cases.
*   `tests/test_limits.py`: Consolidated and enhanced tests for the `limit` parameter across different adapters and edge cases.
*   `test_overview.md`: Updated to reflect the new `KlineData` response format and the expanded error handling tests.

**Refactor**:
*   `src/unified_data/api.py`:
    *   Modified `pull_kline` to return a `KlineData` object instead of a raw DataFrame, providing explicit status and error information.
    *   Added logic to handle empty DataFrames by returning `Status.FAILED`.
    *   Ensured `exchange` and `ticker` columns are added to successful results.
*   Deleted files `tests/test_limit_advanced.py` and `tests/test_limit_logic.py` as their functionality has been merged into `tests/test_limits.py`.

REFACTOR:
  src/unified_data/adapters/akshare_adapter.py:
    - Integrated `get_exchange_symbol` for symbol resolution.
    - Added heuristic for `market_type` inference when not provided.
    - Normalized tickers to uppercase.
  src/unified_data/adapters/base.py:
    - Added `get_exchange_symbol` method.
    - Updated adapter `__init__` signatures to include `market_type` and `limit`.
    - Imported `Columns` and `MarketType` enums.
  src/unified_data/adapters/ccxt_adapter.py:
    - Set default `market_type` to `MarketType.CRYPTO`.
    - Integrated `get_exchange_symbol`.
    - Normalized tickers to uppercase.
  src/unified_data/adapters/yfinance_adapter.py:
    - Set default `market_type` to `MarketType.STOCK`.
    - Integrated `get_exchange_symbol`.
    - Normalized tickers to uppercase.
    - Added specific handling for crypto tickers containing underscores.
TEST:
  tests/test_standard_symbol.py:
    - New file: Added tests to verify mixed-case and standard symbol normalization for futures, crypto, and stocks across `AKShareAdapter`, `CCXTAdapter`, and `YFinanceAdapter`.
    - Includes tests for numeric stock tickers.

**Warnings**:
None.

**Feat**
*   `src/unified_data/adapters/yfinance_adapter.py`: Enhanced `get_kline` to use `yf.Ticker.history` for more robust data fetching, supporting `interval`, `start_date`, `end_date`, and `auto_adjust=True`. Added an example usage block.

**Tests**
*   `tests/test_yfinance_concurrency.py`: Added a new test file for `YFinanceAdapter` to verify concurrency, thread safety, and strict limit enforcement. Ensures correct DataFrame structure, row count, and columns.
*   `test_overview.md`: Documented the new `test_yfinance_concurrency.py` test, detailing its purpose and coverage.
*   `tests/test_basic.py`: Added mocks for `yf.Ticker` and `yf.Ticker.history` in `TestDataAPI.test_pull_kline`.

**Bugfix**
*   `src/unified_data/adapters/akshare_adapter.py`: Refined `get_kline` logic and added `get_exchange_symbol` to handle AKShare's specific symbol formats (e.g., "RB=F" -> "RB0").
*   `src/unified_data/api.py`: Modified `pull_kline` to use `adapter.get_exchange_symbol` for converting standard tickers to exchange-specific symbols before fetching data, ensuring consistency. It also ensures the original standard ticker is returned in the DataFrame.

**Refactor**
*   `src/unified_data/adapters/base.py`: Introduced `get_exchange_symbol` as an abstract method, enforcing consistent symbol conversion across all adapters.
*   `src/unified_data/adapters/akshare_adapter.py`: Streamlined `get_kline` logic and added comprehensive logging.
*   `src/unified_data/adapters/ccxt_adapter.py`: Implemented `get_exchange_symbol` to convert standard crypto tickers (e.g., "BTC_USDT") to CCXT's format ("BTC/USDT").
*   `src/unified_data/adapters/yfinance_adapter.py`: Implemented `get_exchange_symbol` to handle crypto ticker conversions for YFinance (e.g., "BTC_USDT" to "BTC-USD").
*   `tests/test_mocked.py`: Significantly refactored test setup using `setUp` and `tearDown` for better isolation and mocking of external dependencies (`polars`, `ccxt`, `yfinance`, `akshare`) and DataFrame behavior.

**Chore**
*   `pyproject.toml`: Added `pytest>=9.0.2` to the development dependency group.
*   `uv.lock`: Updated package lockfile with new dependencies, including `pytest`, `iniconfig`, `packaging`, `pluggy`, and `pygments`.

**Other**
*   `tests/test_adapters_live.py`: Added a print statement for logging during live adapter tests.
*   `src/unified_data/adapters/yfinance_adapter.py`: Added a `print(df)` statement within the `get_kline` method.

Feat
----
* `src/unified_data/adapters/yfinance_adapter.py`: Enhanced `get_kline` to use `yf.Ticker.history` for more robust data fetching, supporting `interval`, `start_date`, `end_date`, and `auto_adjust=True`. Added an example usage block.

Tests
-----
* `tests/test_yfinance_concurrency.py`: Added a new test file for `YFinanceAdapter` to verify concurrency, thread safety, and strict limit enforcement. Ensures correct DataFrame structure, row count, and columns.
* `test_overview.md`: Documented the new `test_yfinance_concurrency.py` test, detailing its purpose and coverage.

Chore
-----
* `pyproject.toml`: Added `pytest>=9.0.2` to the development dependency group.
* `uv.lock`: Updated package lockfile with new dependencies, including `pytest`, `iniconfig`, `packaging`, `pluggy`, and `pygments`.

Other
-----
* `tests/test_adapters_live.py`: Added a print statement for logging during live adapter tests.

What's New
*   `pyproject.toml`: Added `pytest` to the `dev` dependency group.
*   `src/unified_data/adapters/yfinance_adapter.py`: Enhanced `YFinanceAdapter` to use `yf.Ticker.history()` for more robust historical data fetching. Included an example usage block.
*   `tests/test_yfinance_concurrency.py`: Introduced a new test suite to verify concurrent data fetching and ensure correct data structure and row limits from the `yfinance_adapter`.
*   `uv.lock`: Updated lock file to include new development dependencies like `pytest` and its transitive dependencies.

Documentation
*   `test_overview.md`: Updated to include documentation for the new `test_yfinance_concurrency.py` test suite.

Minor Changes
*   `tests/test_adapters_live.py`: Added a debug print statement in `test_yfinance_adapter_live_stock`.

**Date**: 2026-01-02

**Warnings**:
* No breakpoints found.

**Documentation**
* **`test_overview.md`**
    * Updated test status to '✅ All Tests Passed (28/28)'.
    * Updated test execution time to '~30s'.
    * Enhanced descriptions and coverage details for:
        * `tests/test_adapters_live.py` (including specific adapter details for AKShare, CCXT, YFinance).
        * `tests/test_limit_logic.py` and `tests/test_limit_advanced.py` (detailing limit enforcement, edge cases, compatibility, and period support).
        * `tests/test_top_level_imports.py` (clarifying purpose).
        * `verify_external.sh` (adding simulation, execution, and purpose details).
    * Added notes on:
        *   Adapter optimizations for limit fulfillment using `start_date` heuristics.
        *   Unified import for top-level `pull_kline` function.
        *   Verification of `uv build` packaging for third-party installation.

**Refactor**
* **`.gitignore`**
    * Added `.ruff_cache` to ignore list.
    * Added `.DS_Store` to ignore list.

**Warnings:**
* No breakpoints found.

**What's New:**
*   **New Files:**
    *   `tests/test_kline_exchange_column.py`: Adds tests for the 'exchange' column in `pull_kline`.
    *   `tests/test_limit_advanced.py`: Introduces advanced tests for the 'limit' parameter.
    *   `tests/test_limit_logic.py`: Verifies strict enforcement of the 'limit' parameter.
    *   `tests/test_top_level_imports.py`: Ensures top-level importability of core components.
    *   `verify_external.sh`: A script to verify external installation and usage of the package.
*   **New Features/Utilities:**
    *   `src/unified_data/utils.py`: Introduces `calculate_start_date` for robust date range calculation in adapters.
    *   `src/unified_data/api.py`: Unified adapter handling and exposes `Exchange` and `Columns` enums.

**Bugfix:**
*   **`src/unified_data/api.py`**: Ensures the 'exchange' column is consistently added to the output DataFrame from `pull_kline`.
*   **`src/unified_data/adapters/akshare_adapter.py`**: Improves date handling by using `calculate_start_date` when start/end dates are not provided.
*   **`src/unified_data/adapters/yfinance_adapter.py`**: Improves date handling by using `calculate_start_date` when start/end dates are not provided, and correctly passes parameters to `yf.download`.

**Refactor/Code Organization:**
*   **`src/unified_data/__init__.py`**: Exports `pull_kline`, `MarketType`, `Exchange`, and `Columns` for top-level access.
*   **`README.md`**: Updated to reflect the default limit of 200, the addition of the 'exchange' column, and example imports.
*   **`tests/test_verify_install.py`**: Added `MarketType` import.

What's New:
- Added `.gitignore` to exclude common Python and build artifacts.
- Added `.python-version` specifying Python 3.12.
- Added `__version__.py` with initial version `0.0.1`.
- Added `data_source.md` detailing kline data pulling requirements.
- Added `pyproject.toml` for project configuration and dependencies.
- Added `requirements.txt` listing core dependencies.
- Added `uv.lock` file for dependency management.
- Added `README.md` providing an overview, features, installation, and usage of the `unified-data` library.
- Added `utils.py` with a placeholder `get_logger` function.
- Added `src/api.py` with the main `pull_kline` entry point and adapter factory.
- Added `src/models/enums.py` defining `MarketType`, `Columns`, and `Exchange` enums.
- Added `src/adapters/base.py` defining the abstract `BaseAdapter`.
- Added `src/adapters/akshare_adapter.py` for fetching data using `akshare`.
- Added `src/adapters/ccxt_adapter.py` for fetching data using `ccxt`.
- Added `src/adapters/yfinance_adapter.py` for fetching data using `yfinance`.
- Added `tests/test_adapters_live.py` for live adapter testing.
- Added `tests/test_basic.py` for basic API dispatch tests.
- Added `tests/test_e2e.py` for end-to-end testing of the API.
- Added `tests/test_mocked.py` for mocked API tests.
