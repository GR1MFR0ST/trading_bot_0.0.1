import asyncio
import pandas as pd
from config import Config
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import logging

logger = logging.getLogger(__name__)

class RealtimeDataFetcher:
    """Fetches real-time market data for Solana memecoins using Bitquery."""
    
    def __init__(self, config: Config):
        """Initialize fetcher with configuration.
        
        Args:
            config: Config object with API settings.
        """
        self.config = config
        self.bitquery_url = "https://graphql.bitquery.io"
        self.transport = AIOHTTPTransport(
            url=self.bitquery_url,
            headers={"X-API-KEY": config.BITQUERY_API_KEY}
        )
        self.client = Client(transport=self.transport)
        logger.info("Initialized Bitquery client for real-time data")
    
    async def get_data(self, token_address: str, dex: str = "raydium") -> pd.DataFrame:
        """Fetch real-time trade data for a Solana token.
        
        Args:
            token_address: Token mint address.
            dex: DEX name ('raydium' or 'pump').
        
        Returns:
            DataFrame with latest trade data.
        """
        query = gql("""
        subscription($token: String!, $dex: String!) {
            Solana {
                DEXTrades(
                    where: { Trade: { Currency: { MintAddress: { is: $token } }, Dex: { ProtocolName: { is: $dex } } }
                    limit: { count: 1 }
                ) {
                    Block { Time }
                    Trade { Price Amount }
                }
            }
        }
        """)
        try:
            async with self.client as session:
                result = await session.subscribe(query, variable_values={"token": token_address, "dex": dex})
                async for trade in result:
                    df = pd.DataFrame([{
                        "timestamp": pd.to_datetime(trade["Block"]["Time"]),
                        "close": trade["Trade"]["Price"],
                        "high": trade["Trade"]["Price"],
                        "low": trade["Trade"]["Price"],
                        "volume": trade["Trade"]["Amount"]
                    }])
                    df.set_index("timestamp", inplace=True)
                    logger.info("Fetched real-time trade for %s on %s: $%.2f", token_address, dex, df["close"].iloc[-1])
                    return df
        except Exception as e:
            logger.error("Failed to fetch real-time data for %s: %s", token_address, e)
            return pd.DataFrame()