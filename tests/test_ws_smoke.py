import pytest
import asyncio
from unittest.mock import MagicMock, patch, AsyncMock
import sys
import os
sys.path.insert(0, os.path.abspath("src"))

from unified_data.ws_api import sub_live_price, _ADAPTERS
from unified_data.models.enums import Exchange

@pytest.mark.asyncio
async def test_sub_live_price_flow():
    with patch("unified_data.ws_adapters.tqsdk_adapter.TqApi") as MockApi:
        mock_api_instance = MockApi.return_value
        mock_api_instance.__aenter__ = AsyncMock(return_value=mock_api_instance)
        mock_api_instance.__aexit__ = AsyncMock(return_value=None)
        
        async def fake_wait():
            await asyncio.sleep(0.01)
        mock_api_instance.wait_update = AsyncMock(side_effect=fake_wait)
        mock_api_instance.get_quote = MagicMock(return_value=MagicMock())
        mock_api_instance.is_changing = MagicMock(return_value=False)
        
        callback = AsyncMock()
        
        print("Calling subscribe")
        await sub_live_price(
            ticker="SHFE.rb2505", 
            market_type="futures", 
            exchange="tqsdk", 
            callback=callback
        )
        print("Subscribed returning")
        
        mock_api_instance.get_quote.assert_called_with("SHFE.rb2505")
        adapter = _ADAPTERS[Exchange.TQSDK]
        assert adapter._running is True
        
        print("Sleeping")
        await asyncio.sleep(0.05)
        print("Waking")
        
        adapter._running = False
        if adapter._task:
            print("Awaiting task")
            await adapter._task
            print("Task done")
