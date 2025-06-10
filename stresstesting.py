import pandas as pd
from backtesting import Backtester
import logging

logger = logging.getLogger(__name__)

class StressTester:
    """Tests strategy resilience under extreme conditions."""
    
    def test(self, data: pd.DataFrame, strategy) -> dict:
        """Simulate a flash crash.
        
        Args:
            data: Historical data.
            strategy: Strategy instance.
        
        Returns:
            Dictionary with stress test results.
        """
        # Simulate flash crash: Drop prices by 20%
        stressed_data = data.copy()
        stressed_data["close"] *= 0.8
        stressed_data["high"] *= 0.8
        stressed_data["low"] *= 0.8
        
        backtester = Backtester()
        results = backtester.run(stressed_data, strategy)
        logger.info("Stress test completed with flash crash scenario")
        return results