import asyncio
import threading
from solana.rpc.async_api import AsyncClient
from solana.publickey import PublicKey
from config import Config
from data.historical import HistoricalDataFetcher
from data.realtime import RealtimeDataFetcher
from tracker import Tracker
from analyzer import Analyzer
from analysis.sentiment import SentimentStream
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class TokenMonitor:
    """Monitors trusted wallets for new token purchases and tracks those tokens."""
    
    def __init__(self, config: Config, historical_fetcher: HistoricalDataFetcher, 
                 realtime_fetcher: RealtimeDataFetcher, strategies, tracker: Tracker, analyzer: Analyzer):
        """Initialize with configuration and components.
        
        Args:
            config: Config object with API keys and settings.
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
        self.solana_client = AsyncClient(self.config.SOLANA_RPC_URL)
        self.last_signatures = {wallet: None for wallet in self.config.TRUSTED_WALLETS}
        self.tracked_tokens = set()
        self.active_positions = []
        self.sentiment_stream = SentimentStream(config, self.tracked_tokens)
        self.stream_thread = threading.Thread(target=self.sentiment_stream.filter)
        self.stream_thread.start()
    
    async def run(self):
        """Run the token monitor."""
        while True:
            await self.fetch_wallet