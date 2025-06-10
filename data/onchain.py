from solana.rpc.async_api import AsyncClient
from solana.publickey import PublicKey
import pandas as pd
from config import Config
import logging

logger = logging.getLogger(__name__)

class OnchainDataFetcher:
    """Fetches on-chain data from Solana blockchain."""
    
    def __init__(self, config: Config):
        """Initialize fetcher with Solana RPC client.
        
        Args:
            config: Config object with Solana RPC settings.
        """
        self.config = config
        self.client = AsyncClient("https://api.mainnet-beta.solana.com")
        logger.info("Initialized Solana RPC client")
    
    async def get_data(self, token_address: str) -> pd.DataFrame:
        """Fetch recent transaction data for a Solana token.
        
        Args:
            token_address: Token mint address.
        
        Returns:
            DataFrame with transaction data (timestamp, price, volume).
        """
        try:
            token_pubkey = PublicKey(token_address)
            signatures = await self.client.get_signatures_for_address(token_pubkey, limit=100)
            data = []
            for sig in signatures["result"]:
                tx = await self.client.get_transaction(sig["signature"])
                if tx["result"]:
                    amount = tx["result"]["meta"]["postTokenBalances"][0]["uiTokenAmount"]["uiAmount"] if tx["result"]["meta"]["postTokenBalances"] else 0
                    data.append({
                        "timestamp": pd.to_datetime(sig["blockTime"], unit="s"),
                        "close": amount,  # Simplified; needs price conversion
                        "high": amount,
                        "low": amount,
                        "volume": amount
                    })
            df = pd.DataFrame(data)
            df.set_index("timestamp", inplace=True)
            logger.info("Fetched %d on-chain transactions for %s", len(df), token_address)
            return df
        except Exception as e:
            logger.error("Failed to fetch on-chain data for %s: %s", token_address, e)
            return pd.DataFrame()