import talib as ta
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class TechnicalAnalyzer:
    """Provides technical indicators for market analysis."""
    
    def calculate_atr(self, data: pd.DataFrame, period: int = 14) -> pd.Series:
        """Calculate Average True Range (ATR).
        
        Args:
            data: DataFrame with 'high', 'low', 'close' columns.
            period: Lookback period for ATR.
        
        Returns:
            Series with ATR values.
        """
        try:
            atr = ta.ATR(data["high"], data["low"], data["close"], timeperiod=period)
            logger.debug("Calculated ATR for %d periods", period)
            return atr
        except Exception as e:
            logger.error("Error calculating ATR: %s", e)
            return pd.Series()
    
    def calculate_rsi(self, data: pd.DataFrame, period: int = 14) -> pd.Series:
        """Calculate Relative Strength Index (RSI).
        
        Args:
            data: DataFrame with 'close' column.
            period: Lookback period for RSI.
        
        Returns:
            Series with RSI values.
        """
        try:
            rsi = ta.RSI(data["close"], timeperiod=period)
            logger.debug("Calculated RSI for %d periods", period)
            return rsi
        except Exception as e:
            logger.error("Error calculating RSI: %s", e)
            return pd.Series()