import pandas as pd
from .base import Strategy

class CustomStrategy(Strategy):
    """User-defined custom trading strategy."""
    
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """Generate custom signals (placeholder for UI/script input).
        
        Args:
            data: DataFrame with price data.
        
        Returns:
            Series of boolean signals (True for buy, False for no action).
        """
        # Example: Simple momentum strategy
        returns = data['close'].pct_change()
        signals = (returns > 0).astype(bool)
        return signals