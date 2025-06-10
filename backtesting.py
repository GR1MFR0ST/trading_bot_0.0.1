import backtrader as bt
import pandas as pd
from strategies.ma_crossover import MACrossoverStrategy
import logging

logger = logging.getLogger(__name__)

class Backtester:
    """Backtests trading strategies."""
    
    def __init__(self):
        """Initialize backtester."""
        self.cerebro = bt.Cerebro()
    
    def run(self, data: pd.DataFrame, strategy: MACrossoverStrategy) -> dict:
        """Run backtest on historical data.
        
        Args:
            data: DataFrame with 'close', 'high', 'low' columns.
            strategy: Strategy instance to test.
        
        Returns:
            Dictionary with backtest results.
        """
        class BTStrategy(bt.Strategy):
            def __init__(self):
                self.strategy = strategy
                self.signals = self.strategy.generate_signals(pd.DataFrame({
                    "close": self.data.close.array,
                    "high": self.data.high.array,
                    "low": self.data.low.array
                }))
                self.signal_idx = 0
            
            def next(self):
                if self.signal_idx < len(self.signals) and self.signals.iloc[self.signal_idx]:
                    self.buy()
                self.signal_idx += 1
        
        # Prepare data
        bt_data = bt.feeds.PandasData(dataname=data)
        self.cerebro.adddata(bt_data)
        self.cerebro.addstrategy(BTStrategy)
        self.cerebro.broker.setcash(10000.0)
        self.cerebro.run()
        
        final_value = self.cerebro.broker.getvalue()
        logger.info("Backtest completed with final value: $%.2f", final_value)
        return {"final_value": final_value}