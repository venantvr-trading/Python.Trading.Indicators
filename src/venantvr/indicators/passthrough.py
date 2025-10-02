from pandas import DataFrame

from venantvr.indicators.indicator import Indicator
from venantvr.indicators.tools.logger import logger


class PassThroughIndicator(Indicator):
    def __init__(self, enabled: bool = False):  # Disabled by default
        super().__init__(enabled)

    def compute_indicator(self, candles: DataFrame):
        logger.warning("PassThroughIndicator used - no real analysis performed")

    def evaluate_sell_condition(self) -> bool:
        return self.is_enabled

    def evaluate_buy_condition(self) -> bool:
        return self.is_enabled

    @property
    def current_value(self) -> float:
        """Return 1.0 if enabled, 0.0 if disabled"""
        return 1.0 if self.is_enabled else 0.0
