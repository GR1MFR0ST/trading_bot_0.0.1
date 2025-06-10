import pandas as pd

class MomentumStrategy:
    """Momentum-based strategy for memecoin trading."""
    
    def __init__(self, lookback_period: int = 5, threshold: float = 0.05, profit_target: float = 0.5, stop_loss: float = 0.2):
        """Initialize with lookback period, threshold, and trade parameters.
        
        Args:
            lookback_period: Number of periods to check for price change.
            threshold: Percentage price increase required to trigger a buy.
            profit_target: Percentage gain to trigger a sell.
            stop_loss: Percentage loss to trigger a sell.
        """
        self.lookback_period = lookback_period
        self.threshold = threshold
        self.profit_target = profit_target
        self.stop_loss = stop_loss
    
    def generate_signals(self, data: pd.DataFrame, entry_price: float = None) -> dict:
        """Generate buy/sell signals based on momentum and trade parameters.
        
        Args:
            data: DataFrame with 'close' prices.
            entry_price: Entry price for tracking profit/loss (optional).
        
        Returns:
            Dictionary with 'buy' (True/False) and 'sell' (True/False).
        """
        signals = {"buy": False, "sell": False}
        if len(data) < self.lookback_period:
            return signals
        recent_change = (data['close'].iloc[-1] - data['close'].iloc[-self.lookback_period]) / data['close'].iloc[-self.lookback_period]
        signals["buy"] = recent_change > self.threshold
        if entry_price:
            current_price = data['close'].iloc[-1]
            profit = (current_price - entry_price) / entry_price
            signals["sell"] = profit >= self.profit_target or profit <= -self.stop_loss
        return signals