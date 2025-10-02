from abc import ABC, abstractmethod
from typing import Optional

from pandas import DataFrame


class Indicator(ABC):

    def __init__(self, enabled: bool = True):
        self.is_enabled = enabled

    @abstractmethod
    def compute_indicator(self, candles: DataFrame):
        """
        Compute the indicator based on the provided candles.
        """
        pass

    def calculate(self, candles: DataFrame) -> bool:
        if not self.is_enabled:
            return True
        else:
            self.compute_indicator(
                candles
            )  # Call the specific indicator computation method
            return True  # Return True to indicate that calculation has been performed

    def check_sell_condition(self) -> bool:
        if not self.is_enabled:
            return False  # Disabled indicators provide no signal
        return self.evaluate_sell_condition()

    def check_buy_condition(self) -> bool:
        if not self.is_enabled:
            return False  # Disabled indicators provide no signal
        return self.evaluate_buy_condition()

    @abstractmethod
    def evaluate_sell_condition(self) -> bool:
        """
        Evaluate the sell condition based on the indicator's calculation.
        """
        pass

    @abstractmethod
    def evaluate_buy_condition(self) -> bool:
        """
        Evaluate the buy condition based on the indicator's calculation.
        """
        pass

    @property
    @abstractmethod
    def current_value(self) -> Optional[float]:
        """
        Return the current value of the indicator.
        Must be implemented by all indicators.
        """
        pass
