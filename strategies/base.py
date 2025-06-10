from abc import ABC, abstractmethod
import pandas as pd

class Strategy(ABC):
    """Abstract base class for trading strategies."""
    
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """Generate buy/sell signals based on input data.
        
        Args:
            data: DataFrame with price data (e.g., 'close', 'high', 'low').
        
        Returns:
            Series of boolean signals (True for buy, False otherwise).
        """
        pass