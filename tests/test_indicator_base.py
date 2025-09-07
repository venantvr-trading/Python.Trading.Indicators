import pytest
from pandas import DataFrame

from venantvr.indicators.indicator import Indicator


class TestIndicatorImplementation(Indicator):
    """Test implementation of the abstract Indicator class"""

    def __init__(self, enabled: bool = True):
        super().__init__(enabled)
        self.computed = False
        self.buy_condition = False
        self.sell_condition = False

    def compute_indicator(self, candles: DataFrame):
        self.computed = True

    def evaluate_buy_condition(self) -> bool:
        return self.buy_condition

    def evaluate_sell_condition(self) -> bool:
        return self.sell_condition


class TestIndicatorBase:
    """Test the abstract Indicator base class"""

    def test_indicator_is_abstract(self):
        """Test that Indicator class is abstract and cannot be instantiated directly"""
        with pytest.raises(TypeError):
            Indicator()

    def test_indicator_inheritance(self):
        """Test that concrete implementations can be instantiated"""
        indicator = TestIndicatorImplementation()
        assert isinstance(indicator, Indicator)
        assert indicator.is_enabled is True

    def test_indicator_enabled_by_default(self):
        """Test that indicators are enabled by default"""
        indicator = TestIndicatorImplementation()
        assert indicator.is_enabled is True

    def test_indicator_can_be_disabled(self):
        """Test that indicators can be disabled during initialization"""
        indicator = TestIndicatorImplementation(enabled=False)
        assert indicator.is_enabled is False

    def test_calculate_when_enabled(self, sample_candles):
        """Test calculate method when indicator is enabled"""
        indicator = TestIndicatorImplementation(enabled=True)
        result = indicator.calculate(sample_candles)

        assert result is True
        assert indicator.computed is True

    def test_calculate_when_disabled(self, sample_candles):
        """Test calculate method when indicator is disabled"""
        indicator = TestIndicatorImplementation(enabled=False)
        result = indicator.calculate(sample_candles)

        assert result is True
        assert indicator.computed is False  # Should not compute when disabled

    def test_check_buy_condition_when_enabled(self):
        """Test buy condition checking when enabled"""
        indicator = TestIndicatorImplementation(enabled=True)
        indicator.buy_condition = True

        assert indicator.check_buy_condition() is True

        indicator.buy_condition = False
        assert indicator.check_buy_condition() is False

    def test_check_buy_condition_when_disabled(self):
        """Test buy condition checking when disabled"""
        indicator = TestIndicatorImplementation(enabled=False)
        indicator.buy_condition = True

        # When disabled, should return False (no signal) regardless of actual condition
        assert indicator.check_buy_condition() is False

    def test_check_sell_condition_when_enabled(self):
        """Test sell condition checking when enabled"""
        indicator = TestIndicatorImplementation(enabled=True)
        indicator.sell_condition = True

        assert indicator.check_sell_condition() is True

        indicator.sell_condition = False
        assert indicator.check_sell_condition() is False

    def test_check_sell_condition_when_disabled(self):
        """Test sell condition checking when disabled"""
        indicator = TestIndicatorImplementation(enabled=False)
        indicator.sell_condition = True

        # When disabled, should return False (no signal) regardless of actual condition
        assert indicator.check_sell_condition() is False
