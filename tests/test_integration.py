import numpy as np
import pandas as pd

from venantvr.indicators.candlestick import CandlestickIndicator
from venantvr.indicators.drop import SuddenPriceDropIndicator
from venantvr.indicators.passthrough import PassThroughIndicator
from venantvr.indicators.rsi import RSIIndicator
from venantvr.indicators.vix import VIXIndicator


class TestIndicatorIntegration:
    """Integration tests for multiple indicators working together"""

    def test_all_indicators_with_sample_data(self, sample_candles):
        """Test that all indicators can process the same data without errors"""
        indicators = [
            RSIIndicator(period=5),
            CandlestickIndicator(lookback_period=3),
            SuddenPriceDropIndicator(lookback_period=5),
            VIXIndicator(period=5),
            PassThroughIndicator(enabled=True),
        ]

        for indicator in indicators:
            # Should not raise any exceptions
            result = indicator.calculate(sample_candles)
            assert result is True

            # Should be able to check conditions
            buy_condition = indicator.check_buy_condition()
            sell_condition = indicator.check_sell_condition()

            assert isinstance(buy_condition, bool)
            assert isinstance(sell_condition, bool)

    def test_indicator_combination_strategy(self):
        """Test a simple combination strategy using multiple indicators"""
        # Create trending upward data with high volume
        data = {
            "open": [
                100,
                102,
                104,
                106,
                108,
                110,
                112,
                114,
                116,
                118,
                120,
                122,
                124,
                126,
                128,
            ],
            "close": [
                101,
                103,
                105,
                107,
                109,
                111,
                113,
                115,
                117,
                119,
                121,
                123,
                125,
                127,
                129,
            ],
            "volume": [
                1000,
                1100,
                1200,
                1300,
                1400,
                1500,
                1600,
                1700,
                1800,
                1900,
                2000,
                3000,
                2200,
                2300,
                2400,
            ],
        }
        candles = pd.DataFrame(data)

        # Initialize indicators
        rsi = RSIIndicator(period=10, buy_threshold=40, sell_threshold=80)
        candlestick = CandlestickIndicator(lookback_period=3, volume_threshold=1.2)
        drop_detector = SuddenPriceDropIndicator(drop_percentage=5, lookback_period=5)

        # Calculate all indicators
        rsi.calculate(candles)
        candlestick.calculate(candles)
        drop_detector.calculate(candles)

        # Check conditions
        rsi_buy = rsi.check_buy_condition()
        rsi_sell = rsi.check_sell_condition()
        candlestick_buy = candlestick.check_buy_condition()
        candlestick_sell = candlestick.check_sell_condition()
        drop_buy = drop_detector.check_buy_condition()
        drop_sell = drop_detector.check_sell_condition()

        # Simple combination logic: buy if majority agrees
        buy_signals = sum([rsi_buy, candlestick_buy, drop_buy])
        sell_signals = sum([rsi_sell, candlestick_sell, drop_sell])

        # With uptrending data, should have more buy signals
        assert buy_signals >= sell_signals

    def test_indicator_disagreement_scenario(self):
        """Test scenario where indicators disagree"""
        # Create mixed signal data: trending up but with a recent drop
        data = {
            "open": [
                100,
                102,
                104,
                106,
                108,
                110,
                112,
                114,
                116,
                118,
                120,
                118,
                115,
                112,
                110,
            ],
            "close": [
                101,
                103,
                105,
                107,
                109,
                111,
                113,
                115,
                117,
                119,
                121,
                117,
                113,
                110,
                108,
            ],
            "volume": [
                1000,
                1100,
                1200,
                1300,
                1400,
                1500,
                1600,
                1700,
                1800,
                1900,
                2000,
                3500,
                2200,
                2300,
                2400,
            ],
        }
        candles = pd.DataFrame(data)

        rsi = RSIIndicator(period=10)
        candlestick = CandlestickIndicator(lookback_period=3)
        drop_detector = SuddenPriceDropIndicator(drop_percentage=8, lookback_period=5)

        rsi.calculate(candles)
        candlestick.calculate(candles)
        drop_detector.calculate(candles)

        # Should be able to get different signals from different indicators
        conditions = {
            "rsi_buy": rsi.check_buy_condition(),
            "rsi_sell": rsi.check_sell_condition(),
            "candlestick_buy": candlestick.check_buy_condition(),
            "candlestick_sell": candlestick.check_sell_condition(),
            "drop_buy": drop_detector.check_buy_condition(),
            "drop_sell": drop_detector.check_sell_condition(),
        }

        # All conditions should be boolean values
        for condition_name, condition_value in conditions.items():
            assert isinstance(
                condition_value, bool
            ), f"{condition_name} should be boolean"

    def test_disabled_indicators_in_strategy(self, sample_candles):
        """Test strategy with some disabled indicators"""
        indicators = [
            RSIIndicator(enabled=True),
            CandlestickIndicator(enabled=False),  # Disabled
            SuddenPriceDropIndicator(enabled=True),
            VIXIndicator(enabled=False),  # Disabled
            PassThroughIndicator(enabled=False),  # Disabled by default
        ]

        enabled_count = sum(1 for ind in indicators if ind.is_enabled)
        disabled_count = sum(1 for ind in indicators if not ind.is_enabled)

        assert enabled_count == 2
        assert disabled_count == 3

        for indicator in indicators:
            indicator.calculate(sample_candles)

            if indicator.is_enabled:
                # Enabled indicators should compute and potentially return various conditions
                buy_condition = indicator.check_buy_condition()
                sell_condition = indicator.check_sell_condition()
                assert isinstance(buy_condition, bool)
                assert isinstance(sell_condition, bool)
            else:
                # Disabled indicators should return False for conditions (except passthrough)
                if isinstance(indicator, PassThroughIndicator):
                    # PassThrough returns False when disabled
                    assert indicator.check_buy_condition() is False
                    assert indicator.check_sell_condition() is False
                else:
                    # Other indicators return False when disabled
                    assert indicator.check_buy_condition() is False
                    assert indicator.check_sell_condition() is False

    def test_error_handling_with_bad_data(self):
        """Test error handling when indicators receive problematic data"""
        # Create DataFrame with NaN values
        data = {
            "close": [100, 101, np.nan, 103, 104],
            "volume": [1000, np.nan, 1200, 1300, 1400],
        }
        candles = pd.DataFrame(data)

        indicators = [
            RSIIndicator(period=3),
            CandlestickIndicator(lookback_period=2),
            SuddenPriceDropIndicator(lookback_period=3),
            VIXIndicator(period=3),
        ]

        for indicator in indicators:
            # Should not crash with NaN values
            try:
                result = indicator.calculate(candles)
                # Some may return True (handled gracefully), others may have issues
                assert isinstance(result, bool)

                buy_condition = indicator.check_buy_condition()
                sell_condition = indicator.check_sell_condition()

                assert isinstance(buy_condition, bool)
                assert isinstance(sell_condition, bool)
            except Exception as e:
                # If an exception occurs, it should be a known type
                assert isinstance(e, (ValueError, KeyError, TypeError, AttributeError))

    def test_consistent_api_across_indicators(self, sample_candles):
        """Test that all indicators follow the same API consistently"""
        indicator_classes = [
            RSIIndicator,
            CandlestickIndicator,
            SuddenPriceDropIndicator,
            VIXIndicator,
            PassThroughIndicator,
        ]

        for indicator_class in indicator_classes:
            # Should be able to instantiate
            indicator = indicator_class()

            # Should have common interface
            assert hasattr(indicator, "calculate")
            assert hasattr(indicator, "check_buy_condition")
            assert hasattr(indicator, "check_sell_condition")
            assert hasattr(indicator, "is_enabled")

            # Should be able to call common methods
            result = indicator.calculate(sample_candles)
            assert isinstance(result, bool)

            buy_condition = indicator.check_buy_condition()
            sell_condition = indicator.check_sell_condition()

            assert isinstance(buy_condition, bool)
            assert isinstance(sell_condition, bool)

    def test_performance_with_large_dataset(self):
        """Test performance with larger dataset"""
        # Create larger dataset
        np.random.seed(42)
        size = 1000
        prices = 100 + np.cumsum(np.random.randn(size) * 0.01)
        volumes = np.random.randint(1000, 5000, size)

        data = {
            "open": prices
                    - np.random.randn(size) * 0.005,  # Open slightly different from close
            "close": prices,
            "volume": volumes,
        }
        candles = pd.DataFrame(data)

        indicators = [
            RSIIndicator(period=50),
            CandlestickIndicator(lookback_period=10),
            SuddenPriceDropIndicator(lookback_period=20),
            VIXIndicator(period=30),
        ]

        # Should complete in reasonable time
        import time

        start_time = time.time()

        for indicator in indicators:
            indicator.calculate(candles)
            indicator.check_buy_condition()
            indicator.check_sell_condition()

        end_time = time.time()
        execution_time = end_time - start_time

        # Should complete within 5 seconds (generous for CI environments)
        assert (
                execution_time < 5.0
        ), f"Execution took {execution_time:.2f} seconds, which is too long"
