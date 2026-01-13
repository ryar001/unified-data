import ccxt
from ...models.enums import MarketType, TimeFramePeriod
from .base import BaseCCXTStrategy

class CoinbaseStrategy(BaseCCXTStrategy):
    """Coinbase specific implementation."""

    def _initialize_exchange(self) -> ccxt.Exchange:
        return ccxt.coinbase()

    def get_exchange_symbol(self, ticker: str, market_type: MarketType | str) -> str:
        # Standard: BTC_USDT -> CCXT: BTC/USDT
        # Coinbase usually pairs with USD, not USDT for fiat pairs, but accepts standard slash format
        ticker = ticker.upper()
        symbol = ticker.replace("_", "/")
        
        # Check if we need to fallback from USDT to USD
        # Only check if the symbol ends with /USDT
        if symbol.endswith("/USDT"):
            # Ensure markets are loaded
            if not self._exchange.markets:
                try:
                    self._exchange.load_markets()
                except Exception:
                    # If network fails, fallback to default symbol
                    return symbol
                    
            if symbol not in self._exchange.markets:
                # Try replacing USDT with USD
                alt_symbol = symbol.replace("/USDT", "/USD")
                if alt_symbol in self._exchange.markets:
                    return alt_symbol
                    
        return symbol

    def to_exchange_period(self, period: str) -> str:
        # Coinbase specific timeframes if different, otherwise standard
        
        if period == TimeFramePeriod.M1: # "1M"
            return "1M" # Check if supported, usually is
        if period == "1m": 
             return "1m"
        if period == TimeFramePeriod.W1:
            return "1w"
        if period == TimeFramePeriod.D1:
            return "1d"
            
        return period
