import backtrader as bt
import logging

logger = logging.getLogger(__name__)

class Analyzer:
    """Analyzes backtesting results and suggests strategy improvements."""
    
    def calculate_metrics(self, cerebro: bt.Cerebro, trades: list) -> dict:
        """Calculate key performance metrics from backtesting and tracking.
        
        Args:
            cerebro: Backtrader Cerebro instance after running the backtest.
            trades: List of trades from real-time tracking.
        
        Returns:
            Dictionary with performance metrics.
        """
        strat = cerebro.runstrats[0][0]
        trades_bt = strat.trades
        win_rate = sum(1 for trade in trades_bt if trade.pnl > 0) / len(trades_bt) if trades_bt else 0
        max_drawdown = cerebro.runstrats[0][0].stats.drawdown.max
        trade_freq = len(trades_bt) / (cerebro.runstrats[0][0].data.datetime.date(0) - cerebro.runstrats[0][0].data.datetime.date(-1)).days
        tracking_profit = sum(t["price"] * 0.1 for t in trades if t["action"] == "buy")  # Simplified
        return {
            "win_rate": win_rate,
            "max_drawdown": max_drawdown,
            "trade_freq": trade_freq,
            "tracking_profit": tracking_profit
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
        if metrics["tracking_profit"] < 100:
            suggestions.append("Optimize entry timing to capture larger price movements.")
        return suggestions