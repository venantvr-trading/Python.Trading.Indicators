# Python.Trading.Indicators

## Description

`Python.Trading.Indicators` est une bibliothèque Python conçue pour fournir une suite d'indicateurs d'analyse technique pour le trading. Elle est construite autour d'une
classe de base `Indicator` et permet de calculer des conditions d'achat et de vente basées sur les données de bougies (candlesticks).

## Installation

Cette bibliothèque est conçue pour être installée en tant que package Python.

```
pip install .
```

ou, si vous souhaitez l'installer en mode "editable" pour le développement :

```
pip install -e .
```

### Prérequis

* Python \>= 3.8
* pandas
* numpy

## Modules et fonctionnalités

### `indicator.py`

Ce module définit la classe abstraite `Indicator`, qui sert de base à tous les indicateurs. Elle établit une interface commune pour le calcul, l'évaluation des conditions
d'achat/vente et la gestion d'un état "activé" ou "désactivé".

### `candlestick.py`

* **`CandlestickIndicator`**: Cet indicateur analyse les bougies récentes pour déterminer si la tendance est haussière (bullish) ou baissière (bearish). Il vérifie
  également si cette tendance est confirmée par un volume de trading élevé, comparé à la moyenne passée.

### `drop.py`

* **`SuddenPriceDropIndicator`**: Cet indicateur détecte les baisses de prix soudaines. Il compare le cours de clôture actuel avec le cours le plus élevé des
  `lookback_period` précédentes et vérifie si la baisse est confirmée par un volume élevé.

### `rsi.py`

* **`RSIIndicator`**: Un indicateur de force relative (Relative Strength Index). Il calcule le RSI et évalue les conditions d'achat ou de vente basées sur des seuils de
  survente (en dessous de 30) et de surachat (au-dessus de 70).

### `vix.py`

* **`VIXIndicator`**: Cet indicateur mesure la volatilité du marché. Il calcule une mesure de la volatilité et évalue les conditions de "panique" si cette valeur dépasse
  un certain seuil. Un volume élevé peut confirmer cette condition.

### `passthrough.py`

* **`PassThroughIndicator`**: Un indicateur simple et désactivé par défaut. Il ne fait aucune analyse réelle et est utile pour désactiver temporairement un indicateur
  sans modifier le reste du code.

## Utilisation

Voici un exemple d'utilisation des indicateurs avec des données de bougies fictives (DataFrame de pandas).

```python
import pandas as pd
from venantvr.indicators.rsi import RSIIndicator
from venantvr.indicators.drop import SuddenPriceDropIndicator
from venantvr.indicators.candlestick import CandlestickIndicator
from venantvr.indicators.vix import VIXIndicator

# Création de données de bougies fictives
data = {
    'close': [100, 102, 105, 103, 108, 115, 110, 109, 107, 102, 95],
    'open': [98, 100, 102, 105, 103, 108, 115, 110, 109, 107, 102],
    'volume': [1000, 1100, 1200, 900, 1500, 2500, 1800, 1000, 1100, 2200, 3000]
}
candles = pd.DataFrame(data)

# Utilisation de l'indicateur RSI
rsi_indicator = RSIIndicator(period=5, buy_threshold=40, sell_threshold=60)
rsi_indicator.calculate(candles)
if rsi_indicator.check_buy_condition():
    print("RSI: Condition d'achat détectée.")
if rsi_indicator.check_sell_condition():
    print("RSI: Condition de vente détectée.")

# Utilisation de l'indicateur de baisse de prix
drop_indicator = SuddenPriceDropIndicator(drop_percentage=10)
drop_indicator.calculate(candles)
if drop_indicator.check_sell_condition():
    print("Drop: Baisse de prix soudaine détectée.")
if drop_indicator.check_buy_condition():
    print("Drop: Aucune baisse de prix soudaine détectée.")

# Utilisation de l'indicateur Candlestick
candlestick_indicator = CandlestickIndicator(lookback_period=3)
candlestick_indicator.calculate(candles)
if candlestick_indicator.check_buy_condition():
    print("Candlestick: Tendance haussière confirmée par le volume.")
if candlestick_indicator.check_sell_condition():
    print("Candlestick: Tendance baissière confirmée par le volume.")

# Utilisation de l'indicateur VIX
vix_indicator = VIXIndicator(period=5, panic_threshold=20)
vix_indicator.calculate(candles)
if vix_indicator.check_sell_condition():
    print("VIX: Volatilité élevée, possible condition de panique.")
```
