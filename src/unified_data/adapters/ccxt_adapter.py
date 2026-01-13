
import polars as pl
from datetime import datetime
from .base import BaseAdapter
from ..models.enums import Columns, MarketType, CcxtExchange
from ..utils import get_logger
from .ccxt_strategies.base import BaseCCXTStrategy
from .ccxt_strategies.binance import BinanceStrategy
from .ccxt_strategies.coinbase import CoinbaseStrategy

logger = get_logger("ccxt_adapter")

class CCXTAdapter(BaseAdapter):
    def __init__(self, exchange_id: str | CcxtExchange = CcxtExchange.BINANCE):
        self.exchange_id = str(exchange_id).lower()
        self.strategy: BaseCCXTStrategy = self._get_strategy()
        
    def _get_strategy(self) -> BaseCCXTStrategy:
        if self.exchange_id == CcxtExchange.BINANCE:
            return BinanceStrategy()
        elif self.exchange_id == CcxtExchange.COINBASE:
            return CoinbaseStrategy()
        else:
            # Fallback or error - for now fallback to trying dynamic loading or error
            # If we want strict typing we raise error
            raise ValueError(f"Unsupported CCXT exchange strategy: {self.exchange_id}")

    def get_kline(
        self, 
        ticker: str, 
        period: str, 
        start_date: datetime | None = None, 
        end_date: datetime | None = None, 
        limit: int = 100,
        market_type: MarketType | str | None = None
    ) -> pl.DataFrame:
        
        # 1. Parse ticker via strategy
        market_type = market_type or MarketType.CRYPTO
        symbol = self.strategy.get_exchange_symbol(ticker, market_type)
        
        # 2. Get Exchange instance from strategy
        exchange = self.strategy.get_exchange()
        
        # 3. Handle Time parameters
        since = None
        if start_date:
            if isinstance(start_date, str):
                try:
                    dt = datetime.fromisoformat(start_date)
                    since = int(dt.timestamp() * 1000)
                except ValueError:
                    logger.warning(f"Could not parse start_date: {start_date}")
            elif isinstance(start_date, datetime):
                since = int(start_date.timestamp() * 1000)

        # Convert period via strategy
        exchange_period = self.strategy.to_exchange_period(period)
        logger.info(f"Fetching {symbol} {exchange_period} from CCXT ({self.exchange_id}) (since={since}, limit={limit})")
        
        try:
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe=exchange_period, since=since, limit=limit)
        except Exception as e:
            logger.error(f"CCXT Error: {e}")
            raise

        if not ohlcv:
            logger.warning(f"No data returned for {symbol}")
            return pl.DataFrame()

        # 4. Convert to Polars DataFrame
        data = {
            Columns.TIMESTAMP.value: [x[0] for x in ohlcv],
            Columns.OPEN.value: [x[1] for x in ohlcv],
            Columns.HIGH.value: [x[2] for x in ohlcv],
            Columns.LOW.value: [x[3] for x in ohlcv],
            Columns.CLOSE.value: [x[4] for x in ohlcv],
            Columns.VOLUME.value: [x[5] for x in ohlcv],
            Columns.SYMBOL.value: [ticker] * len(ohlcv)
        }
        
        df = pl.DataFrame(data)
        
        # Optional: Cast types if needed
        df = df.with_columns(
            pl.col(Columns.TIMESTAMP.value).cast(pl.Int64),
            pl.col(Columns.OPEN.value).cast(pl.Float64),
            pl.col(Columns.HIGH.value).cast(pl.Float64),
            pl.col(Columns.LOW.value).cast(pl.Float64),
            pl.col(Columns.CLOSE.value).cast(pl.Float64),
            pl.col(Columns.VOLUME.value).cast(pl.Float64)
        )

        return df

    def get_exchange_symbol(self, ticker: str, market_type: str) -> str:
        return self.strategy.get_exchange_symbol(ticker, market_type)

    def to_exchange_period(self, period: str) -> str:
        return self.strategy.to_exchange_period(period)
