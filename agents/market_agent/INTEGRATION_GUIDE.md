# Market Analysis Agent Integration Guide

## Overview

The Market Analysis Agent is a production-ready Apify Actor that fetches market data from Yahoo Finance, computes technical indicators, and generates AI-powered insights using Anthropic Claude. This guide explains how to integrate it with other agents and decision-making systems.

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Decision      │    │  Market Analysis  │    │   Yahoo Finance  │
│   Agent         │◄───┤    Apify Actor    │◄───┤     API         │
│                 │    │                   │    │                 │
└─────────────────┘    └───────────────────┘    └─────────────────┘
         ▲                        ▲
         └────────────────────────┘
              JSON API Response
```

## Complete Flow

### 1. Input Request
```json
{
  "symbol": "NVDA",
  "data_type": "historical",
  "interval": "1d",
  "range": "1mo"
}
```

### 2. Data Processing Pipeline
1. **Fetch Data**: Yahoo Finance API call
2. **Technical Analysis**: Compute 10+ indicators
3. **AI Analysis**: Claude LLM generates insights
4. **Structured Output**: JSON response with confidence scores

### 3. Output Response
```json
{
  "symbol": "NVDA",
  "price": 182.41,
  "indicators": {
    "sma20": 184.47,
    "rsi": 47.55,
    "bollinger": {"upper": 196.06, "middle": 184.47, "lower": 172.88},
    "volatility": 5.94
  },
  "llm_analysis": {
    "trend_analysis": {"insight": "...", "confidence": 0.7},
    "rsi_insights": {"insight": "...", "confidence": 0.8},
    "actionable_guidance": "Based on analysis...",
    "overall_confidence": 0.7
  },
  "success": true
}
```

## Integration Patterns

### Pattern 1: Direct API Call

```python
import requests

def get_market_analysis(symbol, apify_token, actor_id):
    response = requests.post(
        f"https://api.apify.com/v2/acts/{actor_id}/runs",
        headers={
            "Authorization": f"Bearer {apify_token}",
            "Content-Type": "application/json"
        },
        json={
            "symbol": symbol,
            "data_type": "historical",
            "interval": "1d",
            "range": "1mo"
        }
    )

    run_id = response.json()["data"]["id"]

    # Wait for completion and get results
    results = requests.get(
        f"https://api.apify.com/v2/acts/{actor_id}/runs/{run_id}/dataset/items",
        headers={"Authorization": f"Bearer {apify_token}"}
    )

    return results.json()[0]
```

### Pattern 2: Webhook Integration

```python
# Set up webhook in Apify Console
WEBHOOK_URL = "https://your-agent.com/webhook/market-analysis"

# Apify will POST results to your endpoint
@app.route('/webhook/market-analysis', methods=['POST'])
def handle_market_analysis():
    analysis_data = request.json

    # Process analysis and make decisions
    symbol = analysis_data["symbol"]
    confidence = analysis_data["llm_analysis"]["overall_confidence"]

    if confidence > 0.8:
        # High confidence signal - take action
        execute_trade(symbol, analysis_data)
    else:
        # Low confidence - monitor only
        log_for_monitoring(symbol, analysis_data)

    return {"status": "processed"}
```

### Pattern 3: Scheduled Analysis

```python
import schedule
import time

def daily_market_scan():
    symbols = ["NVDA", "AAPL", "MSFT", "GOOGL", "AMZN"]

    for symbol in symbols:
        analysis = get_market_analysis(symbol, APIFY_TOKEN, ACTOR_ID)

        # Apply your trading strategy
        decision = make_trading_decision(analysis)

        if decision["action"] != "HOLD":
            execute_trade(decision)

# Schedule daily analysis at market open
schedule.every().day.at("09:30").do(daily_market_scan)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### Pattern 4: Real-time Decision Agent

```python
class RealTimeTradingAgent:
    def __init__(self, market_analyzer):
        self.market_analyzer = market_analyzer
        self.positions = {}  # Track current positions

    def process_market_signal(self, symbol):
        # Get fresh analysis
        analysis = self.market_analyzer.analyze_market(symbol)

        # Extract key metrics
        trend_conf = analysis["llm_analysis"]["trend_analysis"]["confidence"]
        rsi_conf = analysis["llm_analysis"]["rsi_insights"]["confidence"]
        guidance = analysis["llm_analysis"]["actionable_guidance"]

        # Decision logic
        if trend_conf > 0.8 and "bullish" in guidance:
            if symbol not in self.positions:
                self.enter_position(symbol, analysis["price"])
        elif rsi_conf > 0.8 and "overbought" in guidance:
            if symbol in self.positions:
                self.exit_position(symbol, analysis["price"])

    def run_real_time(self):
        symbols = ["NVDA", "AAPL", "TSLA"]
        while True:
            for symbol in symbols:
                self.process_market_signal(symbol)
            time.sleep(300)  # Check every 5 minutes
```

## Decision-Making Strategies

### Confidence-Based Trading

```python
def confidence_based_strategy(analysis):
    overall_conf = analysis["llm_analysis"]["overall_confidence"]

    if overall_conf >= 0.9:
        return "AGGRESSIVE_TRADE"  # Full position size
    elif overall_conf >= 0.7:
        return "NORMAL_TRADE"      # Half position size
    elif overall_conf >= 0.5:
        return "SMALL_TRADE"       # 25% position size
    else:
        return "NO_TRADE"          # Wait for better signals
```

### Multi-Factor Analysis

```python
def multi_factor_decision(analysis):
    factors = {
        "trend": analysis["llm_analysis"]["trend_analysis"]["confidence"],
        "momentum": analysis["llm_analysis"]["momentum_interpretation"]["confidence"],
        "rsi": analysis["llm_analysis"]["rsi_insights"]["confidence"],
        "volume": analysis["llm_analysis"]["volume_insights"]["confidence"]
    }

    # Weighted decision
    weights = {"trend": 0.4, "momentum": 0.3, "rsi": 0.2, "volume": 0.1}

    weighted_score = sum(factors[k] * weights[k] for k in factors)

    if weighted_score > 0.75:
        return "STRONG_BUY"
    elif weighted_score > 0.6:
        return "BUY"
    elif weighted_score < 0.4:
        return "SELL"
    else:
        return "HOLD"
```

### Risk Management Integration

```python
def risk_adjusted_decision(analysis, portfolio_risk):
    decision = basic_decision_logic(analysis)
    volatility = analysis["indicators"]["volatility"]
    position_size = analysis["price"] * 100  # Example position

    # Adjust for volatility
    if volatility > 15:  # High volatility
        position_size *= 0.5  # Reduce position size
    elif volatility > 10:
        position_size *= 0.75

    # Adjust for portfolio risk
    max_position = portfolio_risk["max_single_position"]
    if position_size > max_position:
        position_size = max_position

    return {
        "decision": decision,
        "position_size": position_size,
        "stop_loss": analysis["price"] * 0.95,  # 5% stop loss
        "take_profit": analysis["price"] * 1.1   # 10% take profit
    }
```

## Error Handling

### Network Issues
```python
def robust_market_analysis(symbol):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            return get_market_analysis(symbol)
        except requests.RequestException as e:
            if attempt == max_retries - 1:
                logger.error(f"Failed to analyze {symbol}: {e}")
                return None
            time.sleep(2 ** attempt)  # Exponential backoff
```

### Invalid Data Handling
```python
def validate_analysis_response(analysis):
    required_fields = ["symbol", "price", "indicators", "llm_analysis", "success"]

    if not all(field in analysis for field in required_fields):
        raise ValueError("Invalid analysis response structure")

    if not analysis["success"]:
        raise ValueError(f"Analysis failed: {analysis.get('error', 'Unknown error')}")

    # Validate confidence scores
    llm_analysis = analysis["llm_analysis"]
    for insight_type, insight_data in llm_analysis.items():
        if isinstance(insight_data, dict) and "confidence" in insight_data:
            conf = insight_data["confidence"]
            if not (0 <= conf <= 1):
                logger.warning(f"Invalid confidence score for {insight_type}: {conf}")

    return analysis
```

## Performance Considerations

### Caching Strategy
```python
from cachetools import TTLCache

class CachedMarketAnalyzer:
    def __init__(self, analyzer):
        self.analyzer = analyzer
        self.cache = TTLCache(maxsize=100, ttl=300)  # 5-minute cache

    def analyze_market(self, symbol):
        cache_key = f"{symbol}_1d_1mo"

        if cache_key in self.cache:
            return self.cache[cache_key]

        analysis = self.analyzer.analyze_market(symbol)
        self.cache[cache_key] = analysis
        return analysis
```

### Batch Processing
```python
def batch_market_analysis(symbols, max_concurrent=3):
    """Analyze multiple symbols concurrently"""
    import asyncio
    import aiohttp

    async def analyze_symbol(session, symbol):
        # Async version of market analysis call
        async with session.post(API_URL, json={"symbol": symbol}) as response:
            return await response.json()

    async def main():
        async with aiohttp.ClientSession() as session:
            tasks = [analyze_symbol(session, symbol) for symbol in symbols]
            return await asyncio.gather(*tasks)

    return asyncio.run(main())
```

## Monitoring and Logging

### Structured Logging
```python
import logging
import json

def log_trading_decision(symbol, analysis, decision):
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "symbol": symbol,
        "current_price": analysis["price"],
        "decision": decision["signal"],
        "confidence": decision["confidence"],
        "indicators": {
            "rsi": analysis["indicators"]["rsi"],
            "volatility": analysis["indicators"]["volatility"]
        },
        "llm_confidence": analysis["llm_analysis"]["overall_confidence"]
    }

    logger.info("Trading decision made", extra=log_data)
```

### Performance Metrics
```python
class PerformanceTracker:
    def __init__(self):
        self.metrics = {
            "total_analyses": 0,
            "successful_analyses": 0,
            "avg_response_time": 0,
            "error_rate": 0
        }

    def track_analysis(self, symbol, success, response_time):
        self.metrics["total_analyses"] += 1
        if success:
            self.metrics["successful_analyses"] += 1

        # Update moving average response time
        self.metrics["avg_response_time"] = (
            (self.metrics["avg_response_time"] * (self.metrics["total_analyses"] - 1)) +
            response_time
        ) / self.metrics["total_analyses"]

        self.metrics["error_rate"] = (
            (self.metrics["total_analyses"] - self.metrics["successful_analyses"]) /
            self.metrics["total_analyses"]
        )
```

## Example Implementation

See `integration_example.py` for a complete working example of a decision-making agent that integrates with the Market Analysis Actor.

## API Reference

### Input Parameters
- `symbol` (string): Stock/crypto symbol (e.g., "NVDA", "AAPL", "BTC-USD")
- `data_type` (string): "historical" or "quote"
- `interval` (string): "1d", "1h", "5m" (required for historical)
- `range` (string): "1mo", "3mo", "6mo", "1y" (required for historical)

### Output Structure
- `symbol` (string): Analyzed symbol
- `price` (float): Current/last price
- `indicators` (object): Technical indicators
- `llm_analysis` (object): AI-generated insights with confidence scores
- `success` (boolean): Operation success status

## Best Practices

1. **Rate Limiting**: Respect API limits (both Apify and Yahoo Finance)
2. **Error Handling**: Implement comprehensive error handling and retries
3. **Caching**: Cache results for frequently analyzed symbols
4. **Validation**: Always validate response structure
5. **Monitoring**: Log performance metrics and trading decisions
6. **Risk Management**: Implement position sizing and stop-loss logic
7. **Backtesting**: Test strategies with historical data before live trading

## Security Considerations

1. **API Keys**: Store Apify tokens securely (environment variables, secret managers)
2. **Input Validation**: Validate all inputs to prevent injection attacks
3. **Rate Limiting**: Implement client-side rate limiting
4. **Logging**: Avoid logging sensitive financial data
5. **Encryption**: Use HTTPS for all API communications

This integration guide provides everything needed to build sophisticated trading systems using the Market Analysis Agent as a foundation component.
