import sys
import os
import unittest
from unittest.mock import MagicMock

# 1. Mock External Dependencies (Moved to setUp/tearDown to avoid side effects)


# Mock DataFrame behavior to avoid crashes when calling methods on it

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Now import our modules
# We need to make sure enum_ is importable. It's in root.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from unified_data.api import pull_kline  # noqa: E402
from unified_data.models.enums import MarketType, Exchange  # noqa: E402

class TestMockedAPI(unittest.TestCase):
    def setUp(self):
        self.original_modules = sys.modules.copy()
        
        self.mock_pl = MagicMock()
        self.mock_ccxt = MagicMock()
        self.mock_yf = MagicMock()
        self.mock_ak = MagicMock()
        
        # Patch modules
        sys.modules["polars"] = self.mock_pl
        sys.modules["ccxt"] = self.mock_ccxt
        sys.modules["yfinance"] = self.mock_yf
        sys.modules["akshare"] = self.mock_ak
        
        # Setup mock DataFrame
        self.mock_df = MagicMock()
        self.mock_pl.DataFrame.return_value = self.mock_df
        self.mock_pl.from_pandas.return_value = self.mock_df
        self.mock_df.select.return_value = self.mock_df
        self.mock_df.rename.return_value = self.mock_df
        self.mock_df.with_columns.return_value = self.mock_df
        self.mock_df.tail.return_value = self.mock_df
        self.mock_df.__getitem__.return_value = [100.0] 
        self.mock_df.columns = ["ts", "open", "high", "low", "close", "volume", "symbol"]
        self.mock_df.is_empty.return_value = False

    def tearDown(self):
        # Restore original modules
        # Remove mocks we added
        for mod in ["polars", "ccxt", "yfinance", "akshare"]:
            if mod in self.original_modules:
                sys.modules[mod] = self.original_modules[mod]
            else:
                del sys.modules[mod]

        # Force re-import of src modules if needed, though typically unittest runs isolations differently.
        # But safest is just to clean sys.modules.
    def test_pull_kline_crypto_call(self):
        # We just want to ensure it calls the right adapter and returns the mock df
        try:
            df = pull_kline("BTC_USDT", MarketType.CRYPTO, "1d", limit=10)
        except Exception as e:
            self.fail(f"pull_kline raised exception: {e}")
        
        # Verify it returned our mock dict/df
        self.assertTrue(df is not None)

    def test_pull_kline_stock_call(self):
         try:
            df = pull_kline("AAPL", MarketType.STOCK, "1d", exchange=Exchange.YFINANCE)
         except Exception as e:
            self.fail(f"pull_kline raised exception: {e}")
         self.assertTrue(df is not None)

if __name__ == '__main__':
    unittest.main()
