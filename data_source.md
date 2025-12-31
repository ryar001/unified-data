# Unified Kline Data Pulling Requirements

## Overview
This project aims to build a unified interface for pulling kline (candlestick) data from various financial markets (Crypto, Stocks, Futures). The system will normalize inputs into a standard format and handle exchange-specific translations internally.

## 1. Main Entry Interface
 The system provides a single main entry point for data retrieval.

**Function Signature**
```python
import polars as pl
from datetime import datetime

def pull_kline(
    ticker: str, 
    market_type: str, 
    period: str, 
    start_date: datetime | str = None, 
    end_date: datetime | str = None, 
    limit: int = 100,
    exchange: str = None
) -> pl.DataFrame:
    ...
```

**Parameters**
- **`ticker`**: Standardized asset symbol (see Section 2).
- **`market_type`**: The class of the asset (e.g., Crypto, Stock).
- **`period`**: Time interval for the data.
- **`start_date`**: Start time for data retrieval.
- **`end_date`**: End time for data retrieval.
- **`limit`**: Maximum number of records to return (Default: 100).
- **`exchange`** *(Optional)*: Specific exchange to source data from. If None, defaults are used.

**Return Type**
- Must return a **Polars DataFrame**.

---

## 2. Standardized Input Formats
All inputs must serve as a universal language for the system. Lower-level adapters will translate these to specific API requirements.

### Ticker Standards
| Market Type | Format Pattern | Example | Description |
| :--- | :--- | :--- | :--- |
| **Crypto** | `[SYMBOL]_[QUOTE]` | `BTC_USDT` | Standard pair with underscore separator. |
| **Stocks** | `[SYMBOL]` | `AAPL` | Common ticker symbol. |
| **Futures (Front)**| `[SYMBOL]=F` | `GC=F` | Continuous/Front month contract. |
| **Futures (Specific)**| `[SYMBOL][MONTH][YY]` | `GCU26` | Specific expiry (e.g., Gold September 2026). |

### Month Codes (Futures)
| Code | Month | Code | Month | Code | Month |
| :--- | :--- | :--- | :--- | :--- | :--- |
| F | January | K | May | U | September |
| G | February | M | June | V | October |
| H | March | N | July | X | November |
| J | April | Q | August | Z | December |

---

## 3. Data Source Architecture
The system uses a plug-in adapter pattern with the following default sources:

| Market Type | Region/Sub-type | Source Library | Notes |
| :--- | :--- | :--- | :--- |
| **Crypto** | Global | `ccxt` | Free market data. |
| **Stocks** | USA | `yfinance` | Free market data. |
| **Stocks** | China | `akshare` | Free market data. |
| **Futures** | China | `akshare` | Free market data. |
| **Futures** | Global/USA | `yfinance` | Free market data. |

- **Strategy**:
    - **Input Conversion**: Adapters convert the standard `BTC_USDT` to their API specific format (e.g., `BTC/USDT`, `BTC-USD`).
    - **Output Normalization**: Adapters MUST return a Polars DataFrame with standardized column names defined in `enum.py`.

---

## 4. Centralized Constants (`enum.py`)
To maintain strict type safety and consistency, all string literals must be stored in `enum.py` using `StrEnum`.

**Requirements**:
- **NO** magic strings in the logic code.
- **ALL** DataFrame columns keys must be imported from `enum.py`.

### Example `enum.py` Spec
```python
from enum import StrEnum

class MarketType(StrEnum):
    CRYPTO = "crypto"
    STOCK = "stock"
    FUTURES = "futures"

class Columns(StrEnum):
    TIMESTAMP = "ts"
    OPEN = "open"
    HIGH = "high"
    LOW = "low"
    CLOSE = "close"
    VOLUME = "vol"
    SYMBOL = "symbol"
```

---

## 5. Logging
Use the `logging_utils` from `dev_utils` package.
- Repo: `https://github.com/ryar001/dev_utils`
- Ensure standardized logging across all adapters.