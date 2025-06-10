import pandas as pd
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from config import Config
import logging

logger = logging.getLogger(__name__)

class HistoricalDataFetcher:
    """Fetches historical market data for Solana tokens from Bitquery."""
    
    def __init__(self, config: Config):
        """Initialize fetcher with configuration.
        
        Args:
            config: Config object with BITQUERY_API_KEY.
        """
        self.config = config
        self.bitquery_url = "[invalid url, do not cite]
        self.transport = RequestsHTTPTransport(
            url=self.bitquery_url,
            headers={"X-API-KEY": self.config.BITQUERY_API_KEY}
        )
        self.client = Client(transport=self.transport)
        logger.info("Initialized Bitquery client for historical data")
    
    def get_data(self, token_address: str, dex: str = "raydium") -> pd.DataFrame:
        """Fetch historical trade data for a Solana token.
        
        Args:
            token_address: Token mint address.
            dex: DEX name ('raydium' or 'pump').
        
        Returns:
            DataFrame with historical price and volume data.
        """
        query = gql("""
        query($token: String!, $dex: String!) {
            Solana {
                DEXTrades(
                    where: { Trade: { Currency: { MintAddress: { is: $token } }, Dex: { ProtocolName: { is: $dex } } } }
                    orderBy: { descending: Block_Time }
                    limit: { count: 1000 }
                ) {
                    Block { Time }
                    Trade { Price Amount }
                }
            }
        }
        """)
        try:
            result = self.client.execute(query, variable_values={"token": token_address, "dex": dex})
            trades = result["Solana"]["DEXTrades"]
            df = pd.DataFrame([
                {
                    "timestamp": pd.to_datetime(trade["Block"]["Time"]),
                    "close": trade["Trade"]["Price"],
                    "volume": trade["Trade"]["Amount"]
                }
                for trade in trades
            ])
            df.set_index("timestamp", inplace=True)
            logger.info("Fetched %d historical trades for token %s on %s", len(df), token_address, dex)
            return df
        except Exception as e:
            logger.error("Failed to fetch historical data for %s: %s", token_address, e)
            return pd.DataFrame()