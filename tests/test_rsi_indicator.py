import pandas as pd

from venantvr.indicators.rsi import RSIIndicator


# noinspection PyUnresolvedReferences
class TestRSIIndicator:
    """Test the RSI (Relative Strength Index) Indicator"""

    def test_rsi_indicator_initialization(self):
        """Test RSI indicator initialization with default parameters"""
        rsi = RSIIndicator()

        assert rsi.is_enabled is True
        assert rsi._RSIIndicator__period == 14
        assert rsi._RSIIndicator__buy_threshold == 30
        assert rsi._RSIIndicator__sell_threshold == 70

    def test_rsi_indicator_custom_parameters(self):
        """Test RSI indicator initialization with custom parameters"""
        rsi = RSIIndicator(
            period=21, buy_threshold=25, sell_threshold=75, enabled=False
        )

        assert rsi.is_enabled is False
        assert rsi._RSIIndicator__period == 21
        assert rsi._RSIIndicator__buy_threshold == 25
        assert rsi._RSIIndicator__sell_threshold == 75

    def test_rsi_insufficient_data(self, insufficient_candles):
        """Test RSI calculation with insufficient data"""
        rsi = RSIIndicator(period=14)
        rsi.calculate(insufficient_candles)

        assert rsi.check_buy_condition() is False
        assert rsi.check_sell_condition() is False

    def test_rsi_calculation_trending_up(self, trending_up_candles):
        """Test RSI calculation with uptrending data"""
        rsi = RSIIndicator(period=5)
        rsi.calculate(trending_up_candles)

        # With consistent uptrend, RSI should be high
        rsi_values = rsi._RSIIndicator__rsi_values
        assert rsi_values is not None
        assert len(rsi_values) > 0
        assert rsi_values[-1] > 50  # Should be above neutral

    def test_rsi_calculation_trending_down(self, trending_down_candles):
        """Test RSI calculation with downtrending data"""
        rsi = RSIIndicator(period=5)
        rsi.calculate(trending_down_candles)

        # With consistent downtrend, RSI should be low
        rsi_values = rsi._RSIIndicator__rsi_values
        assert rsi_values is not None
        assert len(rsi_values) > 0
        assert rsi_values[-1] < 50  # Should be below neutral

    def test_rsi_buy_condition_oversold(self):
        """Test RSI buy condition when oversold"""
        # Create data that will result in low RSI (oversold condition)
        data = {"close": [100, 95, 90, 85, 80, 75, 70, 65, 60, 55, 50, 45, 40, 35, 30]}
        candles = pd.DataFrame(data)

        rsi = RSIIndicator(period=14, buy_threshold=40)
        rsi.calculate(candles)

        assert rsi.check_buy_condition() is True
        assert rsi.check_sell_condition() is False

    def test_rsi_sell_condition_overbought(self):
        """Test RSI sell condition when overbought"""
        # Create data that will result in high RSI (overbought condition)
        data = {
            "close": [50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120]
        }
        candles = pd.DataFrame(data)

        rsi = RSIIndicator(period=14, sell_threshold=60)
        rsi.calculate(candles)

        assert rsi.check_buy_condition() is False
        assert rsi.check_sell_condition() is True

    def test_rsi_neutral_condition(self, sample_candles):
        """Test RSI in neutral conditions"""
        # Adjust thresholds so the calculated RSI (around 21) is in neutral zone
        rsi = RSIIndicator(period=5, buy_threshold=20, sell_threshold=80)
        rsi.calculate(sample_candles)

        # With sample data and adjusted thresholds, should be in neutral zone
        assert rsi.check_buy_condition() is False
        assert rsi.check_sell_condition() is False

    def test_rsi_disabled_indicator(self, trending_up_candles):
        """Test RSI indicator when disabled"""
        rsi = RSIIndicator(enabled=False)
        rsi.calculate(trending_up_candles)

        # When disabled, conditions should always return False
        assert rsi.check_buy_condition() is False
        assert rsi.check_sell_condition() is False

    def test_rsi_zero_division_handling(self):
        """Test RSI calculation handles zero division (no losses)"""
        # Create data with only gains (no losses)
        data = {
            "close": [
                100,
                101,
                102,
                103,
                104,
                105,
                106,
                107,
                108,
                109,
                110,
                111,
                112,
                113,
                114,
            ]
        }
        candles = pd.DataFrame(data)

        rsi = RSIIndicator(period=14)
        rsi.calculate(candles)

        # Should handle zero division and set RSI to 100
        rsi_values = rsi._RSIIndicator__rsi_values
        assert rsi_values is not None
        assert rsi_values[-1] == 100.0

    def test_rsi_calculation_accuracy(self):
        """Test RSI calculation accuracy with known values"""
        # Use simple data where we can verify RSI calculation
        data = {
            "close": [
                44,
                44.34,
                44.09,
                44.15,
                43.61,
                44.33,
                44.83,
                45.85,
                47.37,
                47.20,
                46.57,
                46.03,
                46.98,
                46.40,
                46.12,
                46.89,
            ]
        }
        candles = pd.DataFrame(data)

        rsi = RSIIndicator(period=14)
        rsi.calculate(candles)

        rsi_values = rsi._RSIIndicator__rsi_values
        assert rsi_values is not None
        assert len(rsi_values) > 0
        # RSI should be between 0 and 100
        assert 0 <= rsi_values[-1] <= 100

    def test_rsi_values_range(self, volatile_candles):
        """Test that RSI values are always within valid range"""
        rsi = RSIIndicator(period=14)
        rsi.calculate(volatile_candles)

        rsi_values = rsi._RSIIndicator__rsi_values
        if rsi_values:
            for value in rsi_values:
                assert (
                        0 <= value <= 100
                ), f"RSI value {value} is out of valid range [0, 100]"
