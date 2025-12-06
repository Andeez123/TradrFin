import pandas as pd
import numpy as np
import yfinance as yf
import asyncio
from typing import Dict, Any, List
from datetime import datetime
import json
import matplotlib.pyplot as plt

# Import local modules
import decision_agent
import execution_agent
from get_historical import get_historical_data

class Backtester:
    def __init__(self, symbol: str, initial_capital: float = 10000.0, 
                 start_date: str = None, end_date: str = None, 
                 fee: float = 1.0, period: str = "1y"):
        self.symbol = symbol
        self.initial_capital = initial_capital
        self.investment_balance = initial_capital
        self.portfolio = {}  # {symbol: {"shares": int, "avg_cost": float}}
        self.fee = fee
        self.period = period
        self.start_date = start_date
        self.end_date = end_date
        
        self.history = []  # List of daily portfolio states
        self.trades = []   # List of executed trades
        self.data = None

    def load_data(self):
        """Fetch data and calculate indicators."""
        print(f"Fetching data for {self.symbol}...")
        # Use existing get_historical_data function
        # If start/end dates are provided, we might need to slice the dataframe or use yf.download directly
        # For simplicity, we'll use the period argument if start_date is not specific enough for get_historical_data
        # But get_historical_data uses period/interval. Let's stick to that for now or override if needed.
        
        if self.start_date and self.end_date:
            # If specific dates are needed, we might bypass get_historical_data or modify it.
            # Let's use yfinance directly for specific dates to be precise
            ticker = yf.Ticker(self.symbol)
            self.data = ticker.history(start=self.start_date, end=self.end_date, interval="1d")
        else:
            self.data = get_historical_data(self.symbol, period=self.period)
            
        if self.data.empty:
            raise ValueError("No data fetched")
            
        self.calculate_indicators()
        print(f"Data loaded: {len(self.data)} rows")

    def calculate_indicators(self):
        """Calculate RSI and Movement Score."""
        # RSI Calculation (14-day)
        delta = self.data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        
        rs = gain / loss
        self.data['rsi'] = 100 - (100 / (1 + rs))
        
        # Movement Score Calculation (Proxy)
        # Logic: Normalized position relative to 20-day SMA + Momentum
        # 0.0 = Strong Bearish, 1.0 = Strong Bullish
        sma_20 = self.data['Close'].rolling(window=20).mean()
        std_20 = self.data['Close'].rolling(window=20).std()
        
        # Z-score-like metric: (Price - SMA) / (2 * STD)
        # Clipped to -1 to 1, then scaled to 0 to 1
        z_score = (self.data['Close'] - sma_20) / (2 * std_20)
        self.data['movement_score'] = ((z_score.clip(-1, 1) + 1) / 2).fillna(0.5)
        
        # Fill NaN values for RSI
        self.data['rsi'] = self.data['rsi'].fillna(50)

    def run(self, mode: str = "rule"):
        """Run the backtest simulation."""
        print(f"Starting backtest simulation (Mode: {mode})...")
        
        for date, row in self.data.iterrows():
            # Prepare features for decision agent
            features = {
                "price": row['Close'],
                "movement_score": row['movement_score'],
                "rsi": row['rsi'],
                "volume": row['Volume'],
                # Mock sentiment as unavailable/neutral
                "sentiment_score": 0.0,
                "reason": "Backtest simulation"
            }
            
            # Get Decision
            # Since backtester is synchronous loop, we need to handle the async decision function
            # For "rule" based, we can call the rule function directly to avoid async overhead if we want,
            # but to test the actual agent flow, we should call make_decision.
            # We'll use asyncio.run for the single call or just call the rule logic directly if mode is 'rule'
            
            if mode == "rule":
                # Direct call to rule logic to avoid async complexity in simple loop
                decision = decision_agent.rule_based_decision(features)
            else:
                # For LLM or other async modes, we'd need to run the async function
                # This is a bit heavy for a loop, but necessary for full simulation
                decision = asyncio.run(decision_agent.make_decision(
                    self.symbol, self.portfolio, self.investment_balance, self.fee, mode=mode
                ))
            
            # Execute Decision
            action = decision.get("action", "HOLD")
            price = row['Close']
            
            execution_result = None
            if action == "BUY":
                execution_result = execution_agent.execute_buy(
                    self.symbol, price, self.investment_balance, self.fee, 
                    self.portfolio, self.investment_balance
                )
                if execution_result["status"] == "ok":
                    self.investment_balance = execution_result["investment_balance_remaining"]
                    self.trades.append({
                        "date": date,
                        "type": "BUY",
                        "price": price,
                        "shares": execution_result["shares"],
                        "cost": execution_result["total_cost"],
                        "balance": self.investment_balance
                    })
                    
            elif action == "SELL":
                execution_result = execution_agent.execute_sell(
                    self.symbol, price, self.fee, 
                    self.portfolio, self.investment_balance
                )
                if execution_result["status"] == "ok":
                    self.investment_balance = execution_result["investment_balance_after"]
                    self.trades.append({
                        "date": date,
                        "type": "SELL",
                        "price": price,
                        "shares": execution_result["shares"],
                        "revenue": execution_result["revenue"],
                        "balance": self.investment_balance
                    })
            
            # Track Portfolio Value
            portfolio_value = self.investment_balance
            if self.symbol in self.portfolio:
                portfolio_value += self.portfolio[self.symbol]["shares"] * price
            
            self.history.append({
                "date": date,
                "portfolio_value": portfolio_value,
                "price": price,
                "cash": self.investment_balance,
                "shares": self.portfolio.get(self.symbol, {}).get("shares", 0)
            })

    def calculate_metrics(self):
        """Calculate performance metrics."""
        df_hist = pd.DataFrame(self.history).set_index("date")
        
        if df_hist.empty:
            return {"error": "No history generated"}
            
        initial_value = self.initial_capital
        final_value = df_hist["portfolio_value"].iloc[-1]
        
        # Returns
        total_return = (final_value - initial_value) / initial_value
        total_return_pct = total_return * 100
        
        # Buy and Hold Comparison
        initial_price = df_hist["price"].iloc[0]
        final_price = df_hist["price"].iloc[-1]
        bnh_return = (final_price - initial_price) / initial_price
        bnh_return_pct = bnh_return * 100
        
        # Daily Returns for Sharpe
        df_hist["daily_return"] = df_hist["portfolio_value"].pct_change()
        mean_daily_return = df_hist["daily_return"].mean()
        std_daily_return = df_hist["daily_return"].std()
        
        # Annualized Sharpe (assuming 252 trading days)
        sharpe_ratio = 0.0
        if std_daily_return > 0:
            sharpe_ratio = (mean_daily_return / std_daily_return) * (252 ** 0.5)
            
        # Max Drawdown
        df_hist["cum_max"] = df_hist["portfolio_value"].cummax()
        df_hist["drawdown"] = (df_hist["portfolio_value"] - df_hist["cum_max"]) / df_hist["cum_max"]
        max_drawdown = df_hist["drawdown"].min()
        max_drawdown_pct = max_drawdown * 100
        
        # Win/Loss Stats
        wins = 0
        losses = 0
        total_profit = 0
        total_loss = 0
        
        # We need to pair buys and sells to calculate trade-level PnL properly
        # For simplicity, let's look at the trades list. 
        # This is a simplified PnL per trade cycle (Buy -> Sell)
        # A more robust way is to track closed trades.
        # Let's iterate trades and match sells to weighted avg cost.
        
        trade_pnl = []
        # Re-construct trade PnL from executed trades
        # This is tricky with partial sells, but let's assume FIFO or Avg Cost
        # The execution agent uses Avg Cost.
        
        # We can just look at the 'revenue' from SELLs minus the cost basis of those shares
        # But we don't have the cost basis stored in the trade log easily without re-calculating.
        # Let's use a simpler metric: Profit Factor = Gross Profit / Gross Loss
        # We can estimate this from daily value changes? No, that includes unrealized.
        
        # Let's try to calculate realized PnL from the trades list
        # We need to track cost basis history or just trust the portfolio state?
        # The execution agent updates avg_cost.
        # Let's just count profitable SELL trades relative to the avg_cost AT THAT TIME.
        # Wait, the trade log doesn't have the avg_cost at the time of sell.
        # We can infer it or just skip detailed trade PnL for now and focus on Portfolio metrics.
        
        return {
            "Total Return (%)": float(round(total_return_pct, 2)),
            "Buy & Hold Return (%)": float(round(bnh_return_pct, 2)),
            "Sharpe Ratio": float(round(sharpe_ratio, 2)),
            "Max Drawdown (%)": float(round(max_drawdown_pct, 2)),
            "Final Value": float(round(final_value, 2)),
            "Total Trades": len(self.trades)
        }

    def plot_results(self, filename: str = "backtest_results.png"):
        """Plot portfolio performance vs buy-and-hold."""
        if not self.history:
            print("No history to plot")
            return

        df_hist = pd.DataFrame(self.history).set_index("date")
        
        # Normalize to start at 100 for comparison
        initial_value = df_hist["portfolio_value"].iloc[0]
        initial_price = df_hist["price"].iloc[0]
        
        df_hist["Portfolio"] = (df_hist["portfolio_value"] / initial_value) * 100
        df_hist["Buy & Hold"] = (df_hist["price"] / initial_price) * 100
        
        plt.figure(figsize=(12, 6))
        plt.plot(df_hist.index, df_hist["Portfolio"], label="Portfolio", linewidth=2)
        plt.plot(df_hist.index, df_hist["Buy & Hold"], label="Buy & Hold (Asset Price)", alpha=0.6, linestyle="--")
        
        # Plot Buy/Sell Markers
        # We need to match trades to dates in the plot
        for trade in self.trades:
            date = trade["date"]
            if trade["type"] == "BUY":
                # Find the portfolio value at this date to place the marker
                if date in df_hist.index:
                    val = df_hist.loc[date, "Portfolio"]
                    plt.scatter(date, val, marker="^", color="green", s=100, label="Buy" if "Buy" not in plt.gca().get_legend_handles_labels()[1] else "")
            elif trade["type"] == "SELL":
                if date in df_hist.index:
                    val = df_hist.loc[date, "Portfolio"]
                    plt.scatter(date, val, marker="v", color="red", s=100, label="Sell" if "Sell" not in plt.gca().get_legend_handles_labels()[1] else "")

        plt.title(f"Backtest Results: {self.symbol} ({self.period})")
        plt.xlabel("Date")
        plt.ylabel("Normalized Value (Start=100)")
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.savefig(filename)
        print(f"Plot saved to {filename}")
        plt.close()

if __name__ == "__main__":
    # Example Usage
    backtester = Backtester("AAPL", period="1y")
    try:
        backtester.load_data()
        backtester.run(mode="rule")
        metrics = backtester.calculate_metrics()
        print("\n--- Backtest Results ---")
        print(json.dumps(metrics, indent=2))
    except Exception as e:
        print(f"Backtest failed: {e}")
