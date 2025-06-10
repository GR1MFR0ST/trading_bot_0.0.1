import pandas as pd
from .base import Strategy
from .ma_crossover import MACrossoverStrategy
from .rsi import RSIStrategy
from .macd import MACDStrategy

class VotingStrategy(Strategy):
    """Strategy combining multiple indicators via majority voting."""
    
    def __init__(self):
        """Initialize component strategies."""
        self.strategies = [
            MACrossoverStrategy(),
            RSIStrategy(),
            MACDStrategy()
        ]
    
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """Generate signals based on majority vote.
        
        Args:
            data: DataFrame with 'close' column.
        
        Returns:
            Series of boolean signals (True for buy, False for no action).
        """
        votes = [strategy.generate_signals(data) for strategy in self.strategies]
        vote_sum = sum(votes)
        signals = (vote_sum > len(self.strategies) / 2).astype(bool)
        return signals