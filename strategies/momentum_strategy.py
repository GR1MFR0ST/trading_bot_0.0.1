import pandas as pd

class MomentumStrategy:
    """Momentum-based strategy for memecoin trading."""
    
    def __init__(self, lookback_period: int = 5, threshold: float = 0.05):
        """Initialize with lookback period and threshold.
        
        Args:
            lookback_period: Number of periods to check for price change.
            threshold: Percentage price increase required to trigger a buy.
        """
        self.lookback_period = lookback_period
        self.threshold = threshold
    
    def generate_signals(self, data: pd.DataFrame) -> bool:
        """Generate buy signals based on momentum.
        
        Args:
            data: DataFrame with 'close' prices.
        
        Returns:
            True if a buy signal is generated, False otherwise.
        """
        if len(data) < self.lookback_period:
            return False
        recent_change = (data['close'].iloc[-1] - data['close'].iloc[-self.lookback_period]) / data['close'].iloc[-self.lookback_period]
        return recent_change > self.threshold