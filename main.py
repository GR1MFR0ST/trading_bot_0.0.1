import argparse
import asyncio
import logging
from config import Config
from data.historical import HistoricalDataFetcher
from data.realtime import RealtimeDataFetcher
from strategies.momentum_strategy import MomentumStrategy
from tracker import Tracker
from analyzer import Analyzer
import backtrader as bt
import pandas as pd

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

async def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Solana Memecoin Trading Bot")
    parser.add_argument("--ca", required=True, help="Token Contract Address")
    parser.add_argument("--strategies", nargs="+", default=["momentum"], help="List of strategies (e.g., momentum)")
    parser.add_argument("--track-hours", type=int, default=24, help="Hours to track the token")
    args = parser.parse_args()

    # Initialize components
    config = Config()
    historical_fetcher = HistoricalDataFetcher(config)
    realtime_fetcher = RealtimeDataFetcher(config)
    strategies = [MomentumStrategy()] if "momentum" in args.strategies else []
    tracker = Tracker(realtime_fetcher)
    analyzer = Analyzer()

    # Fetch historical data for backtesting
    historical_data = historical_fetcher.get_data(args.ca)
    if historical_data.empty:
        logger.error("No historical data found for token %s", args.ca)
        return

    # Set up backtesting with backtrader
    cerebro = bt.Cerebro()
    cerebro.broker.set_cash(10000.0)
    cerebro.broker.setcommission(commission=0.000005)  # Solana fee
    cerebro.broker.set_slippage(perc=0.005)  # 0.5% slippage
    bt_data = bt.feeds.PandasData(dataname=historical_data)
    cerebro.adddata(bt_data)

    # Define backtesting strategy
    class BTStrategy(bt.Strategy):
        def __init__(self):
            self.strategy = strategies[0]
            self.signals = self.strategy.generate_signals(historical_data)
            self.index = 0

        def next(self):
            if self.index < len(self.signals) and self.signals.iloc[self.index]:
                self.buy(size=0.1)  # Small position for memecoins
            self.index += 1

    cerebro.addstrategy(BTStrategy)
    cerebro.run()

    # Analyze backtesting results
    metrics = analyzer.calculate_metrics(cerebro)
    suggestions = analyzer.suggest_improvements(metrics)
    logger.info("Backtesting Metrics: %s", metrics)
    logger.info("Improvement Suggestions: %s", suggestions)

    # Track token in real-time
    trades = await tracker.track_token(args.ca, strategies, args.track_hours)
    logger.info("Tracking completed. Trades executed: %d", len(trades))

if __name__ == "__main__":
    asyncio.run(main())