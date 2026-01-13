import ccxt
from ...models.enums import MarketType, TimeFramePeriod
from .base import BaseCCXTStrategy

class BinanceStrategy(BaseCCXTStrategy):
    """Binance specific implementation."""

    def _initialize_exchange(self) -> ccxt.Exchange:
        return ccxt.binance()

    def get_exchange_symbol(self, ticker: str, market_type: MarketType | str) -> str:
        # Standard: BTC_USDT -> CCXT: BTC/USDT
        ticker = ticker.upper()
        return ticker.replace("_", "/")

    def to_exchange_period(self, period: str) -> str:
        # Standard: 1d, 1w, 1M (Monthly)
        # CCXT Binance: 1d, 1w, 1M
        
        if period == TimeFramePeriod.M1: # "1M"
            return "1M"
        if period == "1m": # Explicit minute handling if passed raw
             return "1m"
        if period == TimeFramePeriod.W1:
            return "1w"
        if period == TimeFramePeriod.D1:
            return "1d"
            
        return period
