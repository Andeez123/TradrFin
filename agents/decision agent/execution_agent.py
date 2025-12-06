# execution_agent.py
import math
from typing import Dict, Any

def execute_buy(symbol: str, price: float, budget: float, fee: float,
                portfolio: Dict[str, Any], investment_balance: float) -> Dict[str, Any]:
    """
    Execute a BUY order using investment_balance.
    Deducts the total cost (shares + fee) from investment_balance.
    """
    available = budget - fee
    shares = math.floor(available / price)
    if shares <= 0 or available <= 0:
        return {"status":"failed","reason":"Budget too low"}

    total_cost = shares * price + fee
    if total_cost > investment_balance:
        return {"status":"failed","reason":"Not enough investment balance"}

    if symbol in portfolio:
        prev = portfolio[symbol]
        new_shares = prev["shares"] + shares
        avg_cost = (prev["shares"]*prev["avg_cost"] + shares*price) / new_shares
        portfolio[symbol] = {"shares": new_shares, "avg_cost": avg_cost}
    else:
        portfolio[symbol] = {"shares": shares, "avg_cost": price}

    investment_balance -= total_cost
    return {
        "status":"ok",
        "action":"BUY",
        "symbol":symbol,
        "shares":shares,
        "price":price,
        "fee":fee,
        "total_cost":total_cost,
        "investment_balance_remaining":investment_balance
    }

def execute_sell(symbol: str, price: float, fee: float,
                 portfolio: Dict[str, Any], investment_balance: float) -> Dict[str, Any]:
    """
    Execute a SELL order using investment_balance.
    Adds the net revenue (after fee) back to investment_balance.
    """
    if symbol not in portfolio or portfolio[symbol]["shares"] <= 0:
        return {"status":"failed","reason":"No position to sell"}

    shares = portfolio[symbol]["shares"]
    revenue = shares * price - fee
    investment_balance += revenue
    del portfolio[symbol]
    return {
        "status":"ok",
        "action":"SELL",
        "symbol":symbol,
        "shares":shares,
        "price":price,
        "fee":fee,
        "revenue":revenue,
        "investment_balance_after":investment_balance
    }
