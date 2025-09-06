# Python Trading Indicators

[![PyPI version](https://badge.fury.io/py/Python.Trading.Indicators.svg)](https://badge.fury.io/py/Python.Trading.Indicators)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Tests](https://github.com/venantvr/Python.Trading.Indicators/workflows/Tests/badge.svg)](https://github.com/venantvr/Python.Trading.Indicators/actions)
[![Coverage](https://codecov.io/gh/venantvr/Python.Trading.Indicators/branch/main/graph/badge.svg)](https://codecov.io/gh/venantvr/Python.Trading.Indicators)

A comprehensive Python library for technical analysis indicators used in algorithmic trading. Built with performance and extensibility in mind, this library provides a suite of technical indicators with a clean, consistent API for analyzing market data and generating buy/sell signals.

## ✨ Features

- **Modular Architecture**: Built around an abstract `Indicator` base class for consistency and extensibility
- **Performance Optimized**: Efficient calculations using pandas and numpy
- **Comprehensive Coverage**: RSI, VIX, Candlestick patterns, Price drops, and more
- **Easy Integration**: Simple API for incorporating indicators into trading strategies
- **Type Safety**: Full type hints for better development experience
- **Extensible**: Easy to add custom indicators following the established patterns

## 🚀 Quick Start

### Installation

```bash
pip install Python.Trading.Indicators
```

For development installation:

```bash
git clone https://github.com/venantvr/Python.Trading.Indicators.git
cd Python.Trading.Indicators
pip install -e .
```

### Basic Usage

```python
import pandas as pd
from venantvr.indicators.rsi import RSIIndicator
from venantvr.indicators.candlestick import CandlestickIndicator

# Sample market data
data = {
    'close': [100, 102, 105, 103, 108, 115, 110, 109, 107, 102, 95],
    'open': [98, 100, 102, 105, 103, 108, 115, 110, 109, 107, 102],
    'volume': [1000, 1100, 1200, 900, 1500, 2500, 1800, 1000, 1100, 2200, 3000]
}
candles = pd.DataFrame(data)

# RSI Indicator
rsi = RSIIndicator(period=14, buy_threshold=30, sell_threshold=70)
rsi.calculate(candles)

if rsi.check_buy_condition():
    print("🟢 RSI Buy signal detected")
if rsi.check_sell_condition():
    print("🔴 RSI Sell signal detected")

# Candlestick Pattern Analysis
candlestick = CandlestickIndicator(lookback_period=3)
candlestick.calculate(candles)

if candlestick.check_buy_condition():
    print("🟢 Bullish candlestick pattern with volume confirmation")
```

## 📊 Available Indicators

### RSI (Relative Strength Index)
Identifies overbought and oversold conditions in the market.

```python
from venantvr.indicators.rsi import RSIIndicator

rsi = RSIIndicator(
    period=14,           # Calculation period
    buy_threshold=30,    # Oversold threshold
    sell_threshold=70    # Overbought threshold
)
```

### Candlestick Pattern Analyzer
Analyzes recent candlestick patterns to determine bullish/bearish trends with volume confirmation.

```python
from venantvr.indicators.candlestick import CandlestickIndicator

candlestick = CandlestickIndicator(
    lookback_period=3,    # Number of candles to analyze
    volume_threshold=1.2  # Volume confirmation multiplier
)
```

### Sudden Price Drop Detector
Detects significant price drops that might indicate selling opportunities or rebounds.

```python
from venantvr.indicators.drop import SuddenPriceDropIndicator

drop_detector = SuddenPriceDropIndicator(
    drop_percentage=10,   # Minimum drop percentage
    lookback_period=20   # Period to check for highest price
)
```

### VIX (Volatility Index)
Measures market volatility and identifies panic conditions.

```python
from venantvr.indicators.vix import VIXIndicator

vix = VIXIndicator(
    period=20,           # Calculation period
    panic_threshold=25   # Volatility panic threshold
)
```

### PassThrough Indicator
A utility indicator for testing or temporarily disabling indicator logic.

```python
from venantvr.indicators.passthrough import PassThroughIndicator

passthrough = PassThroughIndicator(enabled=False)
```

## 🏗️ Architecture

All indicators inherit from the abstract `Indicator` base class, ensuring a consistent interface:

```python
from abc import ABC, abstractmethod
from pandas import DataFrame

class Indicator(ABC):
    def __init__(self, enabled: bool = True):
        self.is_enabled = enabled
    
    @abstractmethod
    def compute_indicator(self, candles: DataFrame):
        """Compute the indicator based on the provided candles."""
        pass
    
    @abstractmethod
    def evaluate_buy_condition(self) -> bool:
        """Evaluate if buy conditions are met."""
        pass
    
    @abstractmethod
    def evaluate_sell_condition(self) -> bool:
        """Evaluate if sell conditions are met."""
        pass
```

## 🧪 Testing

Run the complete test suite:

```bash
make test
```

Run tests with coverage:

```bash
make test-coverage
```

## 🔧 Development

Set up the development environment:

```bash
make setup-dev
```

Code formatting:

```bash
make format
```

Linting:

```bash
make lint
```

Run all quality checks:

```bash
make check
```

## 📈 Performance Considerations

- All indicators are optimized for pandas DataFrame operations
- Calculations are vectorized where possible for better performance
- Memory usage is minimized through efficient data handling
- Suitable for both real-time and batch processing scenarios

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

If you encounter any issues or have questions, please file an issue on the [GitHub repository](https://github.com/venantvr/Python.Trading.Indicators/issues).

## 🔗 Links

- **Repository**: https://github.com/venantvr/Python.Trading.Indicators
- **PyPI Package**: https://pypi.org/project/Python.Trading.Indicators/
- **Documentation**: [Coming Soon]

---

**Disclaimer**: This library is for educational and research purposes. Always do your own research before making any trading decisions. Past performance is not indicative of future results.
