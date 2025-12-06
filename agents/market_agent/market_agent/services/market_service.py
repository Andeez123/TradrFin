"""Market data service for fetching data from Yahoo Finance."""

import logging
from typing import Optional
import pandas as pd
import yfinance as yf
from ..types.market_types import (
    MarketRequest,
    MarketData,
    OHLCVData,
    DataType,
    Interval,
    TimeRange,
    ApifyMarketRequest,
    ApifyOHLCVData
)

logger = logging.getLogger(__name__)


class MarketServiceError(Exception):
    """Custom exception for market service errors."""
    pass


class MarketService:
    """Service for fetching market data from Yahoo Finance."""

    def __init__(self):
        """Initialize the market service."""
        self.logger = logging.getLogger(__name__)

    def fetch_market_data(self, request: MarketRequest) -> MarketData:
        """
        Fetch market data based on the request.

        Args:
            request: MarketRequest containing symbol, data_type, interval, and range

        Returns:
            MarketData object with OHLCV data

        Raises:
            MarketServiceError: If data fetching fails
        """
        try:
            if request.data_type == DataType.QUOTE:
                return self._fetch_quote_data(request.symbol)
            elif request.data_type == DataType.HISTORICAL:
                if not request.interval or not request.range:
                    raise MarketServiceError(
                        "Interval and range are required for historical data"
                    )
                return self._fetch_historical_data(
                    request.symbol,
                    request.interval,
                    request.range
                )
            else:
                raise MarketServiceError(f"Unsupported data type: {request.data_type}")

        except Exception as e:
            self.logger.error(f"Failed to fetch market data for {request.symbol}: {str(e)}")
            raise MarketServiceError(f"Failed to fetch data: {str(e)}") from e

    def process_apify_data(self, apify_request: ApifyMarketRequest) -> MarketData:
        """
        Process OHLCV data provided by Apify.

        Args:
            apify_request: ApifyMarketRequest with symbol and historical data

        Returns:
            MarketData object with processed OHLCV data

        Raises:
            MarketServiceError: If data processing fails
        """
        try:
            if not apify_request.historical:
                raise MarketServiceError("No historical data provided in Apify request")

            # Convert ApifyOHLCVData to OHLCVData format
            ohlcv_data = []
            current_price = None

            for item in apify_request.historical:
                ohlcv_data.append(OHLCVData(
                    timestamp=item.timestamp,
                    open=item.open,
                    high=item.high,
                    low=item.low,
                    close=item.close,
                    volume=item.volume,
                    adj_close=item.adj_close or item.close
                ))
                # Set current price as the latest close
                current_price = item.close

            if current_price is None:
                raise MarketServiceError("Could not determine current price from Apify data")

            return MarketData(
                symbol=apify_request.symbol,
                data=ohlcv_data,
                current_price=current_price
            )

        except Exception as e:
            self.logger.error(f"Failed to process Apify data for {apify_request.symbol}: {str(e)}")
            raise MarketServiceError(f"Failed to process Apify data: {str(e)}") from e

    def _fetch_quote_data(self, symbol: str) -> MarketData:
        """
        Fetch current quote data for a symbol.

        Args:
            symbol: Stock/crypto symbol

        Returns:
            MarketData with current price
        """
        try:
            ticker = yf.Ticker(symbol)

            # Get current price
            current_price = ticker.info.get('currentPrice')
            if current_price is None:
                # Try alternative methods
                history = ticker.history(period="1d")
                if not history.empty:
                    current_price = history['Close'].iloc[-1]

            if current_price is None:
                raise MarketServiceError(f"Could not retrieve current price for {symbol}")

            # Get recent OHLCV data (last 5 days for context)
            history = ticker.history(period="5d", interval="1d")
            if history.empty:
                raise MarketServiceError(f"No historical data available for {symbol}")

            # Convert to OHLCV format
            ohlcv_data = []
            for timestamp, row in history.iterrows():
                ohlcv_data.append(OHLCVData(
                    timestamp=timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    open=float(row['Open']),
                    high=float(row['High']),
                    low=float(row['Low']),
                    close=float(row['Close']),
                    volume=float(row['Volume']),
                    adj_close=float(row['Close'])  # Using Close as Adj Close for simplicity
                ))

            return MarketData(
                symbol=symbol,
                data=ohlcv_data,
                current_price=float(current_price)
            )

        except Exception as e:
            self.logger.error(f"Failed to fetch quote data for {symbol}: {str(e)}")
            raise MarketServiceError(f"Failed to fetch quote data: {str(e)}") from e

    def _fetch_historical_data(
        self,
        symbol: str,
        interval: Interval,
        time_range: TimeRange
    ) -> MarketData:
        """
        Fetch historical data for a symbol.

        Args:
            symbol: Stock/crypto symbol
            interval: Time interval
            time_range: Time range

        Returns:
            MarketData with historical OHLCV data
        """
        try:
            ticker = yf.Ticker(symbol)

            # Map interval and period to yfinance format
            period_map = {
                TimeRange.ONE_MONTH: "1mo",
                TimeRange.THREE_MONTHS: "3mo",
                TimeRange.SIX_MONTHS: "6mo",
                TimeRange.ONE_YEAR: "1y"
            }

            interval_map = {
                Interval.FIVE_MIN: "5m",
                Interval.ONE_HOUR: "1h",
                Interval.ONE_DAY: "1d"
            }

            period = period_map.get(time_range)
            yf_interval = interval_map.get(interval)

            if not period or not yf_interval:
                raise MarketServiceError(f"Invalid interval/range combination: {interval}/{time_range}")

            # Fetch historical data
            history = ticker.history(period=period, interval=yf_interval)

            if history.empty:
                raise MarketServiceError(f"No historical data available for {symbol} with {period}/{yf_interval}")

            # Convert to OHLCV format
            ohlcv_data = []
            current_price = None

            for timestamp, row in history.iterrows():
                ohlcv_data.append(OHLCVData(
                    timestamp=timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    open=float(row['Open']),
                    high=float(row['High']),
                    low=float(row['Low']),
                    close=float(row['Close']),
                    volume=float(row['Volume']),
                    adj_close=float(row.get('Adj Close', row['Close']))
                ))
                # Set current price as the latest close
                current_price = float(row['Close'])

            if current_price is None:
                current_price = float(history['Close'].iloc[-1])

            return MarketData(
                symbol=symbol,
                data=ohlcv_data,
                current_price=current_price
            )

        except Exception as e:
            self.logger.error(f"Failed to fetch historical data for {symbol}: {str(e)}")
            raise MarketServiceError(f"Failed to fetch historical data: {str(e)}") from e
