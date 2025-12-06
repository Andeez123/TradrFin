# decision_agent.py
import json
import asyncio
import httpx
import os
import pandas as pd
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

SENTIMENT_AGENT_URL = os.getenv("SENTIMENT_AGENT_URL", "http://localhost:8001/sentiment")
MARKET_AGENT_URL = os.getenv("MARKET_AGENT_URL", "http://localhost:8002/data")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5")

# Cache for precomputed data
_precomputed_cache = {}

async def fetch_sentiment(symbol: str) -> Dict[str, Any]:
    # async with httpx.AsyncClient(timeout=10) as client:
    #     try:
    #         r = await client.get(f"{SENTIMENT_AGENT_URL}?symbol={symbol}")
    #         r.raise_for_status()
    #         return r.json()
    #     except Exception as e:
    #         return {"error": f"sentiment fetch failed: {str(e)}"}
    return {"sentiment_score": 0.7, "reason": "mock sentiment score"}

def load_precomputed_data(symbol: str) -> pd.DataFrame:
    """Load precomputed indicator data for a symbol."""
    global _precomputed_cache
    
    # Check cache first
    if symbol in _precomputed_cache:
        return _precomputed_cache[symbol]
    
    # Find the most recent CSV file for this symbol
    files = [f for f in os.listdir(".") if f.startswith(f"{symbol}_indicators_") and f.endswith(".csv")]
    if not files:
        return None
    
    # Use the most recent file
    latest_file = sorted(files)[-1]
    df = pd.read_csv(latest_file, index_col=0, parse_dates=True)
    
    # Cache it
    _precomputed_cache[symbol] = df
    return df

async def fetch_market_data(symbol: str, day_index: int = None) -> Dict[str, Any]:
    """
    Fetch market data for a symbol.
    If day_index is provided, uses precomputed data for that day.
    Otherwise, returns mock data.
    """
    # If day_index is provided, try to use precomputed data
    if day_index is not None:
        df = load_precomputed_data(symbol)
        if df is not None and day_index < len(df):
            row = df.iloc[day_index]
            # Format date to remove time component
            date_obj = df.index[day_index]
            date_str = date_obj.strftime("%Y-%m-%d") if hasattr(date_obj, 'strftime') else str(date_obj).split()[0]
            
            return {
                "price": float(row['Price']),
                "movement_score": float(row['Movement_Score']),
                "rsi": float(row['RSI']),
                "reason": f"Precomputed data for {symbol} day {day_index}",
                "date": date_str
            }
    
    # Fallback to mock data
    # async with httpx.AsyncClient(timeout=10) as client:
    #     try:
    #         r = await client.get(f"{MARKET_AGENT_URL}?symbol={symbol}")
    #         r.raise_for_status()
    #         return r.json()
    #     except Exception as e:
    #         return {"error": f"market fetch failed: {str(e)}"}
    return {
        "price": 100.0,
        "movement_score": 0.7,
        "rsi": 50,
        "reason": "mock market data"
    }

def rule_based_decision(features: Dict[str, Any]) -> Dict[str, Any]:
    """
    Rule-based decision making that works with or without sentiment scores.
    Uses market data (movement, RSI) as primary indicators.
    """
    s = features.get("sentiment_score", 0.0)
    rsi = features.get("rsi", 50)
    movement = features.get("movement_score", 0.5)
    has_sentiment = "sentiment_score" in features and features.get("sentiment_score") != 0.0

    # BUY conditions - can work with or without sentiment
    if has_sentiment:
        # With sentiment: require both positive sentiment and bullish movement
        if s > 0.6 and movement > 0.6 and rsi < 70:
            return {"action":"BUY", "confidence":0.8, "reason":"Positive sentiment + bullish movement"}
    else:
        # Without sentiment: use only market indicators
        if movement > 0.6 and rsi < 70:
            return {"action":"BUY", "confidence":0.7, "reason":"Bullish movement + RSI indicates buying opportunity"}
        elif movement > 0.7 and rsi < 60:
            return {"action":"BUY", "confidence":0.75, "reason":"Strong bullish movement with favorable RSI"}

    # SELL conditions
    if has_sentiment:
        # With sentiment: negative sentiment or weak movement
        if s < -0.5 and movement < 0.4:
            return {"action":"SELL", "confidence":0.75, "reason":"Negative sentiment + weak movement"}
    else:
        # Without sentiment: use only market indicators
        if movement < 0.3 and rsi > 70:
            return {"action":"SELL", "confidence":0.7, "reason":"Weak movement + overbought RSI"}
        elif movement < 0.2:
            return {"action":"SELL", "confidence":0.65, "reason":"Very weak market movement"}
    
    return {"action":"HOLD", "confidence":0.5, "reason":"No clear signal"}

def build_llm_prompt(features: Dict[str, Any], portfolio: Dict[str, Any], budget: float, fee: float) -> str:
    has_sentiment = "sentiment_score" in features and features.get("sentiment_score", 0.0) != 0.0
    
    sentiment_note = ""
    if not has_sentiment:
        sentiment_note = "\nNOTE: Sentiment data is not available. Base your decision primarily on market data (price movement, RSI, volume, etc.)."
    
    prompt = f"""You are an expert financial trading assistant. Analyze the provided data and make a trading decision.

MARKET DATA:
{json.dumps(features, indent=2)}
{sentiment_note}

CURRENT PORTFOLIO:
{json.dumps(portfolio, indent=2)}

AVAILABLE BUDGET: ${budget:.2f}
TRADING FEE PER TRANSACTION: ${fee:.2f}

INSTRUCTIONS:
1. Analyze the available market data to assess the stock's potential
   {"- If sentiment data is available, consider it along with market indicators" if has_sentiment else "- Focus on market indicators: price movement, RSI, volume, trends"}
2. Consider the current portfolio composition and diversification
3. Make a decision: BUY (if bullish), SELL (if bearish or profit-taking), or HOLD (if uncertain)
4. Provide a confidence score (0.0 to 1.0) indicating how certain you are
5. Explain your reasoning

IMPORTANT:
- DO NOT calculate exact costs, shares, or fees - just provide your recommendation
- Consider risk management and portfolio diversification
- Be conservative with confidence scores
- For BUY: Consider if the stock fits the portfolio strategy
- For SELL: Consider if it's time to take profits or cut losses
- {"You can make decisions based on market data alone if sentiment is unavailable" if not has_sentiment else ""}

Respond with ONLY valid JSON in this exact format:
{{
  "action": "BUY|SELL|HOLD",
  "confidence": 0.0-1.0,
  "reason": "Your explanation here"
}}"""
    return prompt

async def llm_decision(features: Dict[str, Any], portfolio: Dict[str, Any], budget: float, fee: float) -> Dict[str, Any]:
    """Use Claude API for LLM-based trading decisions."""
    if not ANTHROPIC_API_KEY:
        return {"action":"HOLD","confidence":0.0,"reason":"ANTHROPIC_API_KEY not set"}
    
    try:
        from anthropic import Anthropic
        
        client = Anthropic(api_key=ANTHROPIC_API_KEY)
        prompt = build_llm_prompt(features, portfolio, budget, fee)
        
        message = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=500,
            temperature=0.3,
            system="You are a financial trading expert. Always respond with valid JSON only. Do not include any text outside the JSON object.",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        # Extract JSON from response
        content = message.content[0].text
        # Try to extract JSON if wrapped in markdown code blocks
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        decision = json.loads(content)
        
        # Validate response structure
        if "action" not in decision:
            decision["action"] = "HOLD"
        if "confidence" not in decision:
            decision["confidence"] = 0.5
        if "reason" not in decision:
            decision["reason"] = "No reasoning provided"
        
        return decision
        
    except ImportError:
        return {"action":"HOLD","confidence":0.0,"reason":"Anthropic SDK not installed. Install with: pip install anthropic"}
    except json.JSONDecodeError as e:
        return {"action":"HOLD","confidence":0.0,"reason":f"Failed to parse Claude response as JSON: {str(e)}"}
    except Exception as e:
        return {"action":"HOLD","confidence":0.5,"reason":f"Claude API error: {str(e)}"}

async def make_decision(symbol: str, portfolio: Dict[str, Any], budget: float, fee: float, mode: str="rule") -> Dict[str, Any]:
    """
    Make a trading decision. Works with or without sentiment data.
    Market data is required, sentiment is optional.
    """
    sentiment, market = await asyncio.gather(fetch_sentiment(symbol), fetch_market_data(symbol))
    
    # Market data is required - if it has an error, return HOLD
    if "error" in market:
        return {"action":"HOLD","confidence":0.5,"reason":"Market data fetch error"}
    
    # Sentiment is optional - merge what we have
    features = {**market}
    if "error" not in sentiment:
        features.update(sentiment)
    # If sentiment has error but we have market data, continue without sentiment

    if mode == "rule":
        return rule_based_decision(features)
    elif mode == "llm":
        return await llm_decision(features, portfolio, budget, fee)
    elif mode == "mock":
        return rule_based_decision(features)
    else:
        return {"action":"HOLD","confidence":0.5,"reason":"Unknown mode"}
