import pandas as pd
from data.realtime import RealtimeDataFetcher
import asyncio
import logging
import time

logger = logging.getLogger(__name__)

class Tracker:
    """Tracks tokens in real-time and determines when they are 'dead'."""
    
    def __init__(self, data_fetcher: RealtimeDataFetcher):
        """Initialize with a real-time data fetcher.
        
        Args:
            data_fetcher: Instance of RealtimeDataFetcher.
        """
        self.data_fetcher = data_fetcher
    
    def is_token_dead(self, data: pd.DataFrame) -> bool:
        """Determine if the token is 'dead' based on activity and volume.
        
        Args:
            data: DataFrame with recent token data.
        
        Returns:
            True if the token is considered dead, False otherwise.
        """
        if data.empty:
            return True
        last_timestamp = data.index[-1]
        no_activity = (pd.Timestamp.now() - last_timestamp).total_seconds() > 3600
        volume_ma = data['volume'].rolling(window=24).mean().iloc[-1]
        low_volume = volume_ma < 10
        price_change = (data['close'].iloc[-1] - data['close'].iloc[-24]) / data['close'].iloc[-24] if len(data) >= 24 else 0
        stable_price = abs(price_change) < 0.01
        return no_activity or (low_volume and stable_price)
    
    async def track_token(self, token_address: str, strategies, duration_hours: int, entry_price: float = None):
        """Track the token and simulate trades.
        
        Args:
            token_address: Token mint address.
            strategies: List of strategy instances.
            duration_hours: Maximum hours to track.
            entry_price: Entry price for tracking profit/loss (optional).
        
        Returns:
            List of trades executed during tracking.
        """
        start_time = time.time()
        trades = []
        data_history = pd.DataFrame()
        while time.time() - start_time < duration_hours * 3600:
            data = self.data_fetcher.get_data(token_address)
            if not data.empty:
                data_history = pd.concat([data_history, data])
                for strategy in strategies:
                    signals = strategy.generate_signals(data_history, entry_price)
                    if signals["buy"] and not entry_price:
                        entry_price = data['close'].iloc[-1]
                        trades.append({"time": time.time(), "action": "buy", "price": entry_price})
                        logger.info("Simulated buy for %s at $%.4f", token_address, entry_price)
                    elif signals["sell"] and entry_price:
                        trades.append({"time": time.time(), "action": "sell", "price": data['close'].iloc[-1]})
                        logger.info("Simulated sell for %s at $%.4f", token_address, data['close'].iloc[-1])
                        break
                if self.is_token_dead(data_history):
                    logger.info("Token %s appears dead. Stopping tracking.", token_address)
                    break
            await asyncio.sleep(60)
        return trades