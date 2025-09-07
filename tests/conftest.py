import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def sample_candles():
    """Sample candlestick data for testing"""
    data = {
        "open": [100, 101, 102, 103, 104, 105, 104, 103, 102, 101, 100],
        "high": [102, 103, 104, 105, 106, 107, 106, 105, 104, 103, 102],
        "low": [99, 100, 101, 102, 103, 104, 103, 102, 101, 100, 99],
        "close": [101, 102, 103, 104, 105, 104, 103, 102, 101, 100, 99],
        "volume": [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000],
    }
    return pd.DataFrame(data)


@pytest.fixture
def trending_up_candles():
    """Uptrend candlestick data"""
    data = {
        "open": [100, 102, 104, 106, 108, 110, 112, 114, 116, 118],
        "high": [102, 104, 106, 108, 110, 112, 114, 116, 118, 120],
        "low": [99, 101, 103, 105, 107, 109, 111, 113, 115, 117],
        "close": [101, 103, 105, 107, 109, 111, 113, 115, 117, 119],
        "volume": [1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800],
    }
    return pd.DataFrame(data)


@pytest.fixture
def trending_down_candles():
    """Downtrend candlestick data"""
    data = {
        "open": [120, 118, 116, 114, 112, 110, 108, 106, 104, 102],
        "high": [121, 119, 117, 115, 113, 111, 109, 107, 105, 103],
        "low": [118, 116, 114, 112, 110, 108, 106, 104, 102, 100],
        "close": [119, 117, 115, 113, 111, 109, 107, 105, 103, 101],
        "volume": [2000, 2200, 2400, 2600, 2800, 3000, 3200, 3400, 3600, 3800],
    }
    return pd.DataFrame(data)


@pytest.fixture
def high_volume_candles():
    """Candlestick data with high volume spikes"""
    data = {
        "open": [100, 101, 102, 103, 104],
        "high": [102, 103, 104, 105, 106],
        "low": [99, 100, 101, 102, 103],
        "close": [101, 102, 103, 104, 105],
        "volume": [1000, 1000, 1000, 5000, 1000],  # Volume spike in 4th candle
    }
    return pd.DataFrame(data)


@pytest.fixture
def insufficient_candles():
    """Insufficient data for calculations"""
    data = {
        "open": [100, 101],
        "high": [102, 103],
        "low": [99, 100],
        "close": [101, 102],
        "volume": [1000, 1100],
    }
    return pd.DataFrame(data)


@pytest.fixture
def volatile_candles():
    """High volatility candlestick data"""
    np.random.seed(42)  # For reproducible tests
    prices = 100 + np.cumsum(
        np.random.randn(50) * 2
    )  # Random walk with higher volatility
    volumes = np.random.randint(1000, 5000, 50)

    data = {
        "open": prices[:-1],
        "high": prices[:-1] + np.abs(np.random.randn(49) * 3),
        "low": prices[:-1] - np.abs(np.random.randn(49) * 3),
        "close": prices[1:],
        "volume": volumes[:-1],
    }
    return pd.DataFrame(data)
