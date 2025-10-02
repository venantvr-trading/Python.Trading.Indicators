from pandas import DataFrame

from python_trading_indicators.indicator import Indicator
from python_trading_indicators.tools.logger import logger


class RSIIndicator(Indicator):

    def __init__(
            self,
            period: int = 14,
            buy_threshold: float = 30,
            sell_threshold: float = 70,
            enabled: bool = True,
    ):
        super().__init__(enabled)
        self.__period = period
        self.__buy_threshold = buy_threshold  # RSI < 30 for buy
        self.__sell_threshold = sell_threshold  # RSI > 70 for sell
        self.__rsi_values = None

    def compute_indicator(self, candles: DataFrame):
        if len(candles) < self.__period:
            logger.warning("Not enough candles for RSIIndicator")
            self.__rsi_values = None
            return

        closes = candles["close"]
        gains = []
        losses = []
        for i in range(1, len(closes)):
            diff = closes.iloc[i] - closes.iloc[i - 1]
            gains.append(max(diff, 0))
            losses.append(-min(diff, 0))

        avg_gain = sum(gains[: self.__period]) / self.__period
        avg_loss = sum(losses[: self.__period]) / self.__period

        rsi_values = []
        for i in range(self.__period, len(closes)):
            avg_gain = (avg_gain * (self.__period - 1) + gains[i - 1]) / self.__period
            avg_loss = (avg_loss * (self.__period - 1) + losses[i - 1]) / self.__period
            if avg_loss == 0:
                rsi = 100.0
            else:
                rs = avg_gain / avg_loss
                rsi = 100.0 - (100.0 / (1 + rs))
            rsi_values.append(rsi)

        self.__rsi_values = rsi_values
        logger.info(
            f"RSI: {self.__rsi_values[-1]:.2f}" if self.__rsi_values else "RSI: None"
        )

    def evaluate_sell_condition(self) -> bool:
        if not self.is_enabled or not self.__rsi_values:
            return False
        return bool(self.__rsi_values[-1] > self.__sell_threshold)

    def evaluate_buy_condition(self) -> bool:
        if not self.is_enabled or not self.__rsi_values:
            return False
        return bool(self.__rsi_values[-1] < self.__buy_threshold)

    @property
    def current_value(self) -> float:
        """Return the current RSI value"""
        if not self.__rsi_values:
            return 0.0
        return self.__rsi_values[-1]

    @property
    def period(self) -> int:
        """Return the RSI period"""
        return self.__period
