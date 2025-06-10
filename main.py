import argparse
import asyncio
import logging
from config import Config
from data.historical import HistoricalDataFetcher
from data.realtime import RealtimeDataFetcher
from strategies.momentum_strategy import MomentumStrategy
from tracker import Tracker
from analyzer import Analyzer
from token_monitor import TokenMonitor
import pandas as pd
import backtrader as bt

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

async def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Solana Memecoin Trading Bot")
    parser.add_argument("--ca", help="Token Contract Address (optional for monitoring)")
    parser.add_argument("--strategies", nargs="+", default=["momentum"], help="List of strategies")
    parser.add_argument("--track-hours", type=int, default=24, help="Hours to track tokens")
    args = parser.parse_args()

    # Initialize components
    config = Config()
    historical_fetcher = HistoricalDataFetcher(config)
    realtime_fetcher = RealtimeDataFetcher(config)
    strategies = [MomentumStrategy()] if "momentum" in args.strategies else []
    tracker = Tracker(realtime_fetcher)
    analyzer = Analyzer()
    monitor = TokenMonitor(config, historical_fetcher, realtime_fetcher, strategies, tracker, analyzer)

    if args.ca:
        # Single token mode
        historical_data = historical_fetcher.get_data(args.ca)
        if historical_data.empty:
            logger.error("No historical data for token %s", args.ca)
            return
        backtest_profit = await monitor.backtest_token(args.ca, historical_data, strategies[0])
        logger.info("Backtest profit for %s: $%.2f", args.ca, backtest_profit)
        trades = await tracker.track_token(args.ca, strategies, args.track_hours)
        metrics = analyzer.calculate_metrics(trades, backtest_profit)
        suggestions = analyzer.suggest_improvements(metrics)
        logger.info("Metrics: %s", metrics)
        logger.info("Suggestions: %s", suggestions)
        # Update strategy parameters
        analyzer.update_strategy(strategies[0], metrics)
    else:
        # Monitor new tokens
        await monitor.run()

if __name__ == "__main__":
    asyncio.run(main())