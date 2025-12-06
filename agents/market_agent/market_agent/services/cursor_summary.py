"""Summary service for generating human-readable market analysis summaries using Anthropic API."""

import logging
import os
from typing import Optional
import json
from anthropic import Anthropic
from ..types.market_types import MarketAnalysis, LLMAnalysis, LLMInsight

logger = logging.getLogger(__name__)


class SummaryServiceError(Exception):
    """Custom exception for summary service errors."""
    pass


class SummaryService:
    """Service for generating human-readable summaries using Anthropic API."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the summary service.

        Args:
            api_key: Anthropic API key. If None, will try to get from environment.
        """
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        self.client = None

        if self.api_key:
            try:
                self.client = Anthropic(api_key=self.api_key)
            except Exception as e:
                logger.warning(f"Failed to initialize Anthropic client: {str(e)}")
        else:
            logger.warning("No Anthropic API key provided. Using fallback template mode.")

    def generate_analysis(self, analysis: MarketAnalysis) -> tuple[str, LLMAnalysis]:
        """
        Generate comprehensive market analysis using Anthropic LLM.
        Returns both structured insights and human-readable summary.

        Args:
            analysis: MarketAnalysis object with technical indicators

        Returns:
            Tuple of (human_readable_summary, structured_llm_analysis)

        Raises:
            SummaryServiceError: If Anthropic API is not available or fails
        """
        if not self.client:
            raise SummaryServiceError("Anthropic API client not available. Please set ANTHROPIC_API_KEY environment variable.")

        try:
            # Generate structured analysis with human-readable summary in one call
            llm_analysis = self._generate_structured_insights(analysis)
            return llm_analysis.human_readable_summary, llm_analysis
        except Exception as e:
            logger.error(f"Anthropic API analysis failed: {str(e)}")
            raise SummaryServiceError(f"Failed to generate LLM analysis: {str(e)}")



    def _generate_structured_insights(self, analysis: MarketAnalysis) -> LLMAnalysis:
        """
        Generate structured insights using Anthropic Claude with temperature=0.

        Args:
            analysis: MarketAnalysis object

        Returns:
            LLMAnalysis with structured insights

        Raises:
            Exception: If API call fails
        """
        # Prepare the raw technical indicators for LLM analysis
        analysis_data = {
            'symbol': analysis.symbol,
            'price': analysis.price,
            'indicators': {
                'sma20': analysis.indicators.sma20,
                'sma50': analysis.indicators.sma50,
                'ema20': analysis.indicators.ema20,
                'ema50': analysis.indicators.ema50,
                'rsi': analysis.indicators.rsi,
                'macd': analysis.indicators.macd,
                'bollinger': analysis.indicators.bollinger,
                'volatility': analysis.indicators.volatility,
                'momentum': analysis.indicators.momentum,
                'volume_avg': analysis.indicators.volume_avg,
                'volume_spike_ratio': analysis.indicators.volume_spike_ratio
            }
        }

        prompt = f"""You are a professional financial analyst. Analyze the following technical indicators and market data for {analysis.symbol}. Provide ONLY a valid JSON response with structured insights, confidence metrics, and a concise human-readable summary.

Data: {json.dumps(analysis_data, indent=2, default=str)}

Return JSON in this exact format:
{{
  "trend_analysis": {{
    "insight": "string describing trend",
    "confidence": 0.0-1.0,
    "reasoning": "step-by-step reasoning"
  }},
  "momentum_interpretation": {{
    "insight": "string describing momentum",
    "confidence": 0.0-1.0,
    "reasoning": "step-by-step reasoning"
  }},
  "rsi_insights": {{
    "insight": "string describing RSI condition",
    "confidence": 0.0-1.0,
    "reasoning": "step-by-step reasoning"
  }},
  "bollinger_insights": {{
    "insight": "string describing Bollinger Bands",
    "confidence": 0.0-1.0,
    "reasoning": "step-by-step reasoning"
  }},
  "volume_insights": {{
    "insight": "string describing volume patterns",
    "confidence": 0.0-1.0,
    "reasoning": "step-by-step reasoning"
  }},
  "volatility_insights": {{
    "insight": "string describing volatility levels",
    "confidence": 0.0-1.0,
    "reasoning": "step-by-step reasoning"
  }},
  "actionable_guidance": "neutral, factual actionable guidance",
  "overall_confidence": 0.0-1.0,
  "human_readable_summary": "concise 2-3 sentence summary covering key signals and actionable insights"
}}

Guidelines:
- Use ONLY the provided data - do not hallucinate or speculate
- Confidence scores based on indicator strength and data quality
- Stepwise reasoning: analyze data → interpret indicators → draw conclusions
- Actionable guidance should be neutral and factual
- Human-readable summary should be 2-3 sentences, professional, and informative
- Return ONLY valid JSON, no additional text"""

        try:
            response = self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=2000,
                temperature=0.0,  # Deterministic output
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Parse the JSON response
            result_text = response.content[0].text.strip()

            # Clean up any potential markdown formatting
            if result_text.startswith('```json'):
                result_text = result_text[7:]
            if result_text.endswith('```'):
                result_text = result_text[:-3]
            result_text = result_text.strip()

            # Parse JSON
            structured_data = json.loads(result_text)

            # Convert to LLMAnalysis object
            return LLMAnalysis(
                trend_analysis=LLMInsight(**structured_data['trend_analysis']),
                momentum_interpretation=LLMInsight(**structured_data['momentum_interpretation']),
                rsi_insights=LLMInsight(**structured_data['rsi_insights']),
                bollinger_insights=LLMInsight(**structured_data['bollinger_insights']),
                volume_insights=LLMInsight(**structured_data['volume_insights']),
                volatility_insights=LLMInsight(**structured_data['volatility_insights']),
                actionable_guidance=structured_data['actionable_guidance'],
                overall_confidence=structured_data['overall_confidence'],
                human_readable_summary=structured_data['human_readable_summary']
            )

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM JSON response: {result_text}")
            raise Exception(f"Invalid JSON response from LLM: {str(e)}")
        except Exception as e:
            logger.error(f"Anthropic API structured analysis failed: {str(e)}")
            raise
