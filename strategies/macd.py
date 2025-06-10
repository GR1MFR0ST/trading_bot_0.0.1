import talib as ta
import pandas as pd
from .base import Strategy

class MACDStrategy(Strategy):
    """MACD-based trading strategy."""
    
    def __init__(self, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9):
        """Initialize MACD strategy parameters.
        
        Args:
            fast_period: Fast EMA period.
            slow_period: Slow EMA period.
            signal_period: Signal line period.
        """
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period
    
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """Generate signals based on MACD crossover.
        
        Args:
            data: DataFrame with 'close' column.
        
        Returns:
            Series of boolean signals (True for buy, False for no action).
        """
        macd, signal, _ = ta.MACD(data['close'], fastperiod=self.fast_period, 
                                slowperiod=self.slow_period, signalperiod=self.signal_period)
        signals = (macd > signal).astype(bool)
        return signals