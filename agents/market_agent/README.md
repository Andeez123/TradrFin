# Market Data Agent

A production-ready Python Market Data Agent built as an Apify Actor that fetches market data from Yahoo Finance, computes technical indicators, applies deterministic trading rules, and generates human-readable summaries using Anthropic API.

## Features

- **Market Data Fetching**: Retrieve current price and historical OHLCV data from Yahoo Finance
- **Technical Analysis**: Compute 10+ technical indicators (SMA, EMA, RSI, MACD, Bollinger Bands, etc.)
- **Trading Rules**: Apply deterministic rules for trend, momentum, RSI, volume, and volatility analysis
- **AI Summaries**: Generate human-readable market analysis using Anthropic Claude API
- **Apify Integration**: Deploy as an Apify Actor for serverless execution
- **Fallback Mode**: Template-based summaries when AI API is unavailable

## Architecture

```
market_agent/
├── main.py                 # Apify Actor entry point
├── services/
│   ├── market_service.py   # Yahoo Finance data fetching
│   ├── analysis_service.py # Technical analysis & rules
│   └── cursor_summary.py   # AI summary generation
├── utils/
│   └── indicator_utils.py  # Technical indicator calculations
├── types/
│   └── market_types.py     # Pydantic data models
└── tests/
    ├── test_market_service.py
    ├── test_analysis.py
    └── test_cursor_summary.py
```

## Installation

### Local Development

1. **Clone the repository** (if applicable) or ensure you have the project files

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**:
   ```bash
   export ANTHROPIC_API_KEY="your-anthropic-api-key-here"
   ```
   On Windows:
   ```cmd
   set ANTHROPIC_API_KEY=your-anthropic-api-key-here
   ```

### Apify Deployment

1. **Install Apify CLI**:
   ```bash
   npm install -g apify-cli
   ```

2. **Login to Apify**:
   ```bash
   apify login
   ```

3. **Initialize Apify project** (if not already done):
   ```bash
   apify init
   ```

## Usage

### Input Schema

The agent accepts JSON input with the following structure:

```json
{
  "symbol": "BTC-USD",
  "data_type": "quote|historical",
  "interval": "1h|1d|5m",
  "range": "1mo|3mo|6mo|1y"
}
```

- `symbol`: Stock/crypto symbol (e.g., "BTC-USD", "AAPL", "GOOGL")
- `data_type`: "quote" for current price, "historical" for time series data
- `interval`: Time interval for historical data (required when data_type is "historical")
- `range`: Time range for historical data (required when data_type is "historical")

### Output Schema

The agent returns structured JSON with analysis results:

```json
{
  "symbol": "BTC-USD",
  "price": 45000.0,
  "indicators": {
    "sma20": 44000.0,
    "sma50": 43000.0,
    "ema20": 44500.0,
    "ema50": 43500.0,
    "rsi": 75.0,
    "macd": {"macd": 500.0, "signal": 300.0, "histogram": 200.0},
    "bollinger": {"upper": 46000.0, "middle": 45000.0, "lower": 44000.0},
    "volatility": 1500.0,
    "momentum": 5.2,
    "volume_avg": 1000000.0,
    "volume_spike_ratio": 2.5
  },
  "trend": "bullish",
  "momentum_state": "strong_up",
  "rsi_state": "overbought",
  "volume_state": "spike",
  "volatility_state": "high",
  "summary": "BTC is showing strong bullish momentum...",
  "success": true
}
```

### Local Execution

Run the agent locally with a JSON input file:

```bash
# Using a JSON file
echo '{"symbol": "BTC-USD", "data_type": "historical", "interval": "1d", "range": "1mo"}' | python main.py

# Or with a file
python main.py < input.json
```

Example with inline JSON:
```bash
python main.py '{"symbol": "AAPL", "data_type": "quote"}'
```

### Apify Actor Execution

1. **Deploy to Apify**:
   ```bash
   apify push
   ```

2. **Run the Actor**:
   ```bash
   apify call your-actor-id --input '{"symbol": "BTC-USD", "data_type": "historical", "interval": "1d", "range": "1mo"}'
   ```

3. **Run via Apify Console**:
   - Go to your Actor in Apify Console
   - Click "Run" and provide the input JSON

## Technical Indicators

The agent computes the following technical indicators:

### Trend Indicators
- **SMA20/SMA50**: Simple Moving Averages (20 and 50 periods)
- **EMA20/EMA50**: Exponential Moving Averages (20 and 50 periods)

### Momentum Indicators
- **RSI**: Relative Strength Index (14 periods)
- **MACD**: Moving Average Convergence Divergence (12, 26, 9)

### Volatility Indicators
- **Bollinger Bands**: 20-period bands with 2 standard deviations
- **Volatility**: Standard deviation of closing prices (20 periods)

### Volume Indicators
- **Volume Average**: Average volume over 20 periods
- **Volume Spike Ratio**: Current volume vs average volume

### Custom Indicators
- **Momentum**: Percentage price change over last 10 candles

## Trading Rules

The agent applies deterministic rules to classify market conditions:

### Trend Analysis
- **Bullish**: Price > SMA20 by more than 1%
- **Bearish**: Price < SMA20 by more than 1%
- **Sideways**: Price within ±1% of SMA20

### Momentum Analysis
- **Strong Up**: EMA20 > EMA50 by more than 2%
- **Weak Up**: EMA20 > EMA50 by 0-2%
- **Down**: EMA20 < EMA50
- **Flat**: EMAs are equal or unavailable

### RSI Analysis
- **Overbought**: RSI > 70
- **Oversold**: RSI < 30
- **Neutral**: RSI between 30-70

### Volume Analysis
- **Spike**: Volume > 2× average
- **Normal**: Volume between 0.5× and 2× average
- **Low**: Volume < 0.5× average

### Volatility Analysis
- **High**: Current volatility > 1.5× average volatility
- **Medium**: Current volatility within ±1.5× average
- **Low**: Current volatility < 0.5× average

## Testing

Run the test suite to ensure everything works correctly:

```bash
# Install test dependencies
pip install -r requirements.txt

# Run all tests
pytest

# Run specific test file
pytest market_agent/tests/test_market_service.py

# Run with coverage
pytest --cov=market_agent --cov-report=html
```

### Test Coverage

- **Market Service Tests**: Mock Yahoo Finance API calls, test data fetching logic
- **Analysis Service Tests**: Test indicator calculations and rule applications
- **Summary Service Tests**: Mock Anthropic API, test summary generation and fallbacks

## Configuration

### Environment Variables

- `ANTHROPIC_API_KEY`: Your Anthropic API key for AI summary generation (optional - falls back to template mode)

### Apify Configuration

The `apify.json` file contains Actor configuration:

```json
{
  "name": "market-data-agent",
  "version": "1.0.0",
  "buildTag": "latest",
  "input": {
    "symbol": "BTC-USD",
    "data_type": "historical",
    "interval": "1d",
    "range": "1mo"
  }
}
```

## Error Handling

The agent includes comprehensive error handling:

- **Network Errors**: Retries and fallbacks for Yahoo Finance API issues
- **Invalid Symbols**: Clear error messages for unsupported symbols
- **API Limits**: Graceful handling of rate limits
- **AI API Failures**: Automatic fallback to template-based summaries
- **Data Validation**: Pydantic models ensure input/output integrity

## Performance

- **Data Fetching**: Optimized Yahoo Finance requests with error handling
- **Indicator Calculation**: Efficient pandas/numpy operations
- **AI Summaries**: Cached responses and timeout handling
- **Memory Usage**: Streaming data processing for large datasets

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Check the test suite: `pytest`
- Review logs for error details
- Ensure all dependencies are installed correctly
- Verify API keys are set (for AI summaries)

## Changelog

### v1.0.0
- Initial release with full market data analysis capabilities
- Apify Actor integration
- Anthropic AI summary generation
- Comprehensive test suite
- Template fallback for AI summaries
