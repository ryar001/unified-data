from abc import ABC, abstractmethod

import ccxt
from ...models.enums import MarketType

class BaseCCXTStrategy(ABC):
    """Abstract base class for CCXT exchange strategies."""
    
    def __init__(self):
        self._exchange = self._initialize_exchange()

    @abstractmethod
    def _initialize_exchange(self) -> ccxt.Exchange:
        """Initialize and return the specific CCXT exchange instance."""
        pass

    def get_exchange(self) -> ccxt.Exchange:
        """Return the initialized exchange instance."""
        return self._exchange

    @abstractmethod
    def get_exchange_symbol(self, ticker: str, market_type: MarketType | str) -> str:
        """Convert standard ticker to exchange-specific symbol."""
        pass

    @abstractmethod
    def to_exchange_period(self, period: str) -> str:
        """Convert standard period to exchange-specific period."""
        pass
