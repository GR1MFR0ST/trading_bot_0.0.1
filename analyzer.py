import backtrader as bt
import logging

logger = logging.getLogger(__name__)

class Analyzer:
    """Analyzes backtesting results and suggests strategy improvements."""
    
    def calculate_metrics(self, trades: list, backtest_profit: float) -> dict:
        """Calculate key performance metrics from backtesting and tracking.
        
        Args:
            trades: List of trades from real-time tracking.
            backtest_profit: Profit from backtesting.
        
        Returns:
            Dictionary with performance metrics.
        """
        win_rate = sum(1 for i in range(0, len(trades)-1, 2) if trades[i+1]["price"] > trades[i]["price"]) / (len(trades)//2) if trades else 0
        tracking_profit = sum(t["price"] * 0.1 * (-1 if t["action"] == "sell" else 1) for t in trades)
        return {
            "win_rate": win_rate,
            "tracking_profit": tracking_profit,
            "backtest_profit": backtest_profit
        }
    
    def suggest_improvements(self, metrics: dict) -> list:
        """Provide suggestions based on performance metrics.
        
        Args:
            metrics: Dictionary with performance metrics.
        
        Returns:
            List of improvement suggestions.
        """
        suggestions = []
        if metrics["win_rate"] < 0.5:
            suggestions.append("Increase momentum threshold to improve win rate.")
        if metrics["tracking_profit"] < 100:
            suggestions.append("Adjust entry timing to capture larger price movements.")
        if metrics["backtest_profit"] < 100:
            suggestions.append("Optimize lookback period for earlier entries.")
        return suggestions
    
    def update_strategy(self, strategy, metrics: dict):
        """Dynamically update strategy parameters based on metrics.
        
        Args:
            strategy: Strategy instance to update.
            metrics: Performance metrics.
        """
        if metrics["win_rate"] < 0.5:
            strategy.threshold += 0.01
            logger.info("Increased momentum threshold to %.2f", strategy.threshold)
        if metrics["tracking_profit"] < 100:
            strategy.lookback_period = max(3, strategy.lookback_period - 1)
            logger.info("Reduced lookback period to %d", strategy.lookback_period)