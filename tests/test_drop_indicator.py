import pytest
import pandas as pd

from venantvr.indicators.drop import SuddenPriceDropIndicator


# noinspection PyUnresolvedReferences
class TestSuddenPriceDropIndicator:
    """Test the Sudden Price Drop Indicator"""
    
    def test_drop_indicator_initialization(self):
        """Test drop indicator initialization with default parameters"""
        drop = SuddenPriceDropIndicator()
        
        assert drop.is_enabled is True
        assert drop._SuddenPriceDropIndicator__drop_percentage == 0.05  # 5% converted to decimal
        assert drop._SuddenPriceDropIndicator__lookback_period == 5
        assert drop._SuddenPriceDropIndicator__volume_threshold == 1.5
    
    def test_drop_indicator_custom_parameters(self):
        """Test drop indicator initialization with custom parameters"""
        drop = SuddenPriceDropIndicator(
            drop_percentage=10, 
            lookback_period=10, 
            volume_threshold=2.0, 
            enabled=False
        )
        
        assert drop.is_enabled is False
        assert drop._SuddenPriceDropIndicator__drop_percentage == 0.10  # 10% converted to decimal
        assert drop._SuddenPriceDropIndicator__lookback_period == 10
        assert drop._SuddenPriceDropIndicator__volume_threshold == 2.0
    
    def test_drop_insufficient_data(self, insufficient_candles):
        """Test drop calculation with insufficient data"""
        drop = SuddenPriceDropIndicator(lookback_period=5)
        drop.calculate(insufficient_candles)
        
        assert drop.check_buy_condition() is False
        assert drop.check_sell_condition() is False
    
    def test_drop_detection_with_volume(self):
        """Test sudden price drop detection with volume confirmation"""
        data = {
            'close': [100, 100, 100, 100, 90],  # 10% drop from max
            'volume': [1000, 1000, 1000, 1000, 2500]  # High volume on drop
        }
        candles = pd.DataFrame(data)
        
        drop = SuddenPriceDropIndicator(drop_percentage=8, volume_threshold=2.0, lookback_period=5)
        drop.calculate(candles)
        
        assert drop.check_buy_condition() is False  # Drop detected, so no buy
        assert drop.check_sell_condition() is True  # Drop with volume confirmation
    
    def test_drop_detection_without_volume(self):
        """Test sudden price drop detection without volume confirmation"""
        data = {
            'close': [100, 100, 100, 100, 90],  # 10% drop from max
            'volume': [1000, 1000, 1000, 1000, 1000]  # No volume spike
        }
        candles = pd.DataFrame(data)
        
        drop = SuddenPriceDropIndicator(drop_percentage=8, volume_threshold=2.0, lookback_period=5)
        drop.calculate(candles)
        
        assert drop.check_buy_condition() is False  # Drop detected, so no buy
        assert drop.check_sell_condition() is False  # No volume confirmation
    
    def test_no_drop_detection(self):
        """Test when no significant drop is detected"""
        data = {
            'close': [100, 102, 101, 103, 98],  # Small fluctuations, no significant drop
            'volume': [1000, 1000, 1000, 1000, 2000]
        }
        candles = pd.DataFrame(data)
        
        drop = SuddenPriceDropIndicator(drop_percentage=5, lookback_period=5)
        drop.calculate(candles)
        
        assert drop.check_buy_condition() is True   # No drop detected, buy condition
        assert drop.check_sell_condition() is False # No drop, no sell condition
    
    def test_drop_threshold_exact(self):
        """Test drop detection at exact threshold"""
        data = {
            'close': [100, 100, 100, 100, 95],  # Exactly 5% drop
            'volume': [1000, 1000, 1000, 1000, 2000]
        }
        candles = pd.DataFrame(data)
        
        drop = SuddenPriceDropIndicator(drop_percentage=5, volume_threshold=1.5, lookback_period=5)
        drop.calculate(candles)
        
        # Should detect drop (current/max - 1 = 95/100 - 1 = -0.05, which is exactly threshold)
        assert drop.check_buy_condition() is False
        assert drop.check_sell_condition() is True
    
    def test_drop_price_recovery(self):
        """Test drop detection when price recovers"""
        data = {
            'close': [100, 90, 95, 98, 99],  # Drop then recovery
            'volume': [1000, 2000, 1000, 1000, 1000]
        }
        candles = pd.DataFrame(data)
        
        drop = SuddenPriceDropIndicator(drop_percentage=5, lookback_period=5)
        drop.calculate(candles)
        
        # Current close (99) vs max (100), only 1% drop from max
        assert drop.check_buy_condition() is True   # No significant drop from max
        assert drop.check_sell_condition() is False
    
    def test_drop_gradual_decline(self):
        """Test drop detection with gradual decline"""
        data = {
            'close': [100, 98, 96, 94, 92],  # Gradual decline, 8% total
            'volume': [1000, 1000, 1000, 1000, 2000]
        }
        candles = pd.DataFrame(data)
        
        drop = SuddenPriceDropIndicator(drop_percentage=7, volume_threshold=1.5, lookback_period=5)
        drop.calculate(candles)
        
        # 8% drop from max (100 to 92) should trigger
        assert drop.check_buy_condition() is False
        assert drop.check_sell_condition() is True
    
    def test_drop_disabled_indicator(self):
        """Test drop indicator when disabled"""
        data = {
            'close': [100, 100, 100, 100, 80],  # 20% drop
            'volume': [1000, 1000, 1000, 1000, 3000]
        }
        candles = pd.DataFrame(data)
        
        drop = SuddenPriceDropIndicator(enabled=False)
        drop.calculate(candles)
        
        assert drop.check_buy_condition() is False
        assert drop.check_sell_condition() is False
    
    def test_drop_zero_average_volume(self):
        """Test drop calculation with zero average volume"""
        data = {
            'close': [100, 100, 100, 100, 90],
            'volume': [0, 0, 0, 0, 1000]  # Zero volume in earlier periods
        }
        candles = pd.DataFrame(data)
        
        drop = SuddenPriceDropIndicator(drop_percentage=8, lookback_period=5)
        drop.calculate(candles)
        
        # Should handle zero average volume gracefully
        assert drop.check_buy_condition() is False  # Drop detected
        assert drop.check_sell_condition() is False  # No volume confirmation possible
    
    def test_drop_single_candle_data(self):
        """Test drop calculation with single candle"""
        data = {
            'close': [100],
            'volume': [1000]
        }
        candles = pd.DataFrame(data)
        
        drop = SuddenPriceDropIndicator(lookback_period=1)
        drop.calculate(candles)
        
        # With single candle, max == current, so no drop
        assert drop.check_buy_condition() is True
        assert drop.check_sell_condition() is False