"""
Python Trading Indicators

A comprehensive library of technical analysis indicators for algorithmic trading.

Available Indicators:
- RSIIndicator: Relative Strength Index for overbought/oversold conditions
- CandlestickIndicator: Candlestick pattern analysis with volume confirmation
- SuddenPriceDropIndicator: Detects significant price drops
- VIXIndicator: Volatility index for panic detection
- PassThroughIndicator: Utility indicator for testing

Example Usage:
    >>> import pandas as pd
    >>> from venantvr.indicators.rsi import RSIIndicator
    >>> 
    >>> # Sample data
    >>> data = {'close': [100, 102, 105, 103, 108]}
    >>> candles = pd.DataFrame(data)
    >>> 
    >>> # Create and use RSI indicator
    >>> rsi = RSIIndicator(period=14, buy_threshold=30, sell_threshold=70)
    >>> rsi.calculate(candles)
    >>> 
    >>> if rsi.check_buy_condition():
    >>>     print("Buy signal detected!")
"""

from .indicator import Indicator
from .rsi import RSIIndicator
from .candlestick import CandlestickIndicator
from .drop import SuddenPriceDropIndicator
from .vix import VIXIndicator
from .passthrough import PassThroughIndicator

__version__ = "0.1.0"

__all__ = [
    "Indicator",
    "RSIIndicator", 
    "CandlestickIndicator",
    "SuddenPriceDropIndicator",
    "VIXIndicator",
    "PassThroughIndicator",
]