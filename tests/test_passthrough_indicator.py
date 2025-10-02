import pandas as pd

from python_trading_indicators.passthrough import PassThroughIndicator


class TestPassThroughIndicator:
    """Test the PassThrough Indicator (utility indicator for testing)"""

    def test_passthrough_indicator_initialization_default(self):
        """Test passthrough indicator initialization with default parameters"""
        passthrough = PassThroughIndicator()

        # PassThrough is disabled by default
        assert passthrough.is_enabled is False

    def test_passthrough_indicator_initialization_enabled(self):
        """Test passthrough indicator initialization when explicitly enabled"""
        passthrough = PassThroughIndicator(enabled=True)

        assert passthrough.is_enabled is True

    def test_passthrough_disabled_behavior(self, sample_candles):
        """Test passthrough behavior when disabled (default)"""
        passthrough = PassThroughIndicator()  # Disabled by default

        # Calculate should work but not perform real analysis
        result = passthrough.calculate(sample_candles)
        assert result is True

        # When disabled, both conditions should return False
        assert passthrough.check_buy_condition() is False
        assert passthrough.check_sell_condition() is False

    def test_passthrough_enabled_behavior(self, sample_candles):
        """Test passthrough behavior when enabled"""
        passthrough = PassThroughIndicator(enabled=True)

        # Calculate should work
        result = passthrough.calculate(sample_candles)
        assert result is True

        # When enabled, both conditions should return True (passthrough behavior)
        assert passthrough.check_buy_condition() is True
        assert passthrough.check_sell_condition() is True

    def test_passthrough_compute_indicator(self, sample_candles):
        """Test that compute_indicator method executes without error"""
        passthrough = PassThroughIndicator(enabled=True)

        # Should not raise any exceptions
        passthrough.compute_indicator(sample_candles)

        # The method should execute but not store any computed values
        # (it's a passthrough, so no real computation)

    def test_passthrough_with_empty_dataframe(self):
        """Test passthrough with empty DataFrame"""
        empty_candles = pd.DataFrame()
        passthrough = PassThroughIndicator(enabled=True)

        # Should handle empty DataFrame gracefully
        result = passthrough.calculate(empty_candles)
        assert result is True

        assert passthrough.check_buy_condition() is True
        assert passthrough.check_sell_condition() is True

    def test_passthrough_with_minimal_data(self, insufficient_candles):
        """Test passthrough with insufficient data"""
        passthrough = PassThroughIndicator(enabled=True)

        # Should work regardless of data sufficiency
        result = passthrough.calculate(insufficient_candles)
        assert result is True

        assert passthrough.check_buy_condition() is True
        assert passthrough.check_sell_condition() is True

    def test_passthrough_evaluate_conditions_directly(self):
        """Test direct evaluation of buy/sell conditions"""
        # Test disabled state
        passthrough_disabled = PassThroughIndicator(enabled=False)
        assert passthrough_disabled.evaluate_buy_condition() is False
        assert passthrough_disabled.evaluate_sell_condition() is False

        # Test enabled state
        passthrough_enabled = PassThroughIndicator(enabled=True)
        assert passthrough_enabled.evaluate_buy_condition() is True
        assert passthrough_enabled.evaluate_sell_condition() is True

    def test_passthrough_toggle_enabled_state(self, sample_candles):
        """Test changing enabled state after initialization"""
        passthrough = PassThroughIndicator(enabled=False)

        # Initially disabled
        assert passthrough.check_buy_condition() is False
        assert passthrough.check_sell_condition() is False

        # Enable the indicator
        passthrough.is_enabled = True

        # Now should return True for both conditions
        assert passthrough.check_buy_condition() is True
        assert passthrough.check_sell_condition() is True

        # Disable again
        passthrough.is_enabled = False

        # Should return False again
        assert passthrough.check_buy_condition() is False
        assert passthrough.check_sell_condition() is False

    def test_passthrough_inheritance(self):
        """Test that PassThroughIndicator properly inherits from Indicator"""
        from python_trading_indicators.indicator import Indicator

        passthrough = PassThroughIndicator()
        assert isinstance(passthrough, Indicator)

        # Should have all the methods from the base class
        assert hasattr(passthrough, "calculate")
        assert hasattr(passthrough, "check_buy_condition")
        assert hasattr(passthrough, "check_sell_condition")
        assert hasattr(passthrough, "compute_indicator")
        assert hasattr(passthrough, "evaluate_buy_condition")
        assert hasattr(passthrough, "evaluate_sell_condition")

    def test_passthrough_consistent_behavior(self, sample_candles):
        """Test that passthrough behavior is consistent across multiple calls"""
        passthrough = PassThroughIndicator(enabled=True)

        # Multiple calculations should yield consistent results
        for _ in range(5):
            result = passthrough.calculate(sample_candles)
            assert result is True
            assert passthrough.check_buy_condition() is True
            assert passthrough.check_sell_condition() is True
