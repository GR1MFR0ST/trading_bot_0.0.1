import backtrader as bt
import logging

logger = logging.getLogger(__name__)

class Analyzer:
    """Analyzes backtesting results and suggests strategy improvements."""
    
    def calculate_metrics(self, cerebro: bt.Cerebro) -> dict:
        """Calculate key performance metrics from backtesting.
        
        Args:
            cerebro: Backtrader Cerebro instance after running the backtest.
        
        Returns:
            Dictionary with performance metrics.
        """
        strat = cerebro.runstrats[0][0]
        trades = strat.trades
        win_rate = sum(1 for trade in trades if trade.pnl > 0) / len(trades) if trades else 0
        max_drawdown = cerebro.runstrats[0][0].stats.drawdown.max
        trade_freq = len(trades) / (cerebro.runstrats[0][0].data.datetime.date(0) - cerebro.runstrats[0][0].data.datetime.date(-1)).days
        return {
            "win_rate": win_rate,
            "max_drawdown": max_drawdown,
            "trade_freq": trade_freq
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
            suggestions.append("Tighten entry threshold to improve win rate.")
        if metrics["max_drawdown"] > 0.2:
            suggestions.append("Reduce position sizes or adjust stop-loss to manage drawdown.")
        if metrics["trade_freq"] < 1:
            suggestions.append("Lower entry threshold to increase trade frequency.")
        return suggestions