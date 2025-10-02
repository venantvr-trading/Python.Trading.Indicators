from pandas import DataFrame

from python_trading_indicators.indicator import Indicator
from python_trading_indicators.tools.logger import logger


class SuddenPriceDropIndicator(Indicator):

    def __init__(
            self,
            drop_percentage: float = 5,
            lookback_period: int = 5,
            volume_threshold: float = 1.5,
            enabled: bool = True,
    ):
        super().__init__(enabled)
        self.__drop_percentage = drop_percentage / 100
        self.__lookback_period = lookback_period
        self.__volume_threshold = volume_threshold
        self.__drop_detected = False
        self.__volume_confirmed = False
        self.__insufficient_data = True

    def compute_indicator(self, candles: DataFrame):
        if len(candles) < self.__lookback_period:
            logger.warning("Not enough candles for SuddenPriceDropIndicator")
            self.__drop_detected = False
            self.__volume_confirmed = False
            self.__insufficient_data = True
            return

        self.__insufficient_data = False
        closes = candles["close"]
        recent_closes = closes.tail(self.__lookback_period)
        current_close = recent_closes.iloc[-1]
        max_close = recent_closes.max()

        self.__drop_detected = bool(
            (current_close / max_close - 1) < -self.__drop_percentage
        )

        avg_volume = (
            candles["volume"].iloc[-self.__lookback_period: -1].mean()
            if len(candles) > 1
            else 0
        )
        latest_volume = candles["volume"].iloc[-1]
        self.__volume_confirmed = (
            bool(latest_volume > avg_volume * self.__volume_threshold)
            if avg_volume > 0
            else False
        )

        logger.info(
            f"SuddenPriceDrop: drop_detected={self.__drop_detected}, "
            f"current_close={current_close:.2f}, max_close={max_close:.2f}, "
            f"volume_confirmed={self.__volume_confirmed}"
        )

    def evaluate_sell_condition(self) -> bool:
        if not self.is_enabled or self.__insufficient_data:
            return False
        return bool(self.__drop_detected and self.__volume_confirmed)

    def evaluate_buy_condition(self) -> bool:
        if not self.is_enabled or self.__insufficient_data:
            return False
        return bool(not self.__drop_detected)

    @property
    def current_value(self) -> float:
        """Return the current drop signal strength (1=drop detected, 0=no drop)"""
        if self.__insufficient_data:
            return 0.0
        return 1.0 if (self.__drop_detected and self.__volume_confirmed) else 0.0

    @property
    def period(self) -> int:
        """Return the drop detection lookback period"""
        return self.__lookback_period
