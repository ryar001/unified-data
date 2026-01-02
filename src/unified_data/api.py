import polars as pl
from datetime import datetime
from .models.enums import MarketType, Exchange, Columns
from .adapters.base import BaseAdapter
from .utils import get_logger

logger = get_logger("data_api")

def _get_adapter(market_type: str, exchange: str | None) -> tuple[BaseAdapter, str]:
    """Factory to get the correct adapter instance and the resolved exchange name."""
    
    # Default routing logic
    if exchange is None:
        if market_type == MarketType.CRYPTO:
            exchange = Exchange.CCXT
        elif market_type == MarketType.STOCK:
            exchange = Exchange.YFINANCE # Default to US stocks
            # Logic could be more complex here to detect China stocks if needed, 
            # but usually 'exchange' or specific logic handles it.
        elif market_type == MarketType.FUTURES:
            exchange = Exchange.YFINANCE
        else:
            raise ValueError(f"Unsupported market type: {market_type}")

    # Dispatch to specific adapters
    # Note: Imports are inside to avoid circular deps or heavy load if not needed
    if exchange == Exchange.CCXT:
        from .adapters.ccxt_adapter import CCXTAdapter
        return CCXTAdapter(), exchange
    elif exchange == Exchange.YFINANCE:
        from .adapters.yfinance_adapter import YFinanceAdapter
        return YFinanceAdapter(), exchange
    elif exchange == Exchange.AKSHARE:
        from .adapters.akshare_adapter import AKShareAdapter
        return AKShareAdapter(), exchange
    else:
        raise ValueError(f"Unsupported exchange: {exchange}")

def pull_kline(
    ticker: str, 
    market_type: str, 
    period: str, 
    start_date: datetime | str | None = None, 
    end_date: datetime | str | None = None, 
    limit: int = 200,
    exchange: str | None = None
) -> pl.DataFrame:
    """
    Main entry point to pull kline data.
    
    Args:
        ticker: Standardized ticker symbol.
        market_type: 'crypto', 'stock', 'futures' (use MarketType enum).
        period: Time period (e.g., '1d', '1h').
        start_date: Start datetime object or string.
        end_date: End datetime object or string.
        limit: Max records.
        exchange: Optional exchange name.

    Returns:
        polars.DataFrame: Standardized OHLCV data.
    """
    logger.info(f"Pulling kline for {ticker} ({market_type}) exchange={exchange}")
    
    try:
        adapter, exchange_name = _get_adapter(market_type, exchange)
        df = adapter.get_kline(ticker, period, start_date, end_date, limit)
        
        if not df.is_empty():
            df = df.with_columns(pl.lit(exchange_name).alias(Columns.EXCHANGE.value))

        return df
    except Exception as e:
        logger.error(f"Failed to pull data: {e}")
        raise
