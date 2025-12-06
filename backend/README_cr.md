# FinTech Backend API

This backend provides API endpoints for the FinTech dashboard application, connecting to a cloud database instead of local SQL setup.

## Setup

1. **Install Dependencies:**
   ```bash
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

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/sentiment` - Get sentiment analysis data
- `GET /api/market-data` - Get market technical data
- `GET /api/transactions` - Get transaction history

## Database Tables

The backend expects these tables in your cloud database:

- `sentiment_agent` - Sentiment analysis data
- `market_data_agent` - Technical market data
- `transaction_history` - Transaction records

## Migration from Local SQL

This replaces the previous local SQL/Docker setup with a cloud database connection. Make sure your cloud database has the same table structure as the previous local setup.
