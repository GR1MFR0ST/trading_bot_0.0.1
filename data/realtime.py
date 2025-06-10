import requests
import pandas as pd
from config import Config
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import logging

logger = logging.getLogger(__name__)

class RealtimeDataFetcher:
    """Fetches real-time market data for Solana tokens using Jupiter API and Bitquery."""
    
    def __init__(self, config: Config):
        """Initialize fetcher with Jupiter API and Bitquery client.
        
        Args:
            config: Config object with BITQUERY_API_KEY.
        """
        self.jupiter_url = "https://price.jup.ag/v4/price"
        self.bitquery_url = "https://graphql.bitquery.io"
        self.transport = RequestsHTTPTransport(
            url=self.bitquery_url,
            headers={"X-API-KEY": config.BITQUERY_API_KEY}
        )
        self.client = Client(transport=self.transport)
        logger.info("Initialized Jupiter API and Bitquery for real-time data")
    
    def get_data(self, token_address: str) -> pd.DataFrame:
        """Fetch current price from Jupiter and recent volume from Bitquery.
        
        Args:
            token_address: Token mint address.
        
        Returns:
            DataFrame with latest price and volume data.
        """
        try:
            # Get price from Jupiter
            response = requests.get(f"{self.jupiter_url}?ids={token_address}")
            response.raise_for_status()
            price_data = response.json()
            price = price_data['data'][token_address]['price']
            
            # Get recent volume from Bitquery (last 1 hour)
            query = gql("""
            query($token: String!) {
                Solana {
                    DEXTrades(
                        where: { Trade: { Currency: { MintAddress: { is: $token } } }, Block: { Time: { after: "%s" } } }
                        orderBy: { descending: Block_Time }
                    ) {
                        Trade { Amount }
                    }
                }
            }
            """ % (pd.Timestamp.now() - pd.Timedelta(hours=1)).isoformat())
            result = self.client.execute(query, variable_values={"token": token_address})
            trades = result["Solana"]["DEXTrades"]
            volume = sum(trade["Trade"]["Amount"] for trade in trades)
            
            df = pd.DataFrame([{
                "timestamp": pd.Timestamp.now(),
                "close": price,
                "volume": volume
            }])
            df.set_index("timestamp", inplace=True)
            logger.info("Fetched real-time data for %s: price $%.4f, volume %.2f", token_address, price, volume)
            return df
        except Exception as e:
            logger.error("Failed to fetch real-time data for %s: %s", token_address, e)
            return pd.DataFrame()