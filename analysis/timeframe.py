import pandas as pd
from analysis.technical import TechnicalAnalyzer
import logging

logger = logging.getLogger(__name__)

class TimeframeAnalyzer:
    """Analyzes data across multiple timeframes."""
    
    def __init__(self):
        """Initialize technical analyzer."""
        self.technical = TechnicalAnalyzer()
    
    def analyze(self, data: pd.DataFrame, timeframes: list = ["1h", "4h", "1d"]) -> dict:
        """Analyze data across specified timeframes.
        
        Args:
            data: DataFrame with price data.
            timeframes: List of timeframes to analyze (e.g., '1h', '4h', '1d').
        
        Returns:
            Dictionary of analysis results per timeframe.
        """
        results = {}
        for tf in timeframes:
            resampled = data.resample(tf).agg({"close": "last", "high": "max", "low": "min"}).dropna()
            results[tf] = {
                "atr": self.technical.calculate_atr(resampled),
                "rsi": self.technical.calculate_rsi(resampled)
            }
            logger.info("Analyzed timeframe %s for %d records", tf, len(resampled))
        return results