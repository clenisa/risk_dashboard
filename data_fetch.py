import yfinance as yf
import pandas as pd

def get_asset_data(tickers, period="1y"):
    """Fetch historical price data for multiple assets from Yahoo Finance."""
    if isinstance(tickers, str):  # Convert single ticker input to list
        tickers = [tickers]

    data = {}
    for ticker in tickers:
        try:
            asset = yf.Ticker(ticker)
            history = asset.history(period=period)

            if history.empty:
                print(f"❌ No data found for {ticker}. Check if the symbol is correct.")
            else:
                data[ticker] = history['Close']
        except Exception as e:
            print(f"❌ Error fetching data for {ticker}: {e}")

    return pd.DataFrame(data)  # Return all price data as a DataFrame