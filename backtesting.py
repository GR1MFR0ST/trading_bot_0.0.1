import backtrader as bt
import pandas as pd
from strategies.ma_crossover import MACrossoverStrategy
import logging

logger = logging.getLogger(__name__)

class Backtester:
    """Backtests trading strategies with Solana memecoin data."""
    
    def __init__(self):
        """Initialize backtester."""
        self.cerebro = bt.Cerebro()
        self.cerebro.broker.set_cash(10000.0)
        self.cerebro.broker.setcommission(commission=0.000005)  # Solana fee
    
    def run(self, data: pd.DataFrame, strategy: MACrossoverStrategy) -> dict:
        """Run backtest on historical data.
        
        Args:
            data: DataFrame with 'close', 'high', 'low', 'volume' columns.
            strategy: Strategy instance to test.
        
        Returns:
            Dictionary with backtest results (profit, drawdown, trades).
        """
        class BTStrategy(bt.Strategy):
            def __init__(self):
                self.strategy = strategy
                self.signals = self.strategy.generate_signals(pd.DataFrame({
                    "close": self.data.close.array,
                    "high": self.data.high.array,
                    "low": self.data.low.array,
                    "volume": self.data.volume.array
                }))
                self.signal_idx = 0
            
            def next(self):
                if self.signal_idx < len(self.signals) and self.signals.iloc[self.signal_idx]:
                    self.buy(size=0.1)  # Small size for memecoin volatility
                self.signal_idx += 1
        
        try:
            bt_data = bt.feeds.PandasData(dataname=data)
            self.cerebro.adddata(bt_data)
            self.cerebro.addstrategy(BTStrategy)
            self.cerebro.run()
            final_value = self.cerebro.broker.getvalue()
            trades = len(self.cerebro.runstrats[0][0].trades)
            logger.info("Backtest completed with final value: $%.2f, %d trades", final_value, trades)
            return {"final_value": final_value, "trades": trades}
        except Exception as e:
            logger.error("Backtest failed: %s", e)
            return {"final_value": 0, "trades": 0}