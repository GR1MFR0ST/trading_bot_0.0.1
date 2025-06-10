import asyncio
import json
import websockets
import ccxt
import pandas as pd
from config import Config
import logging

logger = logging.getLogger(__name__)

class RealtimeDataFetcher:
    """Fetches real-time market data using WebSocket."""
    def __init__(self, config: Config):
        self.config = config
        self.exchange = ccxt.binance({
            'apiKey': config.BINANCE_API_KEY,
            'secret': config.BINANCE_SECRET_KEY,
            'enableRateLimit': True,
        })

    async def get_data(self, asset: str) -> pd.DataFrame:
        """Fetch real-time data for an asset using WebSocket.
        
        Args:
            asset: Asset symbol (e.g., 'BTC/USDT').
        
        Returns:
            DataFrame with latest price data.
        """
        symbol = asset.replace('/', '').upper()  # e.g., 'BTCUSDT'
        uri = f"wss://stream.binance.com:9443/ws/{symbol.lower()}@ticker"
        async with websockets.connect(uri) as websocket:
            data = await websocket.recv()
            data = json.loads(data)
            df = pd.DataFrame([{
                "timestamp": pd.Timestamp.now(),
                "close": float(data['c']),  # Last price
                "high": float(data['h']),   # High price
                "low": float(data['l']),    # Low price
                "volume": float(data['v'])  # Volume
            }])
            df.set_index("timestamp", inplace=True)
            logger.info("Fetched real-time data for %s: $%.2f", asset, df["close"].iloc[-1])
            return df