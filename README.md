# TradrFin 🚀

**Multi-Agent Financial Market Analysis System**

A sophisticated multi-agent AI system that combines news sentiment analysis, technical market indicators, and cross-verification logic to provide intelligent trading insights. Built for hackathon submission targeting **Anthropic (Best Use of Claude)** and **Apify** tracks.

---

## 🏗️ Architecture Overview

TradrFin uses a **4-Agent Multi-Agent System** to analyze financial markets:

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend Dashboard                       │
│                    (React + Tailwind CSS)                   │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌──────────────────────────────┐
        │                              │
┌───────▼──────┐                 ┌─────▼──────────┐
│  Backend API │                 │  Apify Actor   │
│  (Node.js)   │                 │  (Sentiment)   │
└───────┬──────┘                 └─────┬──────────┘
        │                              │
        └───────┬───────────────┬──────┘
                │               │
    ┌───────────▼───────────────▼───────────────┐
    │         Multi-Agent System                │
    ├───────────────────────────────────────────┤
    │  Agent 1: News & Social Sentiment Agent   │
    │  Agent 2: Asset Movement Diagnostics      │
    │  Agent 3: Cross-Verification Agent        │
    │  Agent 4: User-facing Advisor Agent       │
    └───────────────────────────────────────────┘
```

---

## 🤖 The 4-Agent System

### Agent 1: News & Social Sentiment Agent 📰

**Purpose:** Understand market mood from news and social signals

**Inputs:**
- Financial news headlines (Google News RSS, Reuters RSS)
- Market-wide sentiment indices
- Social sentiment data

**Outputs:**
- Overall sentiment: Bullish/Bearish/Neutral
- Sector-level sentiment (tech, finance, energy)
- Key drivers (inflation, earnings, geopolitics)
- Confidence score (0-1)

**Data Sources:**
- Finnhub News Sentiment API
- Google News RSS feeds
- Reuters RSS feeds
- Apify Actor for data collection

**Implementation:**
- Location: `agents/news_sentiment_agent/`
- Uses Claude (Anthropic) for sentiment analysis
- Deployed as Apify Actor

---

### Agent 2: Asset Movement Diagnostics Agent 📈

**Purpose:** Analyze real market behavior through technical indicators

**Inputs:**
- Price candles (1d or 1h)
- Volume changes
- Volatility (ATR - Average True Range)
- Momentum indicators (RSI, MACD)
- Market indices (S&P500, NASDAQ, BTC)

**Outputs:**
- Market trend assessment (upward/downward/neutral)
- Momentum strength
- Volume analysis
- Asset-specific signals (AAPL, TSLA, GOOG, etc.)

**Technical Indicators:**
- **Trend/Momentum:** 20-day MA vs 50-day MA
- **Volatility:** ATR (Average True Range)
- **Volume:** Today's volume vs 5-day moving average
- **RSI:** 51-70 = bullish, 30-50 = neutral, <30 = oversold

**Data Sources:**
- yfinance (free tier)
- AlphaVantage (free tier)
- Finnhub (free tier)

**Implementation:**
- Location: `agents/decision agent/`
- Precomputes indicators via `precompute_indicators.py`
- Analyzes historical data for multiple symbols

---

### Agent 3: Cross-Verification Agent 🧠 (The "Brain")

**Purpose:** Validate sentiment against actual price action - the "magic" that adds intelligence

**Logic Examples:**

**Scenario 1: Contradiction Detection**
```
Sentiment = Bullish
Price Trend = Down
Volume = Low
→ Output: "Sentiment is positive but price action contradicts it. 
           Market may be in distribution or false hype."
```

**Scenario 2: Contrarian Setup**
```
Sentiment = Bearish
Price Trend = Up
Volatility = High
→ Output: "Market is climbing despite fear. 
           Likely short squeeze or contrarian setup."
```

**Outputs:**
- Final combined sentiment (Bullish/Neutral/Bearish)
- Confidence score (0-1)
- Plain English explanation
- 3 key reasons for the assessment

**Implementation:**
- Location: `agents/decision agent/decision_agent.py`
- Uses Claude LLM for intelligent cross-verification
- Rule-based fallback mode available

---

### Agent 4: User-facing Advisor Agent 💬

**Purpose:** Transform all internal signals into actionable insights for users

**Outputs:**
- Clean, readable summary
- Actionable trading insights
- Visual signals (Green/Bullish, Red/Bearish, Yellow/Neutral)
- Beginner-friendly explanations

**Implementation:**
- Location: `backend/server.js` (POST `/api/chat`)
- Frontend: `frontend/src/pages/Advisor.jsx`
- Provides conversational interface

---

## 📊 Example Output

```
Market Sentiment: Bearish (score: 0.32)
Asset Trend: Bullish (score: 0.65)
Final Verdict: Neutral – conflicting signals
Confidence: 0.41

Explanation:
Headlines show strong concerns about inflation and slowing earnings.
BUT the S&P500 is in a short-term uptrend with strong buying volume.
This is often seen during short-covering or temporary relief rallies.

Recommendation:
Wait for confirmation before making large trades.
```

---

## 🛠️ Tech Stack

### Frontend
- **React 19.2.0** - UI framework
- **Vite** - Build tool with Rolldown
- **Tailwind CSS** - Styling
- **React Router** - Navigation
- **Recharts** - Data visualization

### Backend
- **Node.js/Express** - FinTech Dashboard API (port 5000)
- **Python/FastAPI** - Trading Simulation API (port 8000)
- **MySQL** - Cloud database for sentiment and market data

### AI & Data
- **Claude (Anthropic)** - Sentiment analysis and decision-making
- **Apify** - News collection and data processing
- **yfinance** - Market data fetching
- **Pandas** - Data processing

### Agents
- **Apify Actor** - News sentiment collection
- **Python Agents** - Decision making and execution
- **FastAPI** - Agent orchestration

---

## 🚀 Quick Start

### Prerequisites

- Node.js 16+
- Python 3.8+
- MySQL database (cloud or local)
- Anthropic API key
- Apify account (optional, for actor deployment)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd TradrFin
   ```

2. **Setup Backend (Node.js):**
   ```bash
   cd backend
   npm install
   ```
   
   Create `.env` file:
   ```env
   DB_HOST=your-database-host.com
   DB_USER=your-username
   DB_PASSWORD=your-password
   DB_NAME=your-database-name
   DB_PORT=3306
   DB_SSL=true
   PORT=5000
   ```

3. **Setup Backend (Python):**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Setup Frontend:**
   ```bash
   cd frontend
   npm install
   ```

5. **Setup Sentiment Agent (Apify):**
   ```bash
   cd agents/news_sentiment_agent
   npm install
   ```

6. **Precompute Market Indicators:**
   ```bash
   cd agents/decision\ agent
   python precompute_indicators.py
   ```

### Running the Application

**Terminal 1 - Node.js Backend:**
```bash
cd backend
npm start
# Server runs on http://localhost:5000
```

**Terminal 2 - Python FastAPI Backend:**
```bash
cd backend
uvicorn app:app --reload --port 8000
# Server runs on http://localhost:8000
# API docs at http://localhost:8000/docs
```

**Terminal 3 - Frontend:**
```bash
cd frontend
npm run dev
# App runs on http://localhost:5173
```

---

## 📁 Project Structure

```
TradrFin/
├── agents/
│   ├── decision agent/          # Agent 2 & 3: Market analysis & cross-verification
│   │   ├── decision_agent.py    # Cross-verification logic with Claude
│   │   ├── execution_agent.py    # Trade execution
│   │   ├── trading_simulator.py  # Simulation engine
│   │   └── precompute_indicators.py  # Technical indicator computation
│   └── news_sentiment_agent/     # Agent 1: Sentiment collection (Apify Actor)
│       ├── src/main.js           # Apify Actor implementation
│       └── actor.json            # Actor configuration
├── backend/
│   ├── server.js                # Node.js API (Agent 4: Advisor)
│   ├── app.py                    # FastAPI (Trading simulation)
│   └── requirements.txt          # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Advisor.jsx       # Agent 4 UI
│   │   │   ├── Sentiment.jsx     # Agent 1 visualization
│   │   │   └── Technicals.jsx    # Agent 2 visualization
│   │   └── components/           # Reusable components
│   └── package.json
└── README.md
```

---

## 🔌 API Endpoints

### Node.js Backend (Port 5000)

- `GET /api/health` - Health check
- `GET /api/sentiment` - Get sentiment analysis data
- `GET /api/market-data` - Get market technical data
- `GET /api/transactions` - Get transaction history
- `POST /api/chat` - AI chat endpoint (Agent 4)

### FastAPI Backend (Port 8000)

- `GET /` - API information
- `POST /demo` - Run trading simulation
- `GET /portfolio` - Get current portfolio state
- `GET /status` - Get simulation status
- `GET /logs` - List trading log files

See `backend/README.md` for detailed API documentation.

---

## 🎯 Key Features

✅ **Multi-Agent Architecture** - 4 specialized agents working together  
✅ **Claude AI Integration** - Advanced sentiment analysis and decision-making  
✅ **Apify Actor** - Scalable news collection and processing  
✅ **Cross-Verification Logic** - Validates sentiment against price action  
✅ **Real-time Market Analysis** - Technical indicators and trend detection  
✅ **Interactive Dashboard** - Beautiful React UI with real-time updates  
✅ **Trading Simulation** - Backtest strategies with historical data  
✅ **Confidence Scoring** - Transparent AI decision-making  

---

## 📈 How It Works

1. **Agent 1** collects financial news and analyzes sentiment using Claude
2. **Agent 2** computes technical indicators (RSI, MACD, ATR, Volume)
3. **Agent 3** cross-verifies sentiment vs. price action, generates final signal
4. **Agent 4** presents insights in user-friendly format via chat interface

The system flags contradictions (e.g., bullish sentiment but bearish price action) and provides explanations, making it valuable for both beginners and experienced traders.

---

## 🧪 Testing

### Test Sentiment Agent (Apify)
```bash
cd agents/news_sentiment_agent
apify run --input='{"query":"NVIDIA","maxNewsItems":10}'
```

### Test Decision Agent
```bash
cd agents/decision\ agent
python test_decision_agent.py
```

### Test Backtester
```bash
cd agents/decision\ agent
python test_backtester.py
```

---

## 📝 Database Schema

The system expects these tables in your MySQL database:

- `sentiment_agent` - Sentiment analysis results
- `market_data_agent` - Technical market data
- `asset_movement_agent` - Transaction records

---

## 🎨 Frontend Pages

- `/` - Banking Dashboard
- `/advisor` - AI Financial Advisor (Agent 4)
- `/sentiment` - Market Sentiment Analysis (Agent 1)
- `/technicals` - Technical Analysis (Agent 2)
- `/ai-invest` - AI Investment Tools
- `/history` - Transaction History
- `/transfers` - Money Transfers

---

## 🔐 Environment Variables

### Backend (.env)
```env
DB_HOST=your-database-host
DB_USER=your-username
DB_PASSWORD=your-password
DB_NAME=your-database-name
DB_PORT=3306
DB_SSL=true
PORT=5000
```

### Apify Actor
```env
ANTHROPIC_API_KEY=your-anthropic-api-key
```

---

## 🚧 Development Status

- ✅ Agent 1: News & Social Sentiment (Apify Actor)
- ✅ Agent 2: Asset Movement Diagnostics
- ✅ Agent 3: Cross-Verification Agent
- ✅ Agent 4: User-facing Advisor
- ✅ Frontend Dashboard
- ✅ Backend APIs
- ✅ Trading Simulation

---

## 📚 Documentation

- `backend/README.md` - Detailed backend API documentation
- `frontend/README.md` - Frontend setup and structure
- `agents/news_sentiment_agent/README.md` - Apify Actor documentation
- `agents/decision agent/DESIGN_PLAN.md` - Agent design details

---

## 🤝 Contributing

This is a hackathon project. For questions or improvements, please open an issue or submit a pull request.

---

## 📄 License

This project is part of a hackathon submission.

---

## 🏆 Hackathon Highlights

- **Best Use of Claude**: Leverages Claude for intelligent sentiment analysis and cross-verification
- **Apify Integration**: Custom Apify Actor for scalable news collection
- **Multi-Agent Design**: 4 specialized agents working in harmony
- **Real-world Application**: Practical trading insights with confidence scoring
- **Judge-friendly Output**: Clear explanations and actionable recommendations

---

**Built with ❤️ for the hackathon**
