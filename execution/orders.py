from raydium_sdk import RaydiumSDK
from solana.publickey import PublicKey
from config import Config
import pandas as pd

class OrderExecutor:
    def __init__(self, config):
        self.config = config
        self.sdk = RaydiumSDK(rpc_endpoint="https://api.mainnet-beta.solana.com")

    async def place_order(self, token_address, side, quantity, stop_loss, data=None):
        pool_id = PublicKey(token_address)
        if data is not None:
            volatility = data['close'].pct_change().std() * 100  # Daily volatility
            adjusted_quantity = quantity / (1 + volatility)  # Reduce size if volatile
        else:
            adjusted_quantity = quantity
        amount = int(adjusted_quantity * 10**6)
        tx = await self.sdk.swap(
            pool_id=pool_id,
            amount=amount,
            side=side.upper(),
            slippage_bps=50,
            priority_fee="high"
        )
        return tx.signature