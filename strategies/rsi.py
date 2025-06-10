import talib as ta
import pandas as pd
from .base import Strategy

class RSIStrategy(Strategy):
    """RSI-based trading strategy."""
    
    def __init__(self, period: int = 14, overbought: float = 70, oversold: float = 30):
        """Initialize RSI strategy parameters.
        
        Args:
            period: RSI calculation period.
            overbought: RSI level for sell signal.
            oversold: RSI level for buy signal.
        """
        self.period = period
        self.overbought = overbought
        self.oversold = oversold
    
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """Generate signals based on RSI levels.
        
        Args:
            data: DataFrame with 'close' column.
        
        Returns:
            Series of boolean signals (True for buy, False for no action/sell).
        """
        rsi = ta.RSI(data['close'], timeperiod=self.period)
        signals = (rsi < self.oversold).astype(bool)
        return signals