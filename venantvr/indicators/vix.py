import numpy as np
from pandas import DataFrame

from venantvr.indicators.indicator import Indicator
from venantvr.indicators.tools.logger import logger


class VIXIndicator(Indicator):
    def __init__(
            self,
            period: int = 14,
            panic_threshold: float = 30,
            volume_threshold: float = 1.5,
            enabled: bool = True,
    ):
        super().__init__(enabled)
        self.__period = period
        self.__panic_threshold = panic_threshold
        self.__volume_threshold = volume_threshold
        self.__vix = None
        self.__volume_confirmed = False

    def compute_indicator(self, candles: DataFrame):
        if (
                len(candles) <= self.__period
        ):  # Need at least period + 1 for returns calculation
            logger.warning("Not enough candles for VIXIndicator")
            self.__vix = None
            self.__volume_confirmed = False
            return

        closes = candles["close"]
        returns = np.log(closes / closes.shift(1))
        volatility = returns.rolling(window=self.__period).std() * np.sqrt(252) * 100
        self.__vix = (
            volatility.iloc[-1]
            if not volatility.empty and not np.isnan(volatility.iloc[-1])
            else None
        )

        avg_volume = (
            candles["volume"].iloc[-self.__period: -1].mean()
            if len(candles) > 1
            else 0
        )
        latest_volume = candles["volume"].iloc[-1]
        self.__volume_confirmed = (
            bool(latest_volume > avg_volume * self.__volume_threshold)
            if avg_volume > 0
            else False
        )

        vix_str = f"{self.__vix:.2f}" if self.__vix is not None else "None"
        logger.info(f"VIX: {vix_str}, volume_confirmed={self.__volume_confirmed}")

    def evaluate_sell_condition(self) -> bool:
        if not self.is_enabled or self.__vix is None:
            return False
        return bool(self.__vix > self.__panic_threshold and self.__volume_confirmed)

    def evaluate_buy_condition(self) -> bool:
        if not self.is_enabled or self.__vix is None:
            return False
        return bool(self.__vix < self.__panic_threshold - 5)

    @property
    def current_value(self) -> float:
        """Return the current VIX value"""
        if self.__vix is None:
            return 0.0
        return self.__vix

    @property
    def period(self) -> int:
        """Return the VIX calculation period"""
        return self.__period
