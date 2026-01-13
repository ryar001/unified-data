import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))


from unified_data.models.enums import MarketType, TimeFramePeriod
from unified_data.adapters.ccxt_strategies.binance import BinanceStrategy
from unified_data.adapters.ccxt_strategies.coinbase import CoinbaseStrategy

class TestCCXTStrategies(unittest.TestCase):

    def test_binance_symbol_conversion(self):
        strategy = BinanceStrategy()
        # BTC_USDT -> BTC/USDT
        symbol = strategy.get_exchange_symbol("BTC_USDT", MarketType.CRYPTO)
        self.assertEqual(symbol, "BTC/USDT")
        
        # Lower case input
        symbol = strategy.get_exchange_symbol("eth_usdt", MarketType.CRYPTO)
        self.assertEqual(symbol, "ETH/USDT")

    def test_binance_period_conversion(self):
        strategy = BinanceStrategy()
        self.assertEqual(strategy.to_exchange_period("1d"), "1d")
        self.assertEqual(strategy.to_exchange_period(TimeFramePeriod.M1), "1M")

    @patch('ccxt.coinbase')
    def test_coinbase_symbol_fallback(self, mock_ccxt_coinbase):
        # Setup mock exchange
        mock_exchange = MagicMock()
        mock_ccxt_coinbase.return_value = mock_exchange
        
        strategy = CoinbaseStrategy()
        
        # Test 1: Symbol exists exactly (BTC/USDT)
        mock_exchange.markets = {"BTC/USDT": {}, "BTC/USD": {}}
        symbol = strategy.get_exchange_symbol("BTC_USDT", MarketType.CRYPTO)
        self.assertEqual(symbol, "BTC/USDT") # Should keep USDT
        
        # Test 2: USDT Missing, USD Exists (SOL/USDT -> SOL/USD)
        mock_exchange.markets = {"SOL/USD": {}} # No SOL/USDT
        # Mock load_markets to not change markets (or just pass)
        mock_exchange.load_markets.return_value = mock_exchange.markets
        
        symbol = strategy.get_exchange_symbol("SOL_USDT", MarketType.CRYPTO)
        self.assertEqual(symbol, "SOL/USD") # Should fallback
        
        # Test 3: Neither exists (XYZ/USDT)
        mock_exchange.markets = {"SOL/USD": {}} # No XYZ
        symbol = strategy.get_exchange_symbol("XYZ_USDT", MarketType.CRYPTO)
        self.assertEqual(symbol, "XYZ/USDT") # Default behavior (no fallback found)

    def test_coinbase_period_conversion(self):
        strategy = CoinbaseStrategy()
        self.assertEqual(strategy.to_exchange_period("1d"), "1d")
        # Assuming defaults for now
        self.assertEqual(strategy.to_exchange_period("1w"), "1w")

if __name__ == '__main__':
    unittest.main()
