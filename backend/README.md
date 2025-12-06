# TradrFin Backend

This backend directory contains two separate API servers serving different purposes:

1. **FinTech Dashboard API** (Node.js/Express) - Provides endpoints for sentiment analysis, market data, and transaction history from a cloud database
2. **Trading Simulation API** (Python/FastAPI) - Provides endpoints to run and monitor autonomous trading simulations

## Architecture

### FinTech Dashboard API (Node.js)
- **`server.js`**: Express server with cloud database connection
- Provides REST endpoints for frontend dashboard data

### Trading Simulation API (Python)
- **`app.py`**: FastAPI application with REST endpoints
- **`agents/decision agent/trading_simulator.py`**: Core trading simulation logic
- **`agents/decision agent/decision_agent.py`**: Decision-making logic
- **`agents/decision agent/execution_agent.py`**: Trade execution logic

---

## FinTech Dashboard API (Node.js/Express)

### Installation

1. Install Node.js dependencies:
```bash
cd backend
npm install
```

2. **Environment Variables:**
   Create a `.env` file in the backend directory with your cloud database credentials:

   ```env
   DB_HOST=your-database-host.com
   DB_USER=your-username
   DB_PASSWORD=your-password
   DB_NAME=your-database-name
   DB_PORT=3306
   DB_SSL=true
   PORT=5000
   ```

3. **Start the Server:**
   ```bash
   npm start
   ```

   For development with auto-restart:
   ```bash
   npm run dev
   ```

   The server will run on `http://localhost:5000` (or the port specified in `.env`)

### API Endpoints

- `GET /api/health` - Health check endpoint
- `GET /api/sentiment` - Get sentiment analysis data (returns last 50 records)
- `GET /api/market-data` - Get market technical data (returns last 100 records)
- `GET /api/transactions` - Get transaction history (returns last 100 records)
- `POST /api/chat` - AI chat endpoint for financial queries

### Database Tables

The backend expects these tables in your cloud database:

- `sentiment_agent` - Sentiment analysis data
- `market_data_agent` - Technical market data
- `asset_movement_agent` - Transaction records

### Example Usage

```bash
# Health check
curl http://localhost:5000/api/health

# Get sentiment data
curl http://localhost:5000/api/sentiment

# Get market data
curl http://localhost:5000/api/market-data

# Get transactions
curl http://localhost:5000/api/transactions

# Chat with AI
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the current market sentiment?"}'
```

---

## Trading Simulation API (Python/FastAPI)

### Installation

1. Install Python dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Ensure precomputed market data is available:
```bash
cd "../agents/decision agent"
python precompute_indicators.py
```

### Running the API

Start the FastAPI server:

```bash
cd backend
uvicorn app:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

API documentation (Swagger UI) will be available at `http://localhost:8000/docs`

### API Endpoints

#### `GET /`
Root endpoint with API information and available endpoints.

#### `POST /demo`
Run a trading simulation with configurable parameters.

**Request Body** (all optional):
```json
{
  "initial_balance": 5000.0,
  "candidate_symbols": ["AAPL", "TSLA", "GOOG", "AMZN", "MSFT"],
  "trade_budget": 1000.0,
  "trade_fee": 5.0,
  "top_n": 2,
  "decision_mode": "rule",
  "interval_seconds": 2
}
```

**Response**:
```json
{
  "status": "completed",
  "message": "Simulation completed successfully",
  "csv_filename": "trading_log_20251207_021639.csv",
  "final_balance": 244.18,
  "final_portfolio": {...},
  "days_simulated": 5
}
```

#### `GET /portfolio`
Get the current portfolio state.

**Response**:
```json
{
  "portfolio": {...},
  "investment_balance": 244.18,
  "day_index": 5
}
```

#### `GET /status`
Get the current simulation status and last run information.

**Response**:
```json
{
  "is_running": false,
  "last_run": {...},
  "current_state": {...}
}
```

#### `GET /logs`
List all available trading log CSV files.

**Response**:
```json
{
  "log_files": ["trading_log_20251207_021639.csv", ...],
  "count": 3,
  "directory": "..."
}
```

#### `GET /logs/{filename}`
Download a specific trading log CSV file.

#### `GET /logs/{filename}/preview?rows=10`
Preview the first N rows of a trading log CSV file.

### Example Usage

#### Using curl

```bash
# Run a simulation with default parameters
curl -X POST http://localhost:8000/demo

# Run a simulation with custom parameters
curl -X POST http://localhost:8000/demo \
  -H "Content-Type: application/json" \
  -d '{
    "initial_balance": 10000,
    "trade_budget": 2000,
    "interval_seconds": 1
  }'

# Get portfolio
curl http://localhost:8000/portfolio

# List logs
curl http://localhost:8000/logs

# Preview a log file
curl http://localhost:8000/logs/trading_log_20251207_021639.csv/preview?rows=5
```

#### Using Python

```python
import requests

# Run simulation
response = requests.post("http://localhost:8000/demo", json={
    "initial_balance": 10000,
    "trade_budget": 2000
})
result = response.json()
print(f"Simulation {result['status']}: {result['message']}")
print(f"Final balance: ${result['final_balance']:.2f}")

# Get portfolio
portfolio = requests.get("http://localhost:8000/portfolio").json()
print(f"Current balance: ${portfolio['investment_balance']:.2f}")
```

### CSV Output Format

The trading logs are saved as CSV files with the following columns:

- `ticker`: Stock symbol (VARCHAR(20))
- `movement_score`: Market movement score (DECIMAL(20,4))
- `action`: Trade action - buy, sell, or hold (VARCHAR(10))
- `quantity`: Number of shares (DECIMAL(20,4))
- `price`: Price per share (DECIMAL(20,4))
- `executed_at`: Timestamp of execution (TIMESTAMP)
- `status`: Transaction status - executed, failed, or pending (VARCHAR(10))
- `summary`: Description/reason for the trade (TEXT)

This format is designed to be directly importable into a database.

---

## Running Both Servers

To run both backend services simultaneously:

1. **Terminal 1** - Start the Node.js server (port 5000):
```bash
cd backend
npm start
```

2. **Terminal 2** - Start the FastAPI server (port 8000):
```bash
cd backend
uvicorn app:app --reload --port 8000
```

Both servers can run concurrently as they use different ports and serve different purposes.
