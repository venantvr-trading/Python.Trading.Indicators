import pandas as pd

from python_trading_indicators.candlestick import CandlestickIndicator


# noinspection PyUnresolvedReferences
class TestCandlestickIndicator:
    """Test the Candlestick Pattern Indicator"""

    def test_candlestick_indicator_initialization(self):
        """Test candlestick indicator initialization with default parameters"""
        candlestick = CandlestickIndicator()

        assert candlestick.is_enabled is True
        assert candlestick._CandlestickIndicator__lookback_period == 3
        assert candlestick._CandlestickIndicator__volume_threshold == 1.5

    def test_candlestick_indicator_custom_parameters(self):
        """Test candlestick indicator initialization with custom parameters"""
        candlestick = CandlestickIndicator(
            lookback_period=5, volume_threshold=2.0, enabled=False
        )

        assert candlestick.is_enabled is False
        assert candlestick._CandlestickIndicator__lookback_period == 5
        assert candlestick._CandlestickIndicator__volume_threshold == 2.0

    def test_candlestick_insufficient_data(self, insufficient_candles):
        """Test candlestick calculation with insufficient data"""
        candlestick = CandlestickIndicator(lookback_period=5)
        candlestick.calculate(insufficient_candles)

        assert candlestick.check_buy_condition() is False
        assert candlestick.check_sell_condition() is False

    def test_candlestick_bullish_pattern_with_volume(self):
        """Test bullish candlestick pattern with high volume"""
        data = {
            "open": [100, 101, 102],
            "close": [101, 102, 103],  # All bullish candles
            "volume": [1000, 1000, 2500],  # High volume on last candle
        }
        candles = pd.DataFrame(data)

        candlestick = CandlestickIndicator(lookback_period=3, volume_threshold=2.0)
        candlestick.calculate(candles)

        assert candlestick.check_buy_condition() is True
        assert candlestick.check_sell_condition() is False

    def test_candlestick_bearish_pattern_with_volume(self):
        """Test bearish candlestick pattern with high volume"""
        data = {
            "open": [103, 102, 101],
            "close": [102, 101, 100],  # All bearish candles
            "volume": [1000, 1000, 2500],  # High volume on last candle
        }
        candles = pd.DataFrame(data)

        candlestick = CandlestickIndicator(lookback_period=3, volume_threshold=2.0)
        candlestick.calculate(candles)

        assert candlestick.check_buy_condition() is False
        assert candlestick.check_sell_condition() is True

    def test_candlestick_bullish_pattern_without_volume(self):
        """Test bullish pattern without volume confirmation"""
        data = {
            "open": [100, 101, 102],
            "close": [101, 102, 103],  # All bullish candles
            "volume": [1000, 1000, 1000],  # No volume spike
        }
        candles = pd.DataFrame(data)

        candlestick = CandlestickIndicator(lookback_period=3, volume_threshold=1.5)
        candlestick.calculate(candles)

        # Should not trigger buy condition without volume confirmation
        assert candlestick.check_buy_condition() is False
        assert candlestick.check_sell_condition() is False

    def test_candlestick_mixed_pattern(self):
        """Test mixed bullish/bearish pattern"""
        data = {
            "open": [100, 102, 101],
            "close": [101, 101, 102],  # Mixed: bullish, bearish, bullish
            "volume": [1000, 1000, 2000],
        }
        candles = pd.DataFrame(data)

        candlestick = CandlestickIndicator(lookback_period=3, volume_threshold=1.5)
        candlestick.calculate(candles)

        # Bullish should win (2 vs 1), with volume confirmation
        assert candlestick.check_buy_condition() is True
        assert candlestick.check_sell_condition() is False

    def test_candlestick_equal_pattern(self):
        """Test equal bullish/bearish pattern"""
        data = {
            "open": [100, 102],
            "close": [101, 101],  # One bullish, one bearish
            "volume": [1000, 2000],
        }
        candles = pd.DataFrame(data)

        candlestick = CandlestickIndicator(lookback_period=2, volume_threshold=1.5)
        candlestick.calculate(candles)

        # Equal counts should not trigger either condition
        assert candlestick.check_buy_condition() is False
        assert candlestick.check_sell_condition() is False

    def test_candlestick_disabled_indicator(self):
        """Test candlestick indicator when disabled"""
        data = {
            "open": [100, 101, 102],
            "close": [101, 102, 103],
            "volume": [1000, 1000, 2500],
        }
        candles = pd.DataFrame(data)

        candlestick = CandlestickIndicator(enabled=False)
        candlestick.calculate(candles)

        assert candlestick.check_buy_condition() is False
        assert candlestick.check_sell_condition() is False

    def test_candlestick_zero_average_volume(self):
        """Test candlestick calculation with zero average volume"""
        data = {
            "open": [100, 101, 102],
            "close": [101, 102, 103],
            "volume": [0, 0, 1000],  # Zero volume in earlier candles
        }
        candles = pd.DataFrame(data)

        candlestick = CandlestickIndicator(lookback_period=3)
        candlestick.calculate(candles)

        # Should handle zero average volume gracefully
        assert candlestick.check_buy_condition() is False
        assert candlestick.check_sell_condition() is False

    def test_candlestick_single_candle_lookback(self):
        """Test candlestick with single candle lookback"""
        data = {
            "open": [100, 101, 102],
            "close": [101, 102, 103],
            "volume": [1000, 1000, 2500],
        }
        candles = pd.DataFrame(data)

        candlestick = CandlestickIndicator(lookback_period=1, volume_threshold=2.0)
        candlestick.calculate(candles)

        # Should work with single candle lookback
        assert candlestick.check_buy_condition() is True

    def test_candlestick_doji_pattern(self):
        """Test candlestick with doji patterns (open == close)"""
        data = {
            "open": [100, 101, 102],
            "close": [100, 101, 102],  # All doji candles
            "volume": [1000, 1000, 2000],
        }
        candles = pd.DataFrame(data)

        candlestick = CandlestickIndicator(lookback_period=3, volume_threshold=1.5)
        candlestick.calculate(candles)

        # Doji candles should not trigger buy/sell conditions
        assert candlestick.check_buy_condition() is False
        assert candlestick.check_sell_condition() is False
