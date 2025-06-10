from typing import Dict
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class Portfolio:
    """Manages trading portfolio, positions, and value."""
    
    def __init__(self, initial_capital: float):
        """Initialize portfolio with starting capital.
        
        Args:
            initial_capital: Initial cash balance.
        """
        self.capital = initial_capital
        self.positions: Dict[str, float] = {}
    
    def update(self, asset: str, quantity: float, price: float):
        """Update portfolio after a trade.
        
        Args:
            asset: Asset symbol (e.g., 'bitcoin').
            quantity: Amount bought/sold (positive for buy, negative for sell).
            price: Trade price.
        """
        cost = quantity * price
        if asset in self.positions:
            self.positions[asset] += quantity
        else:
            self.positions[asset] = quantity
        self.capital -= cost
        logger.info("Portfolio updated: %s - %f units at $%.2f, new capital $%.2f", 
                    asset, quantity, price, self.capital)
    
    def calculate_value(self, prices: pd.DataFrame) -> float:
        """Calculate total portfolio value.
        
        Args:
            prices: DataFrame with latest prices ('close' column per asset).
        
        Returns:
            Total portfolio value (cash + positions).
        """
        total_value = self.capital
        for asset, quantity in self.positions.items():
            if asset in prices.columns:
                total_value += quantity * prices[asset].iloc[-1]
            else:
                logger.warning("Price data missing for %s, excluding from value calculation.", asset)
        logger.debug("Calculated portfolio value: $%.2f", total_value)
        return total_value