from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from solana.rpc.async_api import AsyncClient
from solana.publickey import PublicKey
import pandas as pd

class HistoricalDataFetcher:
    def __init__(self, config):
        self.config = config
        self.bitquery_url = "https://graphql.bitquery.io"
        self.transport = RequestsHTTPTransport(
            url=self.bitquery_url,
            headers={"X-API-KEY": config.BITQUERY_API_KEY}
        )
        self.client = Client(transport=self.transport)
        self.solana_client = AsyncClient("https://api.mainnet-beta.solana.com")

    def get_data(self, token_address, dex="raydium"):
        if dex in ["raydium", "pumpfun"]:
            return self._get_bitquery_data(token_address, dex)
        elif dex == "photon":
            return self._get_photon_data(token_address)
        else:
            raise ValueError(f"Unsupported DEX: {dex}")

    def _get_bitquery_data(self, token_address, dex):
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
        result = self.client.execute(query, variable_values={"token": token_address, "dex": dex})
        trades = result["Solana"]["DEXTrades"]
        df = pd.DataFrame([
            {
                "timestamp": pd.to_datetime(trade["Block"]["Time"]),
                "close": trade["Trade"]["Price"],
                "high": trade["Trade"]["Price"],
                "low": trade["Trade"]["Price"],
                "volume": trade["Trade"]["Amount"]
            }
            for trade in trades
        ])
        df.set_index("timestamp", inplace=True)
        return df

    async def _get_photon_data(self, token_address):
        token_pubkey = PublicKey(token_address)
        signatures = await self.solana_client.get_signatures_for_address(token_pubkey, limit=100)
        data = []
        for sig in signatures["result"]:
            tx = await self.solana_client.get_transaction(sig["signature"])
            if tx["result"]:
                amount = tx["result"]["meta"]["postTokenBalances"][0]["uiTokenAmount"]["uiAmount"] if tx["result"]["meta"]["postTokenBalances"] else 0
                data.append({
                    "timestamp": pd.to_datetime(sig["blockTime"], unit="s"),
                    "close": amount,
                    "high": amount,
                    "low": amount,
                    "volume": amount
                })
        df = pd.DataFrame(data)
        df.set_index("timestamp", inplace=True)
        return df