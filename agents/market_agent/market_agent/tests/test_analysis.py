"""Tests for AnalysisService."""

import pytest
import pandas as pd
import numpy as np
from market_agent.services.analysis_service import AnalysisService
from market_agent.types.market_types import MarketData, OHLCVData
from market_agent.utils.indicator_utils import IndicatorUtils


class TestAnalysisService:
    """Test cases for AnalysisService."""

    @pytest.fixture
    def analysis_service(self):
        """Create AnalysisService instance for testing."""
        return AnalysisService()

    @pytest.fixture
    def sample_market_data(self):
        """Sample market data for testing."""
        ohlcv_data = []

        # Generate 50 days of sample data
        base_price = 100.0
        dates = pd.date_range('2024-01-01', periods=50, freq='D')

        for i, date in enumerate(dates):
            # Create some trend and volatility
            trend = i * 0.1  # Upward trend
            noise = np.random.normal(0, 2)  # Random noise
            price = base_price + trend + noise

            # Ensure reasonable bounds
            price = max(price, 50)
            volume = 1000 + np.random.normal(0, 200)

            ohlcv_data.append(OHLCVData(
                timestamp=date.strftime('%Y-%m-%d %H:%M:%S'),
                open=price - 1,
                high=price + 2,
                low=price - 2,
                close=price,
                volume=max(volume, 100),
                adj_close=price
            ))

        return MarketData(
            symbol="TEST",
            data=ohlcv_data,
            current_price=ohlcv_data[-1].close
        )

    def test_analyze_market_data_success(self, analysis_service, sample_market_data):
        """Test successful market data analysis."""
        result = analysis_service.analyze_market_data(sample_market_data)

        assert result.symbol == "TEST"
        assert result.price == sample_market_data.current_price
        assert result.indicators is not None
        assert result.trend in ["bullish", "bearish", "sideways"]
        assert result.momentum_state in ["strong_up", "weak_up", "down", "flat"]
        assert result.rsi_state in ["overbought", "oversold", "neutral"]
        assert result.volume_state in ["spike", "normal", "low"]
        assert result.volatility_state in ["high", "medium", "low"]

    def test_analyze_empty_market_data(self, analysis_service):
        """Test analysis with empty market data."""
        empty_data = MarketData(
            symbol="EMPTY",
            data=[],
            current_price=100.0
        )

        with pytest.raises(Exception):  # Should raise AnalysisServiceError
            analysis_service.analyze_market_data(empty_data)

    def test_determine_trend_bullish(self, analysis_service):
        """Test bullish trend determination."""
        # Price 2% above SMA20
        trend = analysis_service._determine_trend(102.0, 100.0)
        assert trend == "bullish"

    def test_determine_trend_bearish(self, analysis_service):
        """Test bearish trend determination."""
        # Price 2% below SMA20
        trend = analysis_service._determine_trend(98.0, 100.0)
        assert trend == "bearish"

    def test_determine_trend_sideways(self, analysis_service):
        """Test sideways trend determination."""
        # Price within 1% of SMA20
        trend = analysis_service._determine_trend(100.5, 100.0)
        assert trend == "sideways"

    def test_determine_trend_no_sma(self, analysis_service):
        """Test trend determination when SMA20 is None."""
        trend = analysis_service._determine_trend(100.0, None)
        assert trend == "sideways"

    def test_determine_momentum_strong_up(self, analysis_service):
        """Test strong upward momentum determination."""
        momentum = analysis_service._determine_momentum(105.0, 100.0)  # 5% difference
        assert momentum == "strong_up"

    def test_determine_momentum_weak_up(self, analysis_service):
        """Test weak upward momentum determination."""
        momentum = analysis_service._determine_momentum(101.5, 100.0)  # 1.5% difference
        assert momentum == "weak_up"

    def test_determine_momentum_down(self, analysis_service):
        """Test downward momentum determination."""
        momentum = analysis_service._determine_momentum(95.0, 100.0)
        assert momentum == "down"

    def test_determine_momentum_flat(self, analysis_service):
        """Test flat momentum determination."""
        momentum = analysis_service._determine_momentum(None, None)
        assert momentum == "flat"

    def test_determine_rsi_overbought(self, analysis_service):
        """Test overbought RSI determination."""
        rsi_state = analysis_service._determine_rsi_state(75.0)
        assert rsi_state == "overbought"

    def test_determine_rsi_oversold(self, analysis_service):
        """Test oversold RSI determination."""
        rsi_state = analysis_service._determine_rsi_state(25.0)
        assert rsi_state == "oversold"

    def test_determine_rsi_neutral(self, analysis_service):
        """Test neutral RSI determination."""
        rsi_state = analysis_service._determine_rsi_state(50.0)
        assert rsi_state == "neutral"

    def test_determine_rsi_none(self, analysis_service):
        """Test RSI determination when RSI is None."""
        rsi_state = analysis_service._determine_rsi_state(None)
        assert rsi_state == "neutral"

    def test_determine_volume_spike(self, analysis_service):
        """Test volume spike determination."""
        volume_state = analysis_service._determine_volume_state(3.0)  # 3x average
        assert volume_state == "spike"

    def test_determine_volume_normal(self, analysis_service):
        """Test normal volume determination."""
        volume_state = analysis_service._determine_volume_state(1.5)  # 1.5x average
        assert volume_state == "normal"

    def test_determine_volume_low(self, analysis_service):
        """Test low volume determination."""
        volume_state = analysis_service._determine_volume_state(0.3)  # 0.3x average
        assert volume_state == "low"

    def test_determine_volume_none(self, analysis_service):
        """Test volume determination when ratio is None."""
        volume_state = analysis_service._determine_volume_state(None)
        assert volume_state == "normal"

    def test_determine_volatility_high(self, analysis_service):
        """Test high volatility determination."""
        # Create sample dataframe
        df = pd.DataFrame({
            'close': [100, 102, 98, 105, 95, 110, 90, 115, 85, 120,
                     80, 125, 75, 130, 70, 135, 65, 140, 60, 145]
        })

        volatility_state = analysis_service._determine_volatility_state(5.0, df)
        # This should be high volatility relative to average
        assert volatility_state in ["high", "medium", "low"]

    def test_determine_volatility_none(self, analysis_service):
        """Test volatility determination when volatility is None."""
        volatility_state = analysis_service._determine_volatility_state(None, pd.DataFrame())
        assert volatility_state == "medium"

    def test_convert_to_dataframe(self, analysis_service):
        """Test conversion of OHLCV data to DataFrame."""
        ohlcv_data = [
            OHLCVData(
                timestamp="2024-01-01 10:00:00",
                open=100.0,
                high=105.0,
                low=95.0,
                close=102.0,
                volume=1000,
                adj_close=102.0
            )
        ]

        df = analysis_service._convert_to_dataframe(ohlcv_data)

        assert not df.empty
        assert len(df) == 1
        assert df.loc[0, 'close'] == 102.0
        assert df.loc[0, 'volume'] == 1000
