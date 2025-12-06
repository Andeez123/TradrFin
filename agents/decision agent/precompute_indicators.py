import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

def calculate_rsi(series, period=14):
    """Calculate RSI for a price series."""
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(50)

def calculate_movement_score(series, period=20):
    """Calculate movement score (0-1) based on position relative to SMA."""
    sma = series.rolling(window=period).mean()
    std = series.rolling(window=period).std()
    
    # Z-score-like metric: (Price - SMA) / (2 * STD)
    # Clipped to -1 to 1, then scaled to 0 to 1
    z_score = (series - sma) / (2 * std)
    movement_score = ((z_score.clip(-1, 1) + 1) / 2).fillna(0.5)
    return movement_score

def precompute_indicators(symbols, period="3mo"):
    """
    Precompute RSI and Movement Score for multiple symbols.
    
    Args:
        symbols: List of stock symbols
        period: How far back to fetch data (default: 3 months)
    
    Returns:
        Dictionary mapping symbol to DataFrame with indicators
    """
    results = {}
    
    for symbol in symbols:
        print(f"Processing {symbol}...")
        try:
            # Fetch data - need more history for indicator calculation
            ticker = yf.Ticker(symbol)
            df = ticker.history(period="1mo", interval="1d")  # Fetch 1 month to calculate indicators
            
            if df.empty:
                print(f"  ⚠️  No data for {symbol}")
                continue
            
            # Calculate indicators
            df['RSI'] = calculate_rsi(df['Close'])
            df['Movement_Score'] = calculate_movement_score(df['Close'])
            
            # Keep only the last few days based on requested period
            if period == "5d":
                df_clean = df.tail(5)
            elif period == "3d":
                df_clean = df.tail(3)
            else:
                df_clean = df
            
            # Keep only relevant columns - just Price and indicators
            df_clean = df_clean[['Close', 'RSI', 'Movement_Score']].copy()
            
            # Rename Close to Price
            df_clean.rename(columns={'Close': 'Price'}, inplace=True)
            
            # Get latest values
            latest = df_clean.iloc[-1]
            print(f"  ✓ {symbol}: Price=${latest['Price']:.2f}, RSI={latest['RSI']:.2f}, Movement={latest['Movement_Score']:.3f}")
            
            results[symbol] = df_clean
            
        except Exception as e:
            print(f"  ✗ Error processing {symbol}: {e}")
    
    return results

def save_to_csv(results, output_dir="."):
    """Save precomputed indicators to CSV files."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    for symbol, df in results.items():
        filename = f"{output_dir}/{symbol}_indicators_{timestamp}.csv"
        df.to_csv(filename)
        print(f"Saved {symbol} to {filename}")

def save_latest_to_json(results, output_file="latest_indicators.json"):
    """Save only the latest indicator values to a JSON file."""
    import json
    
    latest_data = {}
    for symbol, df in results.items():
        latest = df.iloc[-1]
        latest_data[symbol] = {
            "price": float(latest['Price']),
            "rsi": float(latest['RSI']),
            "movement_score": float(latest['Movement_Score']),
            "timestamp": df.index[-1].strftime("%Y-%m-%d %H:%M:%S")
        }
    
    with open(output_file, 'w') as f:
        json.dump(latest_data, f, indent=2)
    
    print(f"\nSaved latest indicators to {output_file}")

if __name__ == "__main__":
    # Define symbols to process
    symbols = ["AAPL", "TSLA", "GOOG", "AMZN", "MSFT"]
    
    print("=" * 60)
    print("Precomputing Indicators for Multiple Stocks")
    print("=" * 60)
    
    # Precompute indicators (5d to get ~3 trading days of advance data)
    results = precompute_indicators(symbols, period="5d")
    
    # Save to CSV files
    print("\n" + "=" * 60)
    print("Saving to CSV files...")
    print("=" * 60)
    save_to_csv(results)
    
    # Save latest values to JSON
    print("\n" + "=" * 60)
    print("Saving latest values to JSON...")
    print("=" * 60)
    save_latest_to_json(results)
    
    print("\n✓ Done!")
