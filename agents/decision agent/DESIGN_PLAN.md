# Stock Investing Agent - Design Plan

## System Architecture

```
┌─────────────────┐
│   FastAPI App   │  (app.py - Main API Server)
└────────┬────────┘
         │
         ├─────────────────┐
         │                 │
┌────────▼────────┐  ┌─────▼──────────┐
│ Decision Agent  │  │ Buy/Sell Algo  │
│ (decision_agent)│  │ (buy_sell_algo) │
└────────┬────────┘  └─────────────────┘
         │
         ├──────────────────┬──────────────────┐
         │                  │                  │
┌────────▼────────┐  ┌──────▼───────┐  ┌──────▼────────┐
│ Sentiment API   │  │ Market Data  │  │ Claude LLM     │
│ Endpoint        │  │ Endpoint     │  │ (Anthropic)    │
└─────────────────┘  └──────────────┘  └────────────────┘
```

## Components

### 1. Decision Agent (`decision_agent.py`)
**Responsibilities:**
- Fetch market sentiment data from sentiment endpoint
- Fetch market data from market data endpoint
- Aggregate data and prepare features for LLM
- Call Claude LLM for initial decision recommendation
- Apply final decision algorithm considering:
  - User's available balance
  - Trading fees
  - Position sizing
  - Risk management
- Return final BUY/SELL/HOLD decision with quantities

**Key Functions:**
- `fetch_sentiment(symbol)` - Calls sentiment endpoint
- `fetch_market_data(symbol)` - Calls market data endpoint
- `query_claude_llm(features, portfolio, balance, fee)` - Gets LLM recommendation
- `final_decision_algorithm(llm_decision, balance, fee, price, portfolio)` - Final decision logic
- `make_decision(symbol, portfolio, balance, fee)` - Main entry point

### 2. Final Decision Algorithm
**Logic Flow:**
1. Receive LLM recommendation (BUY/SELL/HOLD with confidence)
2. Validate against constraints:
   - **For BUY:**
     - Check if balance >= (budget + fee)
     - Calculate max affordable shares: `floor((balance - fee) / price)`
     - Apply position sizing rules (max % of portfolio)
     - Only execute if confidence > threshold AND affordable
   - **For SELL:**
     - Check if position exists in portfolio
     - Verify sufficient shares to sell
     - Only execute if confidence > threshold
3. Return final decision with:
   - Action (BUY/SELL/HOLD)
   - Quantity (shares)
   - Confidence score
   - Reasoning
   - Cost breakdown (including fees)

### 3. Data Flow

```
User Request (symbol, budget, fee)
    ↓
Decision Agent
    ↓
    ├─→ Fetch Sentiment Data (async)
    ├─→ Fetch Market Data (async)
    ↓
Combine Features
    ↓
Query Claude LLM
    ↓
Get LLM Recommendation
    ↓
Apply Final Decision Algorithm
    ├─→ Check Balance
    ├─→ Calculate Fees
    ├─→ Determine Quantity
    ├─→ Risk Validation
    ↓
Return Final Decision
    ↓
App.py executes trade (if action != HOLD)
```

## Decision Algorithm Details

### Input Parameters
- `symbol`: Stock symbol
- `portfolio`: Current holdings {symbol: {shares, avg_cost}}
- `balance`: Available cash
- `fee`: Trading fee per transaction
- `max_position_pct`: Maximum % of portfolio per position (default: 20%)

### Decision Logic

**BUY Decision:**
```python
if llm_action == "BUY" and confidence > buy_threshold:
    available_after_fee = balance - fee
    max_shares_by_budget = floor(available_after_fee / price)
    max_shares_by_position = floor((portfolio_value * max_position_pct) / price)
    quantity = min(llm_suggested_quantity, max_shares_by_budget, max_shares_by_position)
    
    total_cost = (quantity * price) + fee
    if total_cost <= balance and quantity > 0:
        return BUY with quantity
    else:
        return HOLD (insufficient funds)
```

**SELL Decision:**
```python
if llm_action == "SELL" and confidence > sell_threshold:
    if symbol in portfolio:
        available_shares = portfolio[symbol]["shares"]
        quantity = min(llm_suggested_quantity, available_shares)
        if quantity > 0:
            return SELL with quantity
    return HOLD (no position to sell)
```

**HOLD Decision:**
- LLM recommends HOLD
- Confidence below threshold
- Constraints not met (insufficient funds/shares)
- Risk management rules triggered

## Claude LLM Integration

**Model:** `claude-3-sonnet-20240229` or `claude-3-5-sonnet-20241022`

**Prompt Structure:**
1. System message: Define role and output format
2. User message: Include:
   - Market sentiment data
   - Market data (price, volume, indicators)
   - Current portfolio
   - Available balance
   - Trading fee
   - Request JSON response with action, confidence, suggested_quantity, reasoning

**Response Format:**
```json
{
  "action": "BUY|SELL|HOLD",
  "confidence": 0.0-1.0,
  "suggested_quantity": number,
  "reasoning": "explanation"
}
```

## Error Handling

1. **Endpoint Failures:**
   - Retry logic with exponential backoff
   - Fallback to cached data if available
   - Return HOLD with error reason

2. **LLM Failures:**
   - Retry with timeout
   - Fallback to rule-based decision
   - Return HOLD with error reason

3. **Data Validation:**
   - Validate price > 0
   - Validate balance >= 0
   - Validate fee >= 0
   - Sanitize symbol input

## Configuration

Environment Variables:
- `ANTHROPIC_API_KEY`: Claude API key
- `SENTIMENT_AGENT_URL`: Sentiment endpoint URL
- `MARKET_AGENT_URL`: Market data endpoint URL
- `BUY_CONFIDENCE_THRESHOLD`: Minimum confidence for BUY (default: 0.6)
- `SELL_CONFIDENCE_THRESHOLD`: Minimum confidence for SELL (default: 0.6)
- `MAX_POSITION_PCT`: Max % of portfolio per position (default: 0.2)

## Testing Strategy

1. **Unit Tests:**
   - Decision algorithm logic
   - Fee calculations
   - Balance validation

2. **Integration Tests:**
   - Endpoint calls (mocked)
   - Claude API integration
   - Full decision flow

3. **Edge Cases:**
   - Insufficient balance
   - Zero shares in portfolio
   - API failures
   - Invalid data
