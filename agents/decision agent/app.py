# app.py
from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
from contextlib import asynccontextmanager
from decision_agent import make_decision, fetch_sentiment, fetch_market_data
from execution_agent import execute_buy, execute_sell
from datetime import datetime
import pandas as pd
import os
import csv

# User state (demo)
user_state = {
    "portfolio": {},
    "investment_balance": 5000.0,  # Amount user is willing to spend on trading
    "day_index": 0  # Current day index for simulation
}

# CSV log for simple transaction tracking
csv_log_filename = f"trading_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
csv_log_file = None
csv_writer = None

# Candidate assets universe
candidate_symbols = ["AAPL", "TSLA", "GOOG", "AMZN", "MSFT"]

# Config
TRADE_BUDGET = 1000.0
TRADE_FEE = 5.0
TOP_N = 2  # top assets to trade per cycle
DAILY_INTERVAL_HOURS = 24
DECISION_MODE = "rule"  # "rule" | "llm" | "mock"

class TradeRequest(BaseModel):
    budget: float = TRADE_BUDGET
    fee: float = TRADE_FEE
    mode: str = DECISION_MODE

# Scoring function to select top assets
def score_assets(candidates: list, sentiment_data: dict, market_data: dict) -> list:
    """
    Score assets based on market data and optional sentiment data.
    If sentiment is unavailable, uses only market movement score.
    """
    scores = {}
    for symbol in candidates:
        # Get sentiment score if available, otherwise use 0 (neutral)
        s = sentiment_data.get(symbol, {}).get("sentiment_score", 0.0)
        # Get movement score from market data
        m = market_data.get(symbol, {}).get("movement_score", 0.5)
        
        # If sentiment is available, use weighted combination
        # Otherwise, use only movement score
        if s != 0.0 or "sentiment_score" in sentiment_data.get(symbol, {}):
            score = 0.6 * s + 0.4 * m
        else:
            # No sentiment available, use only market movement
            score = m
        
        scores[symbol] = score
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [sym for sym, _ in ranked]

# Autonomous daily trading loop
async def autonomous_test_loop(interval_seconds: int = 2):
    global csv_log_file, csv_writer
    
    # Initialize CSV log
    csv_log_file = open(csv_log_filename, 'w', newline='')
    csv_writer = csv.DictWriter(csv_log_file, fieldnames=[
        'ticker', 'movement_score', 'action', 'quantity', 'price', 'executed_at', 'status', 'summary'
    ])
    csv_writer.writeheader()
    
    print("=" * 60)
    print("AUTONOMOUS TRADING AGENT STARTED")
    print(f"Mode: {DECISION_MODE}")
    print(f"Interval: {interval_seconds} seconds")
    print(f"Initial Balance: ${user_state['investment_balance']:.2f}")
    print(f"CSV Log: {csv_log_filename}")
    print("=" * 60)
    
    # Note: Precomputed data is loaded on-demand by decision_agent
    # We just need to know how many days are available
    # Check the first symbol to determine max_days
    from decision_agent import load_precomputed_data
    sample_df = load_precomputed_data(candidate_symbols[0])
    if sample_df is None:
        print("ERROR: No precomputed data available. Run precompute_indicators.py first.")
        return
    
    max_days = len(sample_df)
    print(f"Simulation will run for {max_days} days (1 day per {interval_seconds}s iteration)")
    print("=" * 60)
    
    iteration = 0
    while True:
        try:
            iteration += 1
            day_index = user_state["day_index"]
            
            # Stop if we've exhausted the precomputed data
            if day_index >= max_days:
                print(f"\n[{datetime.now()}] Reached end of precomputed data (Day {day_index}/{max_days}). Stopping simulation.")
                break
            
            # Stop if investment balance is exhausted
            if user_state["investment_balance"] <= 0:
                print(f"[{datetime.now()}] Investment balance depleted. Stopping autonomous trading.")
                break

            print(f"\n[{datetime.now()}] Iteration #{iteration} - Day {day_index + 1}/{max_days}")
            print(f"Portfolio: {len(user_state['portfolio'])} positions, Investment Balance: ${user_state['investment_balance']:.2f}")

            # Use precomputed data for this day
            print(f"Using precomputed data for day index {day_index}...")
            sentiment_data = {}
            market_data = {}
            trading_date = None  # Will store the actual date from CSV
            
            for symbol in candidate_symbols:
                # Get sentiment (still mock/unavailable)
                sentiment_data[symbol] = await fetch_sentiment(symbol)
                
                # Get market data (with day_index for precomputed data)
                market_data[symbol] = await fetch_market_data(symbol, day_index=day_index)
                
                # Extract trading date from the first symbol's response
                if trading_date is None and "date" in market_data[symbol]:
                    trading_date = market_data[symbol]["date"]
            
            # Print the trading date
            if trading_date:
                print(f"Trading Date: {trading_date}")
            
            # Check if sentiment is available
            has_sentiment = any(
                "sentiment_score" in data and data.get("sentiment_score", 0.0) != 0.0 
                for data in sentiment_data.values()
            )
            
            if has_sentiment:
                # print(f"Sentiment data: {sentiment_data}")
                pass
            else:
                print("Note: Sentiment data not available - using market data only")
            # print(f"Market data: {market_data}")

            # Rank assets and pick top N
            ranked_symbols = score_assets(candidate_symbols, sentiment_data, market_data)
            top_symbols = ranked_symbols[:TOP_N]
            print(f"Top {TOP_N} assets selected: {top_symbols}")

            for symbol in top_symbols:
                # Stop early if balance runs out
                if user_state["investment_balance"] <= 0:
                    print(f"[{datetime.now()}] Investment balance depleted during trading. Stopping.")
                    break

                budget = min(TRADE_BUDGET, user_state["investment_balance"])
                print(f"\nAnalyzing {symbol} with budget ${budget:.2f}...")
                
                decision = await make_decision(symbol, user_state["portfolio"], budget, TRADE_FEE, mode=DECISION_MODE)
                action = decision.get("action", "HOLD")
                confidence = decision.get("confidence", 0.0)
                reason = decision.get("reason", "No reason provided")
                
                print(f"Decision for {symbol}: {action} (confidence: {confidence:.2%}) - {reason}")
                
                price = market_data[symbol].get("price")
                if price is None:
                    print(f"Warning: No price data for {symbol}, skipping...")
                    continue

                if action == "BUY":
                    print(f"Executing BUY for {symbol}...")
                    result = execute_buy(symbol, price, budget, TRADE_FEE,
                                         user_state["portfolio"], user_state["investment_balance"])
                    if result["status"] == "ok":
                        user_state["investment_balance"] = result["investment_balance_remaining"]
                        date_str = f" on {trading_date}" if trading_date else ""
                        print(f"[SUCCESS] BUY{date_str}: {result.get('shares', 0)} shares of {symbol} at ${price:.2f} (Cost: ${result.get('total_cost', 0):.2f}, Remaining Balance: ${user_state['investment_balance']:.2f})")
                        
                        # Log to CSV
                        csv_writer.writerow({
                            'ticker': symbol,
                            'movement_score': f"{market_data[symbol].get('movement_score', 0.0):.4f}",
                            'action': 'buy',
                            'quantity': f"{result.get('shares', 0):.4f}",
                            'price': f"{price:.4f}",
                            'executed_at': trading_date,
                            'status': 'executed',
                            'summary': reason
                        })
                        csv_log_file.flush()
                    else:
                        print(f"[FAILED] BUY: {result.get('reason', 'Unknown error')}")
                        
                        # Log failed transaction to CSV
                        csv_writer.writerow({
                            'ticker': symbol,
                            'movement_score': f"{market_data[symbol].get('movement_score', 0.0):.4f}",
                            'action': 'buy',
                            'quantity': '0.0000',
                            'price': f"{price:.4f}",
                            'executed_at': trading_date,
                            'status': 'failed',
                            'summary': result.get('reason', 'Unknown error')
                        })
                        csv_log_file.flush()
                elif action == "SELL":
                    print(f"Executing SELL for {symbol}...")
                    result = execute_sell(symbol, price, TRADE_FEE,
                                          user_state["portfolio"], user_state["investment_balance"])
                    if result["status"] == "ok":
                        user_state["investment_balance"] = result["investment_balance_after"]
                        date_str = f" on {trading_date}" if trading_date else ""
                        print(f"[SUCCESS] SELL{date_str}: {result.get('shares', 0)} shares of {symbol} at ${price:.2f} (Revenue: ${result.get('revenue', 0):.2f}, New Balance: ${user_state['investment_balance']:.2f})")
                        
                        # Log to CSV
                        csv_writer.writerow({
                            'ticker': symbol,
                            'movement_score': f"{market_data[symbol].get('movement_score', 0.0):.4f}",
                            'action': 'sell',
                            'quantity': f"{result.get('shares', 0):.4f}",
                            'price': f"{price:.4f}",
                            'executed_at': trading_date,
                            'status': 'executed',
                            'summary': reason
                        })
                        csv_log_file.flush()
                    else:
                        print(f"[FAILED] SELL: {result.get('reason', 'Unknown error')}")
                        
                        # Log failed transaction to CSV
                        csv_writer.writerow({
                            'ticker': symbol,
                            'movement_score': f"{market_data[symbol].get('movement_score', 0.0):.4f}",
                            'action': 'sell',
                            'quantity': '0.0000',
                            'price': f"{price:.4f}",
                            'executed_at': trading_date,
                            'status': 'failed',
                            'summary': result.get('reason', 'Unknown error')
                        })
                        csv_log_file.flush()
                else:
                    print(f"HOLD decision for {symbol} - no action taken")
                    
                    # Log HOLD to CSV (as pending since no action taken)
                    csv_writer.writerow({
                        'ticker': symbol,
                        'movement_score': f"{market_data[symbol].get('movement_score', 0.0):.4f}",
                        'action': 'hold',
                        'quantity': '0.0000',
                        'price': f"{price:.4f}",
                        'executed_at': trading_date,
                        'status': 'pending',
                        'summary': reason
                    })
                    csv_log_file.flush()

            # Increment day index for next iteration
            user_state["day_index"] += 1
            
            print(f"\nWaiting {interval_seconds} seconds until next cycle...")
            await asyncio.sleep(interval_seconds)
            
        except Exception as e:
            print(f"ERROR in trading loop: {str(e)}")
            import traceback
            traceback.print_exc()
            await asyncio.sleep(10)  # Wait 10 seconds before retrying
    
    # Cleanup: Close CSV file
    if csv_log_file:
        csv_log_file.close()
        print(f"\nCSV log saved to {csv_log_filename}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting autonomous trading agent...")
    task = asyncio.create_task(autonomous_test_loop())
    yield
    # Shutdown
    print("Shutting down autonomous trading agent...")
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass

app = FastAPI(title="Autonomous Trading Agent", lifespan=lifespan)

@app.get("/portfolio")
def get_portfolio():
    return {
        "portfolio": user_state["portfolio"],
        "investment_balance": user_state["investment_balance"]
    }
