import numpy as np

def sharpe_ratio(returns, risk_free_rate=0.02):
    """Calculate Sharpe Ratio."""
    excess_returns = returns - risk_free_rate / 252  # Convert annual rate to daily
    return np.mean(excess_returns) / np.std(excess_returns)

def sortino_ratio(returns, risk_free_rate=0.02):
    """Calculate Sortino Ratio (only downside risk)."""
    downside_returns = returns[returns < 0]
    if len(downside_returns) == 0:
        return np.nan  # Avoid division by zero
    return np.mean(returns - risk_free_rate / 252) / np.std(downside_returns)

def max_drawdown(prices):
    """Calculate Maximum Drawdown."""
    peak = prices.cummax()
    drawdown = (prices - peak) / peak
    return drawdown.min()

def calmar_ratio(returns, prices):
    """Calculate Calmar Ratio (Return over Max Drawdown)."""
    annual_return = np.mean(returns) * 252  # Annualized return
    return annual_return / abs(max_drawdown(prices))

# Testing the functions
if __name__ == "__main__":
    from data_fetch import get_stock_data, get_crypto_data
    import pandas as pd

    # Fetch sample data
    stock_prices = get_stock_data("AAPL")
    crypto_prices = get_crypto_data("bitcoin")

    # Calculate daily returns
    stock_returns = np.log(stock_prices / stock_prices.shift(1)).dropna()
    crypto_returns = np.log(crypto_prices / crypto_prices.shift(1)).dropna()

    # Compute Metrics
    print(f"📊 AAPL Sharpe Ratio: {sharpe_ratio(stock_returns):.2f}")
    print(f"📉 AAPL Sortino Ratio: {sortino_ratio(stock_returns):.2f}")
    print(f"🔥 AAPL Calmar Ratio: {calmar_ratio(stock_returns, stock_prices):.2f}")
    print(f"📉 AAPL Max Drawdown: {max_drawdown(stock_prices):.2%}")

    print("\n")

    print(f"📊 BTC Sharpe Ratio: {sharpe_ratio(crypto_returns):.2f}")
    print(f"📉 BTC Sortino Ratio: {sortino_ratio(crypto_returns):.2f}")
    print(f"🔥 BTC Calmar Ratio: {calmar_ratio(crypto_returns, crypto_prices):.2f}")
    print(f"📉 BTC Max Drawdown: {max_drawdown(crypto_prices):.2%}")