#!/usr/bin/env python3
"""
Market Analysis Agent Integration Example

This script demonstrates how to integrate with the Market Data Agent Apify Actor
and build decision-making logic based on its structured output.

Usage:
    python integration_example.py
"""

import requests
import json
import time
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

class TradingSignal(Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"
    STRONG_BUY = "STRONG_BUY"
    STRONG_SELL = "STRONG_SELL"

@dataclass
class MarketDecision:
    symbol: str
    signal: TradingSignal
    confidence: float
    reasoning: str
    risk_level: str
    suggested_action: str

class MarketAnalysisConsumer:
    """Example agent that consumes market analysis from the Apify Actor"""

    def __init__(self, apify_actor_id: str, apify_token: str):
        self.apify_actor_id = apify_actor_id
        self.apify_token = apify_token
        self.base_url = "https://api.apify.com/v2"

    def analyze_market(self, symbol: str, data_type: str = "historical",
                      interval: str = "1d", range_period: str = "1mo") -> Dict[str, Any]:
        """
        Call the Market Analysis Apify Actor

        Args:
            symbol: Stock symbol (e.g., 'NVDA', 'AAPL')
            data_type: 'historical' or 'quote'
            interval: Time interval ('1d', '1h', '5m')
            range_period: Time range ('1mo', '3mo', '6mo', '1y')

        Returns:
            Complete analysis results from the actor
        """
        input_data = {
            "symbol": symbol,
            "data_type": data_type,
            "interval": interval,
            "range": range_period
        }

        print(f"📊 Requesting market analysis for {symbol}...")

        # Start the actor run
        run_url = f"{self.base_url}/acts/{self.apify_actor_id}/runs"
        headers = {
            "Authorization": f"Bearer {self.apify_token}",
            "Content-Type": "application/json"
        }

        response = requests.post(run_url, headers=headers, json=input_data)
        response.raise_for_status()

        run_id = response.json()["data"]["id"]
        print(f"🔄 Actor run started: {run_id}")

        # Wait for completion and get results
        return self._wait_for_results(run_id)

    def _wait_for_results(self, run_id: str, max_wait: int = 120) -> Dict[str, Any]:
        """Wait for actor run to complete and return results"""
        dataset_url = f"{self.base_url}/acts/{self.apify_actor_id}/runs/{run_id}/dataset/items"

        for i in range(max_wait):
            response = requests.get(dataset_url, headers={
                "Authorization": f"Bearer {self.apify_token}"
            })

            if response.status_code == 200:
                data = response.json()
                if data:  # Results are available
                    print("✅ Analysis complete!")
                    return data[0]  # Return first (and only) result

            time.sleep(2)  # Wait 2 seconds before checking again

        raise TimeoutError(f"Actor run {run_id} did not complete within {max_wait} seconds")

class TradingDecisionAgent:
    """Example decision-making agent that uses market analysis output"""

    def __init__(self, market_analyzer: MarketAnalysisConsumer):
        self.market_analyzer = market_analyzer

    def make_trading_decision(self, symbol: str) -> MarketDecision:
        """
        Analyze market data and make a trading decision

        Decision Logic:
        - Trend confidence > 0.8: Follow trend direction
        - RSI confidence > 0.8: Consider overbought/oversold signals
        - Overall confidence > 0.8: Strong signal
        - Multiple conflicting signals: Hold position
        """

        # Get market analysis
        analysis = self.market_analyzer.analyze_market(symbol)

        if not analysis.get("success"):
            return MarketDecision(
                symbol=symbol,
                signal=TradingSignal.HOLD,
                confidence=0.0,
                reasoning="Analysis failed",
                risk_level="UNKNOWN",
                suggested_action="Do not trade"
            )

        # Extract key insights
        llm_analysis = analysis["llm_analysis"]
        indicators = analysis["indicators"]
        current_price = analysis["price"]

        # Decision factors
        trend_confidence = llm_analysis["trend_analysis"]["confidence"]
        trend_insight = llm_analysis["trend_analysis"]["insight"].lower()

        rsi_confidence = llm_analysis["rsi_insights"]["confidence"]
        rsi_insight = llm_analysis["rsi_insights"]["insight"].lower()

        momentum_confidence = llm_analysis["momentum_interpretation"]["confidence"]
        momentum_insight = llm_analysis["momentum_interpretation"]["insight"].lower()

        overall_confidence = llm_analysis["overall_confidence"]
        actionable_guidance = llm_analysis["actionable_guidance"].lower()

        # Decision logic
        decision_signal = TradingSignal.HOLD
        decision_confidence = 0.5
        reasoning_parts = []
        risk_level = "MEDIUM"

        # Trend-based decisions
        if trend_confidence > 0.8:
            if "bullish" in trend_insight or "upward" in trend_insight:
                if overall_confidence > 0.8:
                    decision_signal = TradingSignal.STRONG_BUY
                    decision_confidence = min(trend_confidence, overall_confidence)
                    reasoning_parts.append(f"Strong bullish trend (confidence: {trend_confidence:.1f})")
                else:
                    decision_signal = TradingSignal.BUY
                    decision_confidence = trend_confidence
                    reasoning_parts.append(f"Bullish trend detected (confidence: {trend_confidence:.1f})")
            elif "bearish" in trend_insight or "downward" in trend_insight:
                if overall_confidence > 0.8:
                    decision_signal = TradingSignal.STRONG_SELL
                    decision_confidence = min(trend_confidence, overall_confidence)
                    reasoning_parts.append(f"Strong bearish trend (confidence: {trend_confidence:.1f})")
                else:
                    decision_signal = TradingSignal.SELL
                    decision_confidence = trend_confidence
                    reasoning_parts.append(f"Bearish trend detected (confidence: {trend_confidence:.1f})")

        # RSI-based adjustments
        if rsi_confidence > 0.8:
            if "overbought" in rsi_insight:
                if decision_signal == TradingSignal.BUY:
                    decision_signal = TradingSignal.HOLD
                    reasoning_parts.append(f"RSI overbought signal overrides buy (RSI confidence: {rsi_confidence:.1f})")
                    risk_level = "HIGH"
                elif decision_signal == TradingSignal.STRONG_BUY:
                    decision_signal = TradingSignal.BUY
                    reasoning_parts.append(f"RSI overbought reduces strong buy to buy")
            elif "oversold" in rsi_insight:
                if decision_signal == TradingSignal.SELL:
                    decision_signal = TradingSignal.HOLD
                    reasoning_parts.append(f"RSI oversold signal overrides sell (RSI confidence: {rsi_confidence:.1f})")
                    risk_level = "HIGH"
                elif decision_signal == TradingSignal.STRONG_SELL:
                    decision_signal = TradingSignal.SELL
                    reasoning_parts.append(f"RSI oversold reduces strong sell to sell")

        # Momentum confirmation
        if momentum_confidence > 0.8:
            if "strong" in momentum_insight and "positive" in momentum_insight:
                if decision_signal in [TradingSignal.BUY, TradingSignal.STRONG_BUY]:
                    reasoning_parts.append(f"Strong positive momentum confirms buy signal")
                elif decision_signal == TradingSignal.HOLD:
                    decision_signal = TradingSignal.BUY
                    decision_confidence = momentum_confidence
                    reasoning_parts.append(f"Strong positive momentum suggests buy despite neutral trend")

        # Risk assessment based on volatility
        if indicators.get("volatility", 0) > 10:
            risk_level = "HIGH"
            if decision_signal in [TradingSignal.BUY, TradingSignal.SELL]:
                decision_confidence *= 0.8  # Reduce confidence due to high volatility
                reasoning_parts.append("High volatility increases risk")

        # Final reasoning
        reasoning = "; ".join(reasoning_parts) if reasoning_parts else "No clear signals; maintaining hold position"

        # Suggested action
        if decision_signal == TradingSignal.STRONG_BUY:
            suggested_action = f"Strong buy signal - Consider allocating significant capital to {symbol} at ${current_price:.2f}"
        elif decision_signal == TradingSignal.BUY:
            suggested_action = f"Buy signal - Consider purchasing {symbol} at ${current_price:.2f}"
        elif decision_signal == TradingSignal.STRONG_SELL:
            suggested_action = f"Strong sell signal - Consider selling {symbol} position at ${current_price:.2f}"
        elif decision_signal == TradingSignal.SELL:
            suggested_action = f"Sell signal - Consider exiting {symbol} position at ${current_price:.2f}"
        else:
            suggested_action = f"Hold position - Monitor {symbol} for clearer signals"

        return MarketDecision(
            symbol=symbol,
            signal=decision_signal,
            confidence=round(decision_confidence, 2),
            reasoning=reasoning,
            risk_level=risk_level,
            suggested_action=suggested_action
        )

def main():
    """Example usage of the integrated system"""

    # Configuration - Replace with your actual values
    APIFY_ACTOR_ID = "your-actor-id-here"  # From Apify Console
    APIFY_TOKEN = "your-api-token-here"    # From Apify Console

    # Initialize agents
    market_analyzer = MarketAnalysisConsumer(APIFY_ACTOR_ID, APIFY_TOKEN)
    decision_agent = TradingDecisionAgent(market_analyzer)

    # Test with multiple stocks
    symbols_to_analyze = ["NVDA", "AAPL", "TSLA"]

    print("🚀 Market Analysis & Decision Making Demo\n")

    for symbol in symbols_to_analyze:
        print(f"{'='*60}")
        print(f"📈 Analyzing {symbol}")
        print(f"{'='*60}")

        try:
            # Get trading decision
            decision = decision_agent.make_trading_decision(symbol)

            # Display results
            print(f"🎯 Signal: {decision.signal.value}")
            print(f"📊 Confidence: {decision.confidence:.1%}")
            print(f"⚠️  Risk Level: {decision.risk_level}")
            print(f"💡 Reasoning: {decision.reasoning}")
            print(f"🎪 Suggested Action: {decision.suggested_action}")

        except Exception as e:
            print(f"❌ Error analyzing {symbol}: {str(e)}")

        print()  # Blank line between stocks

if __name__ == "__main__":
    main()
