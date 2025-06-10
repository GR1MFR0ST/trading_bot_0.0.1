import asyncio
import json
import websockets
from solana.rpc.websocket_api import connect
from solana.publickey import PublicKey
from config import Config
from data.historical import HistoricalDataFetcher
from data.realtime import RealtimeDataFetcher
from tracker import Tracker
from analyzer import Analyzer
import pandas as pd
import requests
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class TokenMonitor:
    """Monitors new token creations on Pumpfun and Raydium, evaluates, and simulates trades."""
    
    def __init__(self, config: Config, historical_fetcher: HistoricalDataFetcher, 
                 realtime_fetcher: RealtimeDataFetcher, strategies, tracker: Tracker, analyzer: Analyzer):
        """Initialize with configuration and components.
        
        Args:
            config: Config object with API keys.
            historical_fetcher: HistoricalDataFetcher instance.
            realtime_fetcher: RealtimeDataFetcher instance.
            strategies: List of strategy instances.
            tracker: Tracker instance.
            analyzer: Analyzer instance.
        """
        self.config = config
        self.historical_fetcher = historical_fetcher
        self.realtime_fetcher = realtime_fetcher
        self.strategies = strategies
        self.tracker = tracker
        self.analyzer = analyzer
        self.raydium_program_id = PublicKey("675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8")
        self.active_positions = []
    
    async def monitor_pumpfun(self):
        """Monitor new token creations on Pumpfun via WebSocket."""
        uri = "wss://pumpportal.fun/api/data"
        try:
            async with websockets.connect(uri, extra_headers={"Authorization": f"Bearer {self.config.PUMPPORTAL_API_KEY}"}) as websocket:
                await websocket.send(json.dumps({"method": "subscribeNewToken"}))
                while True:
                    message = await websocket.recv()
                    data = json.loads(message)
                    token_address = data.get("token_address")
                    if token_address:
                        logger.info("Detected new Pumpfun token: %s", token_address)
                        await self.evaluate_token(token_address, "pump")
        except Exception as e:
            logger.error("Pumpfun monitoring failed: %s", e)
    
    async def monitor_raydium(self):
        """Monitor new pool creations on Raydium via Solana WebSocket."""
        async with connect(self.config.SOLANA_RPC_URL.replace("https", "wss")) as websocket:
            await websocket.program_subscribe(self.raydium_program_id)
            first_resp = await websocket.recv()
            subscription_id = first_resp[0].result
            while True:
                message = await websocket.recv()
                for m in message:
                    if m['method'] == 'programAccountChangeNotification':
                        account_info = m['params']['result']['value']
                        token_address = account_info['account']['data'].get('base_mint', None)
                        if token_address:
                            logger.info("Detected new Raydium token: %s", token_address)
                            await self.evaluate_token(str(token_address), "raydium")
    
    async def evaluate_token(self, token_address: str, dex: str):
        """Evaluate a new token for trading potential.
        
        Args:
            token_address: Token mint address.
            dex: DEX name ('raydium' or 'pump').
        """
        # Fetch initial data
        data = self.historical_fetcher.get_data(token_address, dex)
        if data.empty:
            logger.info("No data for token %s, skipping", token_address)
            return
        
        # Check time since creation
        creation_time = data.index[0]
        time_since_creation = (pd.Timestamp.now() - creation_time).total_seconds() / 60
        if time_since_creation > 30:
            logger.info("Token %s too old (%.2f minutes), skipping", token_address, time_since_creation)
            return
        
        # Check volume
        recent_volume = data['volume'].sum()
        if recent_volume < 100:
            logger.info("Token %s volume too low (%.2f SOL), skipping", token_address, recent_volume)
            return
        
        # Check sentiment
        sentiment_score = await self.get_sentiment(token_address)
        if sentiment_score < 10:
            logger.info("Token %s sentiment too low (%d posts), skipping", token_address, sentiment_score)
            return
        
        # Simulate buy
        current_price = self.realtime_fetcher.get_data(token_address)['close'].iloc[-1]
        self.active_positions.append({
            "token_address": token_address,
            "entry_price": current_price,
            "quantity": 0.1,
            "entry_time": datetime.now()
        })
        logger.info("Simulated buy for %s at $%.4f", token_address, current_price)
        
        # Track token
        trades = await self.tracker.track_token(token_address, self.strategies, 24, current_price)
        backtest_profit = await self.backtest_token(token_address, data, self.strategies[0])
        metrics = self.analyzer