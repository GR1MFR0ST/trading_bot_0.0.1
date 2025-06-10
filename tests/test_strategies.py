import pytest
import pandas as pd
from strategies.ma_crossover import MACrossoverStrategy

def test_ma_crossover_signals():
    """Test MA Crossover strategy signals."""
    data = pd.DataFrame({"close": [100, 101, 102, 103, 104, 105, 106, 107, 108, 109]})
    strategy = MACrossoverStrategy(short_period=2, long_period=5)
    signals = strategy.generate_signals(data)
    assert len(signals) == len(data)
    assert signals.iloc[-1] == True  # Uptrend should signal buy