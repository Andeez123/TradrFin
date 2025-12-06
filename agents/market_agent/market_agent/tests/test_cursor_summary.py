"""Tests for SummaryService."""

import pytest
from unittest.mock import Mock, patch
from market_agent.services.cursor_summary import SummaryService
from market_agent.types.market_types import MarketAnalysis, TechnicalIndicators


class TestSummaryService:
    """Test cases for SummaryService."""

    @pytest.fixture
    def summary_service(self):
        """Create SummaryService instance for testing."""
        return SummaryService()

    @pytest.fixture
    def sample_analysis(self):
        """Sample market analysis for testing."""
        return MarketAnalysis(
            symbol="BTC-USD",
            price=45000.0,
            indicators=TechnicalIndicators(
                sma20=44000.0,
                sma50=43000.0,
                ema20=44500.0,
                ema50=43500.0,
                rsi=75.0,
                macd={'macd': 500.0, 'signal': 300.0, 'histogram': 200.0},
                bollinger={'upper': 46000.0, 'middle': 45000.0, 'lower': 44000.0},
                volatility=1500.0,
                momentum=5.2,
                volume_avg=1000000.0,
                volume_spike_ratio=2.5
            ),
            trend="bullish",
            momentum_state="strong_up",
            rsi_state="overbought",
            volume_state="spike",
            volatility_state="high",
            summary=""
        )

    def test_init_with_api_key(self):
        """Test initialization with API key."""
        service = SummaryService(api_key="test-key")
        assert service.api_key == "test-key"
        assert service.client is not None

    def test_init_without_api_key(self):
        """Test initialization without API key."""
        with patch.dict('os.environ', {}, clear=True):
            service = SummaryService()
            assert service.api_key is None
            assert service.client is None

    def test_init_with_env_api_key(self):
        """Test initialization with environment API key."""
        with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'env-key'}):
            service = SummaryService()
            assert service.api_key == 'env-key'
            assert service.client is not None

    @patch('anthropic.Anthropic')
    def test_generate_ai_summary_success(self, mock_anthropic_class, summary_service, sample_analysis):
        """Test successful AI summary generation."""
        # Setup mock client
        mock_client = Mock()
        mock_anthropic_class.return_value = mock_client

        mock_response = Mock()
        mock_response.content = [Mock()]
        mock_response.content[0].text = "BTC is showing strong bullish momentum with overbought RSI conditions."
        mock_client.messages.create.return_value = mock_response

        # Set client for testing
        summary_service.client = mock_client

        result = summary_service._generate_ai_summary(sample_analysis)

        assert "BTC is showing strong bullish momentum" in result
        mock_client.messages.create.assert_called_once()

    @patch('anthropic.Anthropic')
    def test_generate_ai_summary_api_error(self, mock_anthropic_class, summary_service, sample_analysis):
        """Test AI summary generation with API error."""
        mock_client = Mock()
        mock_anthropic_class.return_value = mock_client
        mock_client.messages.create.side_effect = Exception("API Error")

        summary_service.client = mock_client

        with pytest.raises(Exception, match="API Error"):
            summary_service._generate_ai_summary(sample_analysis)

    def test_generate_template_summary_bullish_trend(self, summary_service, sample_analysis):
        """Test template summary generation for bullish trend."""
        result = summary_service._generate_template_summary(sample_analysis)

        assert "BTC-USD is currently trading at $45000.00" in result
        assert "above its 20-period SMA" in result
        assert "Strong upward momentum" in result
        assert "RSI at 75.1 indicates overbought conditions" in result
        assert "Volume spike detected" in result
        assert "Volatility is elevated" in result

    def test_generate_template_summary_bearish_trend(self, summary_service):
        """Test template summary generation for bearish trend."""
        analysis = MarketAnalysis(
            symbol="AAPL",
            price=150.0,
            indicators=TechnicalIndicators(
                sma20=155.0,
                rsi=25.0
            ),
            trend="bearish",
            momentum_state="down",
            rsi_state="oversold",
            volume_state="low",
            volatility_state="low",
            summary=""
        )

        result = summary_service._generate_template_summary(analysis)

        assert "below its 20-period SMA" in result
        assert "Downward momentum" in result
        assert "RSI at 25.0 indicates oversold conditions" in result
        assert "Volume is currently low" in result
        assert "Volatility is low" in result

    def test_generate_template_summary_sideways_trend(self, summary_service):
        """Test template summary generation for sideways trend."""
        analysis = MarketAnalysis(
            symbol="TSLA",
            price=200.0,
            indicators=TechnicalIndicators(
                sma20=199.0,
                rsi=55.0
            ),
            trend="sideways",
            momentum_state="flat",
            rsi_state="neutral",
            volume_state="normal",
            volatility_state="medium",
            summary=""
        )

        result = summary_service._generate_template_summary(analysis)

        assert "within 1% of its 20-period SMA" in result
        assert "Momentum appears flat" in result
        assert "RSI at 55.0 is in neutral territory" in result
        assert "Volume is at normal levels" in result
        assert "Volatility is at moderate levels" in result

    def test_generate_summary_with_ai_client(self, summary_service, sample_analysis):
        """Test generate_summary with AI client available."""
        with patch.object(summary_service, '_generate_ai_summary') as mock_ai:
            mock_ai.return_value = "AI generated summary"
            summary_service.client = Mock()  # Mock client exists

            result = summary_service.generate_summary(sample_analysis)

            assert result == "AI generated summary"
            mock_ai.assert_called_once_with(sample_analysis)

    def test_generate_summary_ai_fallback_to_template(self, summary_service, sample_analysis):
        """Test generate_summary fallback to template when AI fails."""
        with patch.object(summary_service, '_generate_ai_summary') as mock_ai, \
             patch.object(summary_service, '_generate_template_summary') as mock_template:

            mock_ai.side_effect = Exception("AI Error")
            mock_template.return_value = "Template summary"
            summary_service.client = Mock()  # Mock client exists

            result = summary_service.generate_summary(sample_analysis)

            assert result == "Template summary"
            mock_ai.assert_called_once()
            mock_template.assert_called_once()

    def test_generate_summary_template_only(self, summary_service, sample_analysis):
        """Test generate_summary with only template (no AI client)."""
        with patch.object(summary_service, '_generate_template_summary') as mock_template:
            mock_template.return_value = "Template summary"
            summary_service.client = None  # No AI client

            result = summary_service.generate_summary(sample_analysis)

            assert result == "Template summary"
            mock_template.assert_called_once()

    def test_generate_summary_complete_failure(self, summary_service, sample_analysis):
        """Test generate_summary when both AI and template fail."""
        with patch.object(summary_service, '_generate_template_summary') as mock_template:
            mock_template.side_effect = Exception("Template Error")
            summary_service.client = None  # No AI client

            result = summary_service.generate_summary(sample_analysis)

            assert "Unable to generate summary" in result
            assert sample_analysis.symbol in result
