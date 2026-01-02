import sys
import os
import unittest

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from unified_data.api import pull_kline
from unified_data.models.enums import MarketType, Exchange

class TestLimitLogic(unittest.TestCase):
    """
    Test that the 'limit' parameter is strictly enforced and works as expected.
    """

    def test_crypto_limit(self):
        """Test crypto kline respects limit (CCXT)."""
        limit = 10
        df = pull_kline(
            ticker="BTC_USDT",
            market_type=MarketType.CRYPTO,
            period="1d",
            limit=limit
        )
        self.assertEqual(len(df), limit)

    def test_stock_limit_yfinance(self):
        """Test stock kline respects limit (YFinance)."""
        limit = 50
        df = pull_kline(
            ticker="AAPL",
            market_type=MarketType.STOCK,
            period="1d",
            limit=limit
        )
        # Sometimes yfinance might return slightly less if data is not available, 
        # but for AAPL daily 50 rows should be fine.
        self.assertEqual(len(df), limit)

    def test_stock_limit_akshare(self):
        """Test stock kline respects limit (AKShare)."""
        limit = 20
        # "000001" is Ping An Bank
        df = pull_kline(
            ticker="000001",
            market_type=MarketType.STOCK,
            period="daily",
            limit=limit,
            exchange=Exchange.AKSHARE
        )
        self.assertEqual(len(df), limit)

    def test_default_limit(self):
        """Test default limit is 200."""
        df = pull_kline(
            ticker="BTC_USDT",
            market_type=MarketType.CRYPTO,
            period="1d"
        )
        self.assertEqual(len(df), 200)

if __name__ == '__main__':
    unittest.main()
