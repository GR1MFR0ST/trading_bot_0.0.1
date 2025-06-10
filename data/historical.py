import requests
import pandas as pd
from config import Config
import logging

logger = logging.getLogger(__name__)

class HistoricalDataFetcher:
    """Fetches historical market data from CoinGecko."""
    
    def __init__(self, config: Config):
        """Initialize fetcher with configuration.
        
        Args:
            config: Config object with API settings.
        """
        self.config = config
        self.base_url = "https://api.coingecko.com/api/v3"
    
    def get_data(self, asset: str) -> pd.DataFrame:
        """Fetch historical data for an asset.
        
        Args:
            asset: Asset symbol (e.g., 'bitcoin').
        
        Returns:
            DataFrame with historical price data.
        """
        endpoint = f"/coins/{asset}/market_chart"
        params = {
            "vs_currency": self.config.VS_CURRENCY,
            "days": 365,
            "interval": "daily"
        }
        try:
            response = requests.get(self.base_url + endpoint, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            df = pd.DataFrame(data["prices"], columns=["timestamp", "close"])
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            df.set_index("timestamp", inplace=True)
            df["high"] = df["close"]  # Simplified, real data would include high/low
            df["low"] = df["close"]
            logger.info("Fetched historical data for %s: %d records", asset, len(df))
            return df
        except requests.RequestException as e:
            logger.error("Failed to fetch historical data for %s: %s", asset, e)
            return pd.DataFrame()