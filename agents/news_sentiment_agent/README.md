# Financial Sentiment Collector - Apify Actor

A custom Apify Actor that collects financial news and analyzes sentiment using Claude (Anthropic) for market analysis.

## Features

- 📰 Collects financial news from **Google News RSS** and **Reuters RSS**
- 🧠 **Sentiment analysis** using **Claude (Anthropic)** AI
- 📊 Collects social sentiment from trusted news sources (Yahoo Finance, fallback to news articles)
- 💾 Saves structured data to Apify dataset
- 🔧 Configurable via input schema

## Data Sources

### News Sources (Working)
1. **Google News RSS** - Aggregates news from multiple financial outlets
2. **Reuters RSS** - Direct from Reuters business news

### Social Sentiment Sources
- Yahoo Finance Community (attempted, often fails)
- Fallback: Uses news articles as sentiment data

### AI Analysis
- **Claude (Anthropic)** - Analyzes collected data for sentiment

## Setup

1. **Install dependencies:**
   ```bash
   cd actor
   npm install
   ```

2. **Set environment variables:**
   - `ANTHROPIC_API_KEY` - Your Anthropic API key (for Claude)
   - Set in Apify Console → Actor Settings → Environment Variables

3. **Test locally:**
   ```bash
   apify run --input='{"query":"NVIDIA"}'
   ```

4. **Deploy to Apify:**
   ```bash
   apify push
   ```

## Input Schema

```json
{
  "query": "NVIDIA",
  "maxNewsItems": 10,
  "maxSocialItems": 20,
  "includeSocial": true
}
```

### Parameters

- **query** (required): Financial query to search (e.g., "NVIDIA", "btc", "AAPL", "S&P500")
- **maxNewsItems** (optional, default: 10): Maximum news articles (1-100)
- **maxSocialItems** (optional, default: 20): Maximum social posts (1-100)
- **includeSocial** (optional, default: true): Whether to collect social sentiment

## Output

The actor saves data to the default dataset with the following structure:

```json
{
  "query": "NVIDIA",
  "timestamp": "2024-01-01T00:00:00.000Z",
  "data_sources": {
    "news_count": 10,
    "social_count": 20
  },
  "news_items": [...],
  "social_posts": [...],
  "sentiment_analysis": {
    "overall_sentiment": "bullish|bearish|neutral",
    "confidence_score": 0.75,
    "sector_sentiments": {
      "technology": "bullish",
      "finance": "neutral",
      "energy": "neutral"
    },
    "key_drivers": ["AI growth", "Earnings beat"],
    "summary": "Market sentiment is bullish...",
    "key_themes": ["AI", "Semiconductors"],
    "risk_level": "medium"
  },
  "summary": {
    "total_items": 30,
    "data_quality": "good",
    "news_with_content": 10,
    "sentiment_sources": ["Google News", "Reuters", "news_articles"]
  }
}
```

## Usage

### Via Python Script
```bash
python agent1_sentiment_custom.py "btc" --actor-id "your-username/financial-sentiment-collector"
```

### Via Apify CLI
```bash
cd actor
apify run --input='{"query":"NVIDIA","maxNewsItems":15}'
```

### Via Apify Console
1. Go to your actor in Apify Console
2. Click "Start"
3. Enter input JSON with your query

## Requirements

- Node.js 16+
- Apify CLI
- Anthropic API key (for Claude sentiment analysis)

## Notes

- Claude integration requires `ANTHROPIC_API_KEY` environment variable
- If Claude API key is not set, sentiment analysis will be skipped
- News sources use RSS feeds (reliable and fast)
- Social media scraping may be blocked (falls back to news articles)
- All data is from trusted financial news sources

