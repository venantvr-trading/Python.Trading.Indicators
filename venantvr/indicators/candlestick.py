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
        self.__is_bullish = bool(bullish_count > bearish_count)
        self.__is_bearish = bool(bearish_count > bullish_count)

        # Volume confirmation
        if len(recent_candles) > 1:
            avg_volume = recent_candles['volume'].iloc[:-1].mean()
            latest_volume = recent_candles['volume'].iloc[-1]
            self.__volume_confirmed = bool(latest_volume > avg_volume * self.__volume_threshold) if avg_volume > 0 else False
        else:
            # For single candle, we need historical data from the full candles to compare
            if len(candles) > 1:
                avg_volume = candles['volume'].iloc[:-1].mean()
                latest_volume = candles['volume'].iloc[-1]
                self.__volume_confirmed = bool(latest_volume > avg_volume * self.__volume_threshold) if avg_volume > 0 else False
            else:
                # Only one candle total, can't confirm volume
                self.__volume_confirmed = False

        logger.info(f"Candlestick: bullish={self.__is_bullish}, bearish={self.__is_bearish}, "
                    f"volume_confirmed={self.__volume_confirmed}")

    def evaluate_sell_condition(self) -> bool:
        if not self.is_enabled:
            return False
        return bool(self.__is_bearish and self.__volume_confirmed)

    def evaluate_buy_condition(self) -> bool:
        if not self.is_enabled:
            return False
        return bool(self.__is_bullish and self.__volume_confirmed)
