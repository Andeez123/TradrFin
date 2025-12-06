"""Utility functions for calculating technical indicators."""

import logging
from typing import Dict, Optional, Tuple
import pandas as pd
import numpy as np
from ta.trend import SMAIndicator, EMAIndicator, MACD
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands

logger = logging.getLogger(__name__)


class IndicatorError(Exception):
    """Custom exception for indicator calculation errors."""
    pass


class IndicatorUtils:
    """Utility class for technical indicator calculations."""

    @staticmethod
    def calculate_sma(data: pd.DataFrame, period: int, column: str = 'close') -> Optional[float]:
        """
        Calculate Simple Moving Average.

        Args:
            data: DataFrame with OHLCV data
            period: Period for SMA calculation
            column: Column name to use for calculation

        Returns:
            Latest SMA value or None if insufficient data
        """
        try:
            if len(data) < period:
                return None

            sma = SMAIndicator(close=data[column], window=period)
            result = sma.sma_indicator()
            return result.iloc[-1] if not result.empty else None

        except Exception as e:
            logger.warning(f"Failed to calculate SMA{period}: {str(e)}")
            return None

    @staticmethod
    def calculate_ema(data: pd.DataFrame, period: int, column: str = 'close') -> Optional[float]:
        """
        Calculate Exponential Moving Average.

        Args:
            data: DataFrame with OHLCV data
            period: Period for EMA calculation
            column: Column name to use for calculation

        Returns:
            Latest EMA value or None if insufficient data
        """
        try:
            if len(data) < period:
                return None

            ema = EMAIndicator(close=data[column], window=period)
            result = ema.ema_indicator()
            return result.iloc[-1] if not result.empty else None

        except Exception as e:
            logger.warning(f"Failed to calculate EMA{period}: {str(e)}")
            return None

    @staticmethod
    def calculate_rsi(data: pd.DataFrame, period: int = 14, column: str = 'close') -> Optional[float]:
        """
        Calculate Relative Strength Index.

        Args:
            data: DataFrame with OHLCV data
            period: Period for RSI calculation (default 14)
            column: Column name to use for calculation

        Returns:
            Latest RSI value or None if insufficient data
        """
        try:
            if len(data) < period + 1:  # RSI needs extra data for calculation
                return None

            rsi = RSIIndicator(close=data[column], window=period)
            result = rsi.rsi()
            return result.iloc[-1] if not result.empty else None

        except Exception as e:
            logger.warning(f"Failed to calculate RSI{period}: {str(e)}")
            return None

    @staticmethod
    def calculate_macd(data: pd.DataFrame, column: str = 'close') -> Optional[Dict[str, float]]:
        """
        Calculate MACD (12, 26, 9).

        Args:
            data: DataFrame with OHLCV data
            column: Column name to use for calculation

        Returns:
            Dictionary with MACD line, signal line, and histogram or None if insufficient data
        """
        try:
            if len(data) < 26:  # MACD needs at least 26 periods
                return None

            macd = MACD(close=data[column], window_slow=26, window_fast=12, window_sign=9)
            macd_line = macd.macd()
            signal_line = macd.macd_signal()
            histogram = macd.macd_diff()

            if macd_line.empty or signal_line.empty or histogram.empty:
                return None

            return {
                'macd': macd_line.iloc[-1],
                'signal': signal_line.iloc[-1],
                'histogram': histogram.iloc[-1]
            }

        except Exception as e:
            logger.warning(f"Failed to calculate MACD: {str(e)}")
            return None

    @staticmethod
    def calculate_bollinger_bands(data: pd.DataFrame, period: int = 20, column: str = 'close') -> Optional[Dict[str, float]]:
        """
        Calculate Bollinger Bands (20 periods, 2 std dev).

        Args:
            data: DataFrame with OHLCV data
            period: Period for Bollinger Bands calculation (default 20)
            column: Column name to use for calculation

        Returns:
            Dictionary with upper, middle, and lower bands or None if insufficient data
        """
        try:
            if len(data) < period:
                return None

            bb = BollingerBands(close=data[column], window=period, window_dev=2)
            upper = bb.bollinger_hband()
            middle = bb.bollinger_mavg()
            lower = bb.bollinger_lband()

            if upper.empty or middle.empty or lower.empty:
                return None

            return {
                'upper': upper.iloc[-1],
                'middle': middle.iloc[-1],
                'lower': lower.iloc[-1]
            }

        except Exception as e:
            logger.warning(f"Failed to calculate Bollinger Bands{period}: {str(e)}")
            return None

    @staticmethod
    def calculate_volatility(data: pd.DataFrame, period: int = 20, column: str = 'close') -> Optional[float]:
        """
        Calculate volatility as standard deviation of closing prices.

        Args:
            data: DataFrame with OHLCV data
            period: Period for volatility calculation (default 20)
            column: Column name to use for calculation

        Returns:
            Standard deviation of closing prices over the period or None if insufficient data
        """
        try:
            if len(data) < period:
                return None

            # Calculate rolling standard deviation
            volatility = data[column].rolling(window=period).std()
            return volatility.iloc[-1] if not volatility.empty else None

        except Exception as e:
            logger.warning(f"Failed to calculate volatility{period}: {str(e)}")
            return None

    @staticmethod
    def calculate_momentum(data: pd.DataFrame, period: int = 10, column: str = 'close') -> Optional[float]:
        """
        Calculate momentum as percentage price change over last N candles.

        Args:
            data: DataFrame with OHLCV data
            period: Period for momentum calculation (default 10)
            column: Column name to use for calculation

        Returns:
            Percentage price change over the period or None if insufficient data
        """
        try:
            if len(data) < period + 1:
                return None

            # Calculate percentage change from period ago to now
            current_price = data[column].iloc[-1]
            past_price = data[column].iloc[-period-1]
            momentum = ((current_price - past_price) / past_price) * 100
            return momentum

        except Exception as e:
            logger.warning(f"Failed to calculate momentum{period}: {str(e)}")
            return None

    @staticmethod
    def calculate_volume_average(data: pd.DataFrame, period: int = 20, column: str = 'volume') -> Optional[float]:
        """
        Calculate average volume over a period.

        Args:
            data: DataFrame with OHLCV data
            period: Period for average volume calculation (default 20)
            column: Column name to use for calculation

        Returns:
            Average volume over the period or None if insufficient data
        """
        try:
            if len(data) < period:
                return None

            avg_volume = data[column].rolling(window=period).mean()
            return avg_volume.iloc[-1] if not avg_volume.empty else None

        except Exception as e:
            logger.warning(f"Failed to calculate average volume{period}: {str(e)}")
            return None

    @staticmethod
    def calculate_volume_spike_ratio(data: pd.DataFrame, avg_period: int = 20, column: str = 'volume') -> Optional[float]:
        """
        Calculate volume spike ratio (last volume / average volume).

        Args:
            data: DataFrame with OHLCV data
            avg_period: Period for calculating average volume (default 20)
            column: Column name to use for calculation

        Returns:
            Ratio of last volume to average volume or None if insufficient data
        """
        try:
            if len(data) < avg_period + 1:
                return None

            avg_volume = IndicatorUtils.calculate_volume_average(data, avg_period, column)
            if avg_volume is None or avg_volume == 0:
                return None

            last_volume = data[column].iloc[-1]
            return last_volume / avg_volume

        except Exception as e:
            logger.warning(f"Failed to calculate volume spike ratio: {str(e)}")
            return None
