import yfinance as yf
import polars as pl
from datetime import datetime
from .base import BaseAdapter
from ..models.enums import Columns
from ..utils import get_logger, calculate_start_date

logger = get_logger("yfinance_adapter")

class YFinanceAdapter(BaseAdapter):
    def get_kline(
        self, 
        ticker: str, 
        period: str, 
        start_date: datetime | None = None, 
        end_date: datetime | None = None, 
        limit: int = 200
    ) -> pl.DataFrame:
        
        # 1. Ticker is usually consistent (AAPL, GC=F), but ensure safe string
        symbol = ticker
        
        logger.info(f"Fetching {symbol} {period} from YFinance")
        
        try:
            # YF usage: download(tickers, period, interval, start, end)
            interval = period
            
            if not end_date:
                end_date = datetime.now()
            
            if not start_date:
                start_date = calculate_start_date(end_date, limit, period)
            
            kwargs = {
                "interval": interval, 
                "progress": False,
                "start": start_date,
                "end": end_date
            }

            pdf = yf.download(symbol, **kwargs)
            
            if pdf.empty:
                logger.warning(f"No data returned for {symbol}")
                return pl.DataFrame()
            
            # Flatten MultiIndex if necessary (yfinance sometimes returns MultiIndex for columns)
            if isinstance(pdf.columns, (list, tuple)) or hasattr(pdf.columns, "levels"):
                 if hasattr(pdf.columns, "get_level_values"):
                    pdf.columns = pdf.columns.get_level_values(0)

            # Reset index to get Date/Datetime as column
            pdf = pdf.reset_index()
            
            # 2. Convert to Polars
            df = pl.from_pandas(pdf)
            
            # 3. Standardize Columns
            # YF cols: Date (or Datetime), Open, High, Low, Close, Adj Close, Volume
            # Standardize names to lowercase first to be safe
            df = df.select(pl.all().name.to_lowercase())
            
            # Rename map
            rename_map = {
                "date": Columns.TIMESTAMP.value,
                "datetime": Columns.TIMESTAMP.value,
                "open": Columns.OPEN.value,
                "high": Columns.HIGH.value,
                "low": Columns.LOW.value,
                "close": Columns.CLOSE.value,
                "volume": Columns.VOLUME.value,
            }
            
            # Filter valid keys that exist in df
            existing_cols = df.columns
            final_map = {k: v for k, v in rename_map.items() if k in existing_cols}
            
            df = df.rename(final_map)
            
            # Ensure TIMESTAMP is proper int (ms) if it's datetime
            # YF usually gives Date or Datetime
            if Columns.TIMESTAMP.value in df.columns:
                df = df.with_columns(
                   pl.col(Columns.TIMESTAMP.value).cast(pl.Datetime).dt.timestamp("ms").alias(Columns.TIMESTAMP.value)
                )

            # Add Symbol
            df = df.with_columns(pl.lit(ticker).alias(Columns.SYMBOL.value))
            
            # Select only required columns (handling missing optional ones gracefully if needed)
            # For now select strictly
            required = [
                Columns.TIMESTAMP.value, 
                Columns.OPEN.value, 
                Columns.HIGH.value, 
                Columns.LOW.value, 
                Columns.CLOSE.value, 
                Columns.VOLUME.value,
                Columns.SYMBOL.value
            ]
            
            df = df.select([c for c in required if c in df.columns])
            
            # Apply limit
            if limit > 0:
                df = df.tail(limit)

            return df

        except Exception as e:
            logger.error(f"YFinance Error: {e}")
            raise
