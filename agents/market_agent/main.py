#!/usr/bin/env python3
"""
Market Data Agent - Apify Actor Entry Point

This script serves as the main entry point for the Market Data Agent,
which can run both as an Apify Actor and as a standalone Python application.
"""

import json
import logging
import os
import sys
from typing import Dict, Any, Optional

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Add the market_agent package to the path
sys.path.insert(0, os.path.dirname(__file__))

from market_agent.types.market_types import MarketRequest, MarketResponse, ApifyMarketRequest
from market_agent.services.market_service import MarketService, MarketServiceError
from market_agent.services.analysis_service import AnalysisService, AnalysisServiceError
from market_agent.services.cursor_summary import SummaryService, SummaryServiceError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """
    Main entry point for the Market Data Agent.

    Supports both Apify Actor execution and local execution.
    """
    try:
        # Check if running on Apify
        is_apify = os.getenv('APIFY_IS_AT_HOME', 'false').lower() == 'true'

        if is_apify:
            # Running as Apify Actor
            return run_as_apify_actor()
        else:
            # Running locally
            return run_locally()

    except Exception as e:
        logger.error(f"Application failed: {str(e)}")
        return {"error": str(e), "success": False}


def run_as_apify_actor():
    """
    Run as an Apify Actor.

    Returns:
        Dict containing the result to be stored by Apify
    """
    try:
        from apify import Actor

        # Initialize Apify Actor
        async def main_async():
            async with Actor:
                # Get input from Apify
                actor_input = await Actor.get_input() or {}

                logger.info(f"Received Apify input: {actor_input}")

                # Process the request
                result = process_market_request(actor_input)

                # Push result to Apify dataset
                await Actor.push_data(result)

                logger.info("Successfully processed market data request")
                return result

        # Run the async main function
        import asyncio
        return asyncio.run(main_async())

    except ImportError:
        logger.error("Apify SDK not available. Please install apify package.")
        return {"error": "Apify SDK not available", "success": False}
    except Exception as e:
        logger.error(f"Apify Actor execution failed: {str(e)}")
        return {"error": str(e), "success": False}


def run_locally():
    """
    Run locally for testing and development.

    Reads input from input.json file or INPUT_FILE environment variable.
    """
    try:
        # Check for custom input file from environment variable (used by web interface)
        input_file = os.getenv('INPUT_FILE', 'input.json')

        if not os.path.exists(input_file):
            error_msg = f"Input file '{input_file}' not found. Please create input.json with your request data."
            logger.error(error_msg)
            result = {"error": error_msg, "success": False}
            print(json.dumps(result, indent=2))
            return result

        with open(input_file, 'r') as f:
            input_data = json.load(f)

        logger.info(f"Processing local request from {input_file}: {input_data}")

        # Process the request
        result = process_market_request(input_data)

        # Output result as JSON (only for console output, not when called from web interface)
        if not os.getenv('INPUT_FILE'):
            print(json.dumps(result, indent=2, default=str))
        else:
            # When called from web interface, output only the JSON result
            print(json.dumps(result, default=str))
        logger.info("Successfully processed market data request")
        return result

    except json.JSONDecodeError as e:
        error_msg = f"Invalid JSON in input.json: {str(e)}"
        logger.error(error_msg)
        result = {"error": error_msg, "success": False}
        print(json.dumps(result, indent=2))
        return result
    except Exception as e:
        error_msg = f"Local execution failed: {str(e)}"
        logger.error(error_msg)
        result = {"error": error_msg, "success": False}
        print(json.dumps(result, indent=2))
        return result


def process_market_request(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process a market data request (supports both legacy and Apify formats).

    Args:
        input_data: Dictionary containing request parameters

    Returns:
        Dictionary containing the analysis results
    """
    try:
        # Process market request (now supports fetching data from Yahoo Finance)
        return process_market_request(input_data)

    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg, "success": False}


def process_market_request(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process market data request - fetch data from Yahoo Finance and analyze.

    Args:
        input_data: Market request with symbol, data_type, interval, range

    Returns:
        Dictionary containing the analysis results
    """
    try:
        # Validate and parse input
        market_request = MarketRequest(**input_data)

        # Initialize services
        market_service = MarketService()
        analysis_service = AnalysisService()
        summary_service = SummaryService()

        # Check if processing single symbol or multiple symbols
        symbols_to_process = []
        if market_request.symbols:
            symbols_to_process = market_request.symbols
            logger.info(f"Processing {len(symbols_to_process)} symbols: {symbols_to_process}")
        elif market_request.symbol:
            symbols_to_process = [market_request.symbol]
            logger.info(f"Processing single symbol: {market_request.symbol}")

        results = []

        # Process each symbol
        for symbol in symbols_to_process:
            logger.info(f"Processing {symbol} ({market_request.data_type})")

            # Create individual request for this symbol
            symbol_request = MarketRequest(
                symbol=symbol,
                data_type=market_request.data_type,
                interval=market_request.interval,
                range=market_request.range
            )

            try:
                # Step 1: Fetch market data from Yahoo Finance
                logger.info(f"Fetching market data for {symbol}")
                market_data = market_service.fetch_market_data(symbol_request)

                # Step 2: Compute technical indicators only
                logger.info(f"Computing technical indicators for {symbol}")
                analysis = analysis_service.analyze_market_data(market_data)

                # Step 3: Generate comprehensive LLM analysis (structured insights + summary)
                logger.info(f"Generating LLM analysis for {symbol}")
                summary, llm_analysis = summary_service.generate_analysis(analysis)

                # Step 4: Prepare response for this symbol
                response = MarketResponse(
                    symbol=analysis.symbol,
                    price=analysis.price,
                    indicators={
                        'sma20': analysis.indicators.sma20,
                        'sma50': analysis.indicators.sma50,
                        'ema20': analysis.indicators.ema20,
                        'ema50': analysis.indicators.ema50,
                        'rsi': analysis.indicators.rsi,
                        'macd': analysis.indicators.macd,
                        'bollinger': analysis.indicators.bollinger,
                        'volatility': analysis.indicators.volatility,
                        'momentum': analysis.indicators.momentum,
                        'volume_avg': analysis.indicators.volume_avg,
                        'volume_spike_ratio': analysis.indicators.volume_spike_ratio
                    },
                    summary=summary,
                    llm_analysis=llm_analysis
                )

                # Convert to dictionary for JSON serialization
                result = response.model_dump()
                result['success'] = True

                results.append(result)
                logger.info(f"Successfully analyzed {symbol}")

            except Exception as e:
                logger.error(f"Failed to analyze {symbol}: {str(e)}")
                # Add error result for this symbol
                error_result = {
                    "symbol": symbol,
                    "success": False,
                    "error": str(e)
                }
                results.append(error_result)

        # Return single result for single symbol, array for multiple symbols
        if len(results) == 1:
            return results[0]
        else:
            return {"results": results, "total_symbols": len(symbols_to_process), "success": True}

    except (MarketServiceError, AnalysisServiceError, SummaryServiceError) as e:
        error_msg = f"Service error: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg, "success": False}


def process_legacy_request(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process legacy market data request (backward compatibility).

    Args:
        input_data: Legacy format with symbol, data_type, etc.

    Returns:
        Dictionary containing the analysis results
    """
    try:
        # Validate and parse input
        market_request = MarketRequest(**input_data)
        logger.info(f"Processing legacy request for {market_request.symbol}")

        # Initialize services
        market_service = MarketService()
        analysis_service = AnalysisService()
        summary_service = SummaryService()

        # Step 1: Fetch market data
        logger.info(f"Fetching {market_request.data_type} data for {market_request.symbol}")
        market_data = market_service.fetch_market_data(market_request)

        # Step 2: Compute technical indicators
        logger.info("Computing technical indicators")
        analysis = analysis_service.analyze_market_data(market_data)

        # Step 3: Generate comprehensive LLM analysis
        logger.info("Generating LLM analysis with structured insights and human-readable summary")
        summary, llm_analysis = summary_service.generate_analysis(analysis)

        # Step 4: Prepare response
        response = MarketResponse(
            symbol=analysis.symbol,
            price=analysis.price,
            indicators={
                'sma20': analysis.indicators.sma20,
                'sma50': analysis.indicators.sma50,
                'ema20': analysis.indicators.ema20,
                'ema50': analysis.indicators.ema50,
                'rsi': analysis.indicators.rsi,
                'macd': analysis.indicators.macd,
                'bollinger': analysis.indicators.bollinger,
                'volatility': analysis.indicators.volatility,
                'momentum': analysis.indicators.momentum,
                'volume_avg': analysis.indicators.volume_avg,
                'volume_spike_ratio': analysis.indicators.volume_spike_ratio
            },
            summary=summary,
            llm_analysis=llm_analysis
        )

        # Convert to dictionary for JSON serialization
        result = response.model_dump()
        result['success'] = True

        logger.info(f"Successfully analyzed {market_request.symbol} (legacy format)")
        return result

    except (MarketServiceError, AnalysisServiceError, SummaryServiceError) as e:
        error_msg = f"Service error: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg, "success": False}


if __name__ == "__main__":
    main()
