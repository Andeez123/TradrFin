"""Analysis service for computing technical indicators and applying trading rules."""

import logging
from typing import Dict, Any, Optional
import pandas as pd
from ..types.market_types import (
    MarketData,
    TechnicalIndicators,
    MarketAnalysis
)
from ..utils.indicator_utils import IndicatorUtils

logger = logging.getLogger(__name__)


class AnalysisServiceError(Exception):
    """Custom exception for analysis service errors."""
    pass


class AnalysisService:
    """Service for computing technical indicators and applying trading rules."""

    def __init__(self):
        """Initialize the analysis service."""
        self.logger = logging.getLogger(__name__)
        self.indicator_utils = IndicatorUtils()

    def analyze_market_data(self, market_data: MarketData) -> MarketAnalysis:
        """
        Analyze market data by computing technical indicators only.
        LLM will determine insights from these raw indicators.

        Args:
            market_data: MarketData object with OHLCV data

        Returns:
            MarketAnalysis with computed indicators

        Raises:
            AnalysisServiceError: If analysis fails
        """
        try:
            # Convert OHLCV data to DataFrame
            df = self._convert_to_dataframe(market_data.data)

            if df.empty:
                raise AnalysisServiceError("No market data available for analysis")

            # Compute all technical indicators
            indicators = self._compute_indicators(df)

            return MarketAnalysis(
                symbol=market_data.symbol,
                price=market_data.current_price,
                indicators=indicators,
                summary=""  # Will be filled by LLM service
            )

        except Exception as e:
            self.logger.error(f"Failed to analyze market data for {market_data.symbol}: {str(e)}")
            raise AnalysisServiceError(f"Analysis failed: {str(e)}") from e

    def _convert_to_dataframe(self, ohlcv_data: list) -> pd.DataFrame:
        """
        Convert OHLCV data list to pandas DataFrame.

        Args:
            ohlcv_data: List of OHLCVData objects

        Returns:
            DataFrame with OHLCV columns
        """
        if not ohlcv_data:
            return pd.DataFrame()

        data = []
        for item in ohlcv_data:
            data.append({
                'timestamp': pd.to_datetime(item.timestamp),
                'open': item.open,
                'high': item.high,
                'low': item.low,
                'close': item.close,
                'volume': item.volume,
                'adj_close': item.adj_close or item.close
            })

        df = pd.DataFrame(data)
        df.set_index('timestamp', inplace=True)
        return df

    def _compute_indicators(self, df: pd.DataFrame) -> TechnicalIndicators:
        """
        Compute all technical indicators.

        Args:
            df: DataFrame with OHLCV data

        Returns:
            TechnicalIndicators object with computed values
        """
        return TechnicalIndicators(
            sma20=self.indicator_utils.calculate_sma(df, 20),
            sma50=self.indicator_utils.calculate_sma(df, 50),
            ema20=self.indicator_utils.calculate_ema(df, 20),
            ema50=self.indicator_utils.calculate_ema(df, 50),
            rsi=self.indicator_utils.calculate_rsi(df, 14),
            macd=self.indicator_utils.calculate_macd(df),
            bollinger=self.indicator_utils.calculate_bollinger_bands(df, 20),
            volatility=self.indicator_utils.calculate_volatility(df, 20),
            momentum=self.indicator_utils.calculate_momentum(df, 10),
            volume_avg=self.indicator_utils.calculate_volume_average(df, 20),
            volume_spike_ratio=self.indicator_utils.calculate_volume_spike_ratio(df, 20)
        )

