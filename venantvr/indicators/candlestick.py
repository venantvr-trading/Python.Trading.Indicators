from pandas import DataFrame

from venantvr.indicators.indicator import Indicator
from venantvr.indicators.tools.logger import logger


class CandlestickIndicator(Indicator):
    def __init__(self, lookback_period: int = 3, volume_threshold: float = 1.5, enabled: bool = True):
        super().__init__(enabled)
        self.__lookback_period = lookback_period
        self.__volume_threshold = volume_threshold
        self.__is_bullish = False
        self.__is_bearish = False
        self.__volume_confirmed = False

    def compute_indicator(self, candles: DataFrame):
        if len(candles) < self.__lookback_period:
            logger.warning("Not enough candles for CandlestickIndicator")
            self.__is_bullish = False
            self.__is_bearish = False
            self.__volume_confirmed = False
            return

        recent_candles = candles.tail(self.__lookback_period)
        closes = recent_candles['close']
        opens = recent_candles['open']

        # Check for bullish/bearish pattern (majority of recent candles)
        bullish_count = sum(1 for c, o in zip(closes, opens) if c > o)
        bearish_count = sum(1 for c, o in zip(closes, opens) if c < o)
        self.__is_bullish = bullish_count > bearish_count
        self.__is_bearish = bearish_count > bullish_count

        # Volume confirmation
        avg_volume = recent_candles['volume'].iloc[:-1].mean() if len(recent_candles) > 1 else 0
        latest_volume = recent_candles['volume'].iloc[-1]
        self.__volume_confirmed = latest_volume > avg_volume * self.__volume_threshold if avg_volume > 0 else False

        logger.info(f"Candlestick: bullish={self.__is_bullish}, bearish={self.__is_bearish}, "
                    f"volume_confirmed={self.__volume_confirmed}")

    def evaluate_sell_condition(self) -> bool:
        if not self.__is_enabled:
            return False
        return self.__is_bearish and self.__volume_confirmed

    def evaluate_buy_condition(self) -> bool:
        if not self.__is_enabled:
            return False
        return self.__is_bullish and self.__volume_confirmed
