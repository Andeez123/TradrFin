import yfinance as yf
import pandas as pd

def get_historical_data(symbol: str, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
    """
    Fetch historical price data using yfinance.
    
    Args:
        symbol (str): Stock symbol (e.g., 'AAPL', 'TSLA', 'MSFT')
        period (str): How far back to fetch. Examples:
                      '1mo', '3mo', '6mo', '1y', '2y', '5y', 'max'
        interval (str): Candle interval. Examples:
                        '1m','5m','15m','1h','1d','1wk','1mo'
    
    Returns:
        pd.DataFrame: Historical OHLCV data.
    """
    ticker = yf.Ticker(symbol)
    df = ticker.history(period=period, interval=interval)

    # Ensure we got valid data
    if df.empty:
        raise ValueError(f"No data returned for {symbol}. Check symbol or interval.")

    return df


if __name__ == "__main__":
    # Example usage:
    symbol = "AAPL"
    df = get_historical_data(symbol, period="1y", interval="1d")
    print(df.head())
    print(df.tail())
    df.to_csv(f"{symbol}_historical_data.csv")