"""Type definitions for Market Data Agent."""

from typing import Dict, Any, Optional, List
from enum import Enum
from pydantic import BaseModel, Field, field_validator
import pandas as pd


class DataType(str, Enum):
    """Type of data to fetch."""
    QUOTE = "quote"
    HISTORICAL = "historical"


class Interval(str, Enum):
    """Time interval for historical data."""
    FIVE_MIN = "5m"
    ONE_HOUR = "1h"
    ONE_DAY = "1d"


class TimeRange(str, Enum):
    """Time range for historical data."""
    ONE_MONTH = "1mo"
    THREE_MONTHS = "3mo"
    SIX_MONTHS = "6mo"
    ONE_YEAR = "1y"


class MarketRequest(BaseModel):
    """Input request schema for market data."""
    symbol: Optional[str] = Field(None, description="Single stock/crypto symbol (e.g., 'BTC-USD', 'AAPL')")
    symbols: Optional[List[str]] = Field(None, description="Multiple symbols to analyze")
    data_type: DataType = Field(..., description="Type of data to fetch")
    interval: Optional[Interval] = Field(None, description="Time interval (required for historical)")
    range: Optional[TimeRange] = Field(None, description="Time range (required for historical)")

    class Config:
        use_enum_values = True


class ApifyOHLCVData(BaseModel):
    """OHLCV data structure from Apify."""
    timestamp: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    adj_close: Optional[float] = None


class ApifyMarketRequest(BaseModel):
    """Input request schema for Apify market data."""
    symbol: str = Field(..., description="Stock/crypto symbol")
    historical: list[ApifyOHLCVData] = Field(..., description="OHLCV historical data from Apify")


class OHLCVData(BaseModel):
    """OHLCV (Open, High, Low, Close, Volume) data structure."""
    timestamp: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    adj_close: Optional[float] = None


class MarketData(BaseModel):
    """Market data response containing OHLCV data."""
    symbol: str
    data: list[OHLCVData]
    current_price: Optional[float] = None


class TechnicalIndicators(BaseModel):
    """Technical indicators dictionary structure."""
    sma20: Optional[float] = None
    sma50: Optional[float] = None
    ema20: Optional[float] = None
    ema50: Optional[float] = None
    rsi: Optional[float] = None
    macd: Optional[Dict[str, float]] = None  # MACD line, signal line, histogram
    bollinger: Optional[Dict[str, float]] = None  # upper, middle, lower bands
    volatility: Optional[float] = None  # Standard deviation of closing prices (20 periods)
    momentum: Optional[float] = None  # % price change over last 10 candles
    volume_avg: Optional[float] = None  # Average volume
    volume_spike_ratio: Optional[float] = None  # lastVolume / avgVolume


class TrendState(str, Enum):
    """Trend state based on price vs SMA20."""
    BULLISH = "bullish"
    BEARISH = "bearish"
    SIDEWAYS = "sideways"


class MomentumState(str, Enum):
    """Momentum state based on EMA20 vs EMA50."""
    STRONG_UP = "strong_up"
    WEAK_UP = "weak_up"
    DOWN = "down"
    FLAT = "flat"


class RSIState(str, Enum):
    """RSI state."""
    OVERBOUGHT = "overbought"
    OVERSOLD = "oversold"
    NEUTRAL = "neutral"


class VolumeState(str, Enum):
    """Volume state."""
    SPIKE = "spike"
    NORMAL = "normal"
    LOW = "low"


class VolatilityState(str, Enum):
    """Volatility state."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class MarketAnalysis(BaseModel):
    """Market analysis with computed technical indicators."""
    symbol: str
    price: float
    indicators: TechnicalIndicators
    summary: str


class LLMInsight(BaseModel):
    """Structured LLM insight with confidence metric."""
    insight: str = Field(..., description="Factual insight based on data")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0-1)")
    reasoning: str = Field(..., description="Step-by-step reasoning")


class LLMAnalysis(BaseModel):
    """Complete LLM-generated analysis."""
    trend_analysis: LLMInsight
    momentum_interpretation: LLMInsight
    rsi_insights: LLMInsight
    bollinger_insights: LLMInsight
    volume_insights: LLMInsight
    volatility_insights: LLMInsight
    actionable_guidance: str = Field(..., description="Neutral, factual actionable guidance")
    overall_confidence: float = Field(..., ge=0.0, le=1.0, description="Overall analysis confidence")
    human_readable_summary: str = Field(..., description="Concise human-readable summary (2-3 sentences)")


class MarketResponse(BaseModel):
    """Final response structure."""
    symbol: str
    price: float
    indicators: Dict[str, Any]  # Flattened indicators for JSON response
    summary: str
    llm_analysis: LLMAnalysis

    class Config:
        use_enum_values = True
