import sys
import os
import unittest
from datetime import datetime, timedelta

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from unified_data.api import pull_kline
from unified_data.models.enums import MarketType

class TestLimitAdvanced(unittest.TestCase):
    """
    Advanced tests for the 'limit' parameter across different vendors and edge cases.
    """

    def test_limit_one(self):
        """Verify limit=1 returns exactly one row."""
        for mt in [MarketType.CRYPTO, MarketType.STOCK]:
            ticker = "BTC_USDT" if mt == MarketType.CRYPTO else "AAPL"
            df = pull_kline(ticker, mt, "1d", limit=1)
            self.assertEqual(len(df), 1, f"Failed for {mt} with limit=1")

    def test_limit_large(self):
        """Verify limit=500 (larger than default) works."""
        # Using Stock for this as it has plenty of history
        df = pull_kline("AAPL", MarketType.STOCK, "1d", limit=500)
        self.assertEqual(len(df), 500)

    def test_limit_intraday(self):
        """Verify limit works with intraday periods."""
        # CCXT supports 1h easily
        df = pull_kline("BTC_USDT", MarketType.CRYPTO, "1h", limit=50)
        self.assertEqual(len(df), 50)

    def test_limit_and_start_date_combined(self):
        """
        Verify that when both start_date and limit are provided, 
        limit acts as a tail on the resulting range.
        Fetch 100 days of data but limit to 5.
        """
        end = datetime.now()
        start = end - timedelta(days=100)
        
        df = pull_kline(
            "AAPL", 
            MarketType.STOCK, 
            "1d", 
            start_date=start, 
            end_date=end, 
            limit=5
        )
        self.assertEqual(len(df), 5)
        
    def test_limit_exceeding_availability(self):
        """
        Verify behavior when limit is larger than available data.
        (e.g. asking for 10000 days of a new asset).
        It should return as much as possible without error.
        """
        # Pick something likely to have less than 5000 days of history if possible, 
        # or just check it doesn't crash.
        df = pull_kline("AAPL", MarketType.STOCK, "1d", limit=10000)
        # AAPL has more than 10k days, but we should at least get a lot or exactly 10k.
        self.assertTrue(len(df) > 0)
        self.assertTrue(len(df) <= 10000)

if __name__ == "__main__":
    unittest.main()
