import numpy as np
import pandas as pd

from venantvr.indicators.vix import VIXIndicator


# noinspection PyUnresolvedReferences
class TestVIXIndicator:
    """Test the VIX (Volatility Index) Indicator"""

    def test_vix_indicator_initialization(self):
        """Test VIX indicator initialization with default parameters"""
        vix = VIXIndicator()

        assert vix.is_enabled is True
        assert vix._VIXIndicator__period == 14
        assert vix._VIXIndicator__panic_threshold == 30
        assert vix._VIXIndicator__volume_threshold == 1.5

    def test_vix_indicator_custom_parameters(self):
        """Test VIX indicator initialization with custom parameters"""
        vix = VIXIndicator(
            period=21, panic_threshold=25, volume_threshold=2.0, enabled=False
        )

        assert vix.is_enabled is False
        assert vix._VIXIndicator__period == 21
        assert vix._VIXIndicator__panic_threshold == 25
        assert vix._VIXIndicator__volume_threshold == 2.0

    def test_vix_insufficient_data(self, insufficient_candles):
        """Test VIX calculation with insufficient data"""
        vix = VIXIndicator(period=14)
        vix.calculate(insufficient_candles)

        assert vix.check_buy_condition() is False
        assert vix.check_sell_condition() is False

    def test_vix_high_volatility_with_volume(self, volatile_candles):
        """Test VIX calculation with high volatility and volume confirmation"""
        # Add high volume to the last candle
        volatile_candles_copy = volatile_candles.copy()
        volatile_candles_copy.loc[volatile_candles_copy.index[-1], "volume"] = 5000

        vix = VIXIndicator(period=20, panic_threshold=15, volume_threshold=1.5)
        vix.calculate(volatile_candles_copy)

        # Should detect high volatility
        vix_value = vix._VIXIndicator__vix
        assert vix_value is not None
        assert vix_value >= 0  # VIX should be positive

        # Depending on the data, might trigger sell condition
        if vix_value > 15:
            assert vix.check_sell_condition() is True

    def test_vix_low_volatility(self):
        """Test VIX calculation with low volatility data"""
        # Create stable price data
        prices = [100] * 30  # Constant prices = no volatility
        data = {"close": prices, "volume": [1000] * 30}
        candles = pd.DataFrame(data)

        vix = VIXIndicator(period=20, panic_threshold=30)
        vix.calculate(candles)

        vix_value = vix._VIXIndicator__vix
        # With constant prices, VIX should be very low or zero
        assert vix_value is not None
        assert vix_value < 5  # Should be very low volatility

        assert vix.check_buy_condition() is True  # Low volatility = buy condition
        assert vix.check_sell_condition() is False  # No panic condition

    # noinspection PyTypeChecker
    def test_vix_calculation_accuracy(self):
        """Test VIX calculation produces reasonable values"""
        # Create realistic price movement data
        np.random.seed(42)
        prices = [100]
        for i in range(50):
            change = np.random.normal(0, 0.02)  # 2% daily volatility
            prices.append(prices[-1] * (1 + change))

        data = {"close": prices, "volume": np.random.randint(1000, 3000, len(prices))}
        candles = pd.DataFrame(data)

        vix = VIXIndicator(period=20)
        vix.calculate(candles)

        vix_value = vix._VIXIndicator__vix
        assert vix_value is not None
        assert 0 <= vix_value <= 200  # Reasonable VIX range
        assert isinstance(vix_value, (int, float))

    def test_vix_panic_threshold_buy_condition(self):
        """Test VIX buy condition below panic threshold"""
        data = {
            "close": [100, 100.1, 99.9, 100.05, 99.95] * 10,  # Low volatility
            "volume": [1000] * 50,
        }
        candles = pd.DataFrame(data)

        vix = VIXIndicator(period=20, panic_threshold=30)
        vix.calculate(candles)

        vix_value = vix._VIXIndicator__vix
        if vix_value is not None and vix_value < 25:  # Below panic threshold - 5
            assert vix.check_buy_condition() is True

    def test_vix_panic_threshold_sell_condition(self, volatile_candles):
        """Test VIX sell condition above panic threshold with volume"""
        # Ensure high volume on last candle
        volatile_candles_copy = volatile_candles.copy()
        volatile_candles_copy.loc[volatile_candles_copy.index[-1], "volume"] = 8000

        vix = VIXIndicator(period=20, panic_threshold=20, volume_threshold=1.2)
        vix.calculate(volatile_candles_copy)

        vix_value = vix._VIXIndicator__vix
        if vix_value is not None and vix_value > 20:
            # Volume confirmation needed for sell condition
            volume_confirmed = vix._VIXIndicator__volume_confirmed
            if volume_confirmed:
                assert vix.check_sell_condition() is True

    def test_vix_disabled_indicator(self, volatile_candles):
        """Test VIX indicator when disabled"""
        vix = VIXIndicator(enabled=False)
        vix.calculate(volatile_candles)

        assert vix.check_buy_condition() is False
        assert vix.check_sell_condition() is False

    def test_vix_zero_average_volume(self):
        """Test VIX calculation with zero average volume"""
        data = {
            "close": [100, 105, 95, 110, 90] * 10,
            "volume": [0] * 49 + [1000],  # Zero volume except last
        }
        candles = pd.DataFrame(data)

        vix = VIXIndicator(period=20)
        vix.calculate(candles)

        # Should handle zero average volume gracefully
        vix_value = vix._VIXIndicator__vix
        assert vix_value is not None
        # Volume confirmation should be False due to zero average
        assert vix._VIXIndicator__volume_confirmed is False

    def test_vix_single_period_calculation(self):
        """Test VIX with minimum required period"""
        data = {
            "close": [
                100,
                102,
                98,
                101,
                99,
                103,
                97,
                104,
                96,
                105,
                95,
                106,
                94,
                107,
                93,
            ],
            "volume": [1000] * 15,
        }
        candles = pd.DataFrame(data)

        vix = VIXIndicator(period=14)
        vix.calculate(candles)

        vix_value = vix._VIXIndicator__vix
        assert vix_value is not None
        assert vix_value >= 0

    def test_vix_boundary_conditions(self):
        """Test VIX calculation at boundary conditions"""
        # Test with minimum required data (period + 1 for returns calculation)
        data = {
            "close": list(range(100, 121)),  # 21 points for period=20
            "volume": [1000] * 21,
        }
        candles = pd.DataFrame(data)

        vix = VIXIndicator(period=20)
        vix.calculate(candles)

        vix_value = vix._VIXIndicator__vix
        assert vix_value is not None

        # Test edge case where all conditions are exactly at thresholds
        if vix_value is not None:
            assert isinstance(vix_value, (int, float, np.floating))
            assert not np.isnan(vix_value)
            assert not np.isinf(vix_value)
