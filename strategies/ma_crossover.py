import talib as ta
import pandas as pd
from .base import Strategy

class MACrossoverStrategy(Strategy):
    """Moving Average Crossover strategy using short and long MAs."""
    
    def __init__(self, short_period: int = 50, long_period: int = 200):
        """Initialize the strategy with MA periods.
        
        Args:
            short_period: Period for the short moving average.
            long_period: Period for the long moving average.
        """
        self.short_period = short_period
        self.long_period = long_period
    
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """Generate signals based on MA crossover.
        
        Args:
            data: DataFrame with 'close' column.
        
        Returns:
            Series of boolean signals (True for buy, False for sell/no action).
        """
        short_ma = ta.SMA(data['close'], timeperiod=self.short_period)
        long_ma = ta.SMA(data['close'], timeperiod=self.long_period)
        signals = (short_ma > long_ma).astype(bool)
        return signals