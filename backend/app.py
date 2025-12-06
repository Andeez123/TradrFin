"""
Backend FastAPI Application
Provides REST API endpoints to run trading simulations via the decision agent.
"""
import sys
import os
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
import asyncio
from datetime import datetime
import pandas as pd

# Add decision agent to path
decision_agent_path = os.path.join(os.path.dirname(__file__), "..", "agents", "decision agent")
sys.path.insert(0, decision_agent_path)

from trading_simulator import run_simulation

app = FastAPI(
    title="Trading Simulation Backend API",
    description="API to run and monitor autonomous trading simulations",
    version="1.0.0"
)

# Global state for simulation
simulation_state = {
    "portfolio": {},
    "investment_balance": 5000.0,
    "day_index": 0
}

# Track simulation results
simulation_results = {
    "last_run": None,
    "is_running": False
}


class SimulationConfig(BaseModel):
    """Configuration for running a trading simulation"""
    initial_balance: Optional[float] = 5000.0
    candidate_symbols: Optional[List[str]] = ["AAPL", "TSLA", "GOOG", "AMZN", "MSFT"]
    trade_budget: Optional[float] = 1000.0
    trade_fee: Optional[float] = 5.0
    top_n: Optional[int] = 2
    decision_mode: Optional[str] = "rule"  # "rule" | "llm" | "mock"
    interval_seconds: Optional[int] = 2


class SimulationResponse(BaseModel):
    """Response from simulation endpoint"""
    status: str
    message: str
    csv_filename: Optional[str] = None
    final_balance: Optional[float] = None
    final_portfolio: Optional[dict] = None
    days_simulated: Optional[int] = None


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Trading Simulation Backend API",
        "version": "1.0.0",
        "endpoints": {
            "POST /demo": "Run a trading simulation",
            "GET /portfolio": "Get current portfolio state",
            "GET /logs": "List available trading log files",
            "GET /logs/{filename}": "Download a specific log file",
            "GET /status": "Get simulation status"
        }
    }


@app.post("/demo", response_model=SimulationResponse)
async def run_demo_simulation(config: Optional[SimulationConfig] = None):
    """
    Run a trading simulation with the decision agent.
    
    This endpoint runs the autonomous trading simulation and returns the results.
    The simulation will process all available days of precomputed market data.
    """
    global simulation_state, simulation_results
    
    # Check if simulation is already running
    if simulation_results["is_running"]:
        raise HTTPException(
            status_code=409,
            detail="Simulation is already running. Please wait for it to complete."
        )
    
    # Use default config if none provided
    if config is None:
        config = SimulationConfig()
    
    # Reset simulation state
    simulation_state = {
        "portfolio": {},
        "investment_balance": config.initial_balance,
        "day_index": 0
    }
    
    # Prepare config dict
    config_dict = {
        "candidate_symbols": config.candidate_symbols,
        "trade_budget": config.trade_budget,
        "trade_fee": config.trade_fee,
        "top_n": config.top_n,
        "decision_mode": config.decision_mode,
        "interval_seconds": config.interval_seconds
    }
    
    # Mark simulation as running
    simulation_results["is_running"] = True
    
    try:
        # Run the simulation
        result = await run_simulation(simulation_state, config_dict)
        
        # Store results
        simulation_results["last_run"] = {
            **result,
            "timestamp": datetime.now().isoformat()
        }
        
        return SimulationResponse(**result)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Simulation failed: {str(e)}"
        )
    finally:
        # Mark simulation as complete
        simulation_results["is_running"] = False


@app.get("/portfolio")
async def get_portfolio():
    """Get the current portfolio state"""
    return {
        "portfolio": simulation_state["portfolio"],
        "investment_balance": simulation_state["investment_balance"],
        "day_index": simulation_state["day_index"]
    }


@app.get("/status")
async def get_status():
    """Get the current simulation status"""
    return {
        "is_running": simulation_results["is_running"],
        "last_run": simulation_results["last_run"],
        "current_state": {
            "portfolio": simulation_state["portfolio"],
            "investment_balance": simulation_state["investment_balance"],
            "day_index": simulation_state["day_index"]
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
