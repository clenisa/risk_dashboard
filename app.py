import streamlit as st
import pandas as pd
import numpy as np
from data_fetch import get_asset_data
from risk_metrics import sharpe_ratio, sortino_ratio, calmar_ratio, max_drawdown

st.title("📈 Multi-Asset Risk Dashboard")

# User enters multiple tickers (stocks & cryptos)
tickers = st.text_input("Enter stock & crypto tickers (comma-separated, e.g., AAPL, BTC-USD, ETH-USD)")

if tickers:
    ticker_list = [t.strip().upper() for t in tickers.split(",")]  # Clean input

    # Fetch price data
    prices = get_asset_data(ticker_list)

    if not prices.empty:
        st.subheader("📊 Risk Metrics")

        metrics = []
        for ticker in prices.columns:
            returns = np.log(prices[ticker] / prices[ticker].shift(1)).dropna()
            
            metrics.append({
                "Asset": ticker,
                "Sharpe Ratio": round(sharpe_ratio(returns), 2),
                "Sortino Ratio": round(sortino_ratio(returns), 2),
                "Calmar Ratio": round(calmar_ratio(returns, prices[ticker]), 2),
                "Max Drawdown (%)": round(max_drawdown(prices[ticker]) * 100, 2)
            })

        df_metrics = pd.DataFrame(metrics)
        st.dataframe(df_metrics)  # Show risk metrics in a table

        # Show price chart
        st.subheader("📈 Price Data")
        st.line_chart(prices)

        # Export to CSV
        st.download_button(
            label="📥 Download CSV",
            data=prices.to_csv().encode("utf-8"),
            file_name="asset_prices.csv",
            mime="text/csv"
        )

    else:
        st.warning("❌ No data found. Check tickers and try again.")