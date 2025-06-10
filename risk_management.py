import talib as ta
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class RiskManager:
    """Manages trading risk with dynamic sizing and stop-loss."""
    
    def __init__(self, max_drawdown: float = 0.2, risk_per_trade: float = 0.01):
        """Initialize risk parameters.
        
        Args:
            max_drawdown: Maximum allowable portfolio drawdown.
            risk_per_trade: Risk percentage per trade.
        """
        self.max_drawdown = max_drawdown
        self.risk_per_trade = risk_per_trade
    
    def calculate_position_size(self, capital: float, atr: float) -> float:
        """Calculate position size based on risk and volatility.
        
        Args:
            capital: Current portfolio capital.
            atr: Average True Range for volatility.
        
        Returns:
            Position size in asset units.
        """
        if atr <= 0:
            logger.warning("ATR is zero or negative, defaulting to minimal position size.")
            return 0.01  # Minimal size to avoid division by zero
        size = (capital * self.risk_per_trade) / atr
        logger.debug("Calculated position size: %f for capital $%.2f and ATR %.4f", size, capital, atr)
        return size
    
    def set_stop_loss(self, entry_price: float, atr: float) -> float:
        """Set stop-loss level based on ATR.
        
        Args:
            entry_price: Entry price of the trade.
            atr: Average True Range for volatility.
        
        Returns:
            Stop-loss price.
        """
        stop_loss = entry_price - (atr * 2)  # 2x ATR below entry
        logger.debug("Set stop-loss at $%.2f for entry $%.2f with ATR %.4f", stop_loss, entry_price, atr)
        return stop_loss