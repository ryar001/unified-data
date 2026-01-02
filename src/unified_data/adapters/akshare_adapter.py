import akshare as ak
import polars as pl
from datetime import datetime
from .base import BaseAdapter
from ..models.enums import Columns
from ..utils import get_logger, calculate_start_date

logger = get_logger("akshare_adapter")

class AKShareAdapter(BaseAdapter):
    def get_kline(
        self, 
        ticker: str, 
        period: str, 
        start_date: datetime | None = None, 
        end_date: datetime | None = None, 
        limit: int = 100
    ) -> pl.DataFrame:
        
        # 1. Prepare Dates (AKShare often expects 'YYYYMMDD' strings)
        if not end_date:
            end_date = datetime.now()
            
        if not start_date:
            start_date = calculate_start_date(end_date, limit, period)
            
        start_str = start_date.strftime("%Y%m%d")
        end_str = end_date.strftime("%Y%m%d")
        
        # 2. Get Exchange Symbol
        # We now rely on the caller or use internal helper if needed. 
        # But since get_kline receives the 'standard' ticker usually, 
        # we strictly should convert it here if it wasn't converted by caller. 
        # However, the design says pull_kline calls get_exchange_symbol.
        # But direct usage of get_kline might pass standard ticker.
        # Let's assume input 'ticker' IS the exchange symbol if it comes from internal,
        # OR we just handle it. Ideally, pull_kline does the work.
        # But to be safe and robust (and support direct use), let's ensure we work with what we have.
        
        # If the ticker has "=F", it likely hasn't been converted. 
        # (Though get_exchange_symbol is the right place for logic)
        symbol = ticker
        
        logger.info(f"Fetching {symbol} from AKShare ({period})")

        try:
            pdf = None
            
            # Simple Heuristic: 
            # If it ENDS with "0" and is alphanumeric (like RB0), it's likely a Future converted by us.
            # If it is numeric (000001), it's a Stock.
            
            # Additional check: If it still looks like "RB=F", try to convert it on the fly or fail?
            # Better to assume it's already converted or formatted correctly for the underlying call
            # properly by the time it gets here, BUT our new architecture demands flexibility.
            
            # Let's trust it's somewhat correct or we try standard calls.
            
            if symbol.isdigit():
                # stock_zh_a_hist: daily data
                adjust = "qfq" # Default forward adjust
                pdf = ak.stock_zh_a_hist(symbol=symbol, start_date=start_str, end_date=end_str, adjust=adjust)
                
            else:
                # Futures
                # e.g. "RB0", "AU2412"
                # try: ak.futures_zh_daily_sina(symbol=symbol)
                pdf = ak.futures_zh_daily_sina(symbol=symbol)

            if pdf is None or pdf.empty:
                logger.warning(f"No data returned for {symbol}")
                return pl.DataFrame()

            # 3. Normalize Columns
            rename_map = {
                "日期": Columns.TIMESTAMP.value,
                "date": Columns.TIMESTAMP.value,
                "开盘": Columns.OPEN.value,
                "open": Columns.OPEN.value,
                "最高": Columns.HIGH.value,
                "high": Columns.HIGH.value,
                "最低": Columns.LOW.value,
                "low": Columns.LOW.value,
                "收盘": Columns.CLOSE.value,
                "close": Columns.CLOSE.value,
                "成交量": Columns.VOLUME.value,
                "volume": Columns.VOLUME.value,
            }
            
            # Convert to Polars
            df = pl.from_pandas(pdf)
            
            # Rename
            existing_cols = df.columns
            final_map = {k: v for k, v in rename_map.items() if k in existing_cols}
            df = df.rename(final_map)
            
            # Date Parsing
            if Columns.TIMESTAMP.value in df.columns:
                col_type = df.schema[Columns.TIMESTAMP.value]
                if col_type == pl.Utf8 or col_type == pl.String:
                     df = df.with_columns(
                        pl.col(Columns.TIMESTAMP.value).str.strptime(pl.Date, "%Y-%m-%d").cast(pl.Datetime).dt.timestamp("ms")
                    )
                elif col_type == pl.Date:
                     df = df.with_columns(
                        pl.col(Columns.TIMESTAMP.value).cast(pl.Datetime).dt.timestamp("ms")
                    )
            
            # Add Symbol (Use original or exchanged? usually we want the standard one in output, 
            # but usually we return what we asked for. 'ticker' arg is best.)
            df = df.with_columns(pl.lit(ticker).alias(Columns.SYMBOL.value))

             # Select strictly
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

            if limit > 0:
                df = df.tail(limit)
                
            return df
            


        except Exception as e:
            logger.error(f"AKShare Error: {e}")
            return pl.DataFrame()

    def get_exchange_symbol(self, ticker: str, market_type: str) -> str:
        # Standard: RB=F (Front Month)
        # Akshare: RB0
        
        if ticker.endswith("=F"):
            # e.g. "RB=F" -> "RB0", "GC=F" -> "GC0"? No, AKShare usually generic is just symbol+0?
            # Actually for Chinese futures, dominant contract is often "V0" e.g. "RB0".
            # Let's assume the prefix is the symbol.
            base = ticker.split("=")[0]
            return f"{base}0"
            
        # Standard: RB2410 (Specific) -> Akshare: RB2410 (often same)
        # But we need to be careful.
        # If it's a Stock, e.g. "000001", it stays "000001".
        
        return ticker
