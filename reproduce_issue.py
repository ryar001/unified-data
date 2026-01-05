
from unified_data.adapters.akshare_adapter import AKShareAdapter

def reproduce():
    adapter = AKShareAdapter()
    try:
        # User reported: ValueError: Length mismatch: Expected axis has 0 elements, new values have 8 elements
        # This likely happens when data is empty but we try to rename/set columns
        
        # Simulating a "wrong symbol" that returns empty or unexpected shape
        print("Attempting to fetch with a wrong symbol...")
        df = adapter.get_kline(ticker="WRONG_SYMBOL", period="daily")
        print("Result:")
        print(df)
    except Exception as e:
        print(f"Caught expected exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    reproduce()
