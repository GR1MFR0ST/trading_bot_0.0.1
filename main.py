import asyncio
import logging
from config import Config
from strategies.ma_crossover import MACrossoverStrategy
from risk_management import RiskManager
from portfolio import Portfolio
from data.historical import HistoricalDataFetcher
from data.realtime import RealtimeDataFetcher
from analysis.technical import TechnicalAnalyzer
from execution.orders import OrderExecutor
from alerts import send_telegram_alert
from database import DatabaseManager

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

async def main():
    """Main function to run the trading bot."""
    config = Config()
    db_manager = DatabaseManager(config)
    historical_fetcher = HistoricalDataFetcher(config)
    realtime_fetcher = RealtimeDataFetcher(config)
    technical_analyzer = TechnicalAnalyzer()
    risk_manager = RiskManager()
    portfolio = Portfolio(config.INITIAL_CAPITAL)
    strategy = MACrossoverStrategy()
    order_executor = OrderExecutor(config)

    logger.info("Trading bot started with initial capital: $%.2f", config.INITIAL_CAPITAL)

    while True:
        try:
            for asset in config.ASSETS:
                # Fetch data
                historical_data = historical_fetcher.get_data(asset)
                realtime_data = await realtime_fetcher.get_data(asset)
                
                # Analyze data
                signals = strategy.generate_signals(historical_data)
                atr = technical_analyzer.calculate_atr(historical_data)
                
                # Trading logic
                if signals.iloc[-1]:
                    position_size = risk_manager.calculate_position_size(portfolio.capital, atr.iloc[-1])
                    stop_loss = risk_manager.set_stop_loss(realtime_data['close'].iloc[-1], atr.iloc[-1])
                    
                    # Execute trade
                    order_id = await order_executor.place_order(asset, "buy", position_size, stop_loss)
                    portfolio.update(asset, position_size, realtime_data['close'].iloc[-1])
                    
                    # Log and alert
                    db_manager.log_trade(asset, "buy", position_size, realtime_data['close'].iloc[-1], order_id)
                    send_telegram_alert(f"Bought {position_size:.4f} {asset} at ${realtime_data['close'].iloc[-1]:.2f}")
                    logger.info("Trade executed: %s - Buy %f at $%.2f", asset, position_size, realtime_data['close'].iloc[-1])
                
                # Update portfolio value (simplified)
                portfolio_value = portfolio.calculate_value(realtime_data)
                db_manager.log_portfolio_value(portfolio_value)
                
            await asyncio.sleep(config.TRADE_INTERVAL)
        except Exception as e:
            logger.error("Error in main loop: %s", e)
            send_telegram_alert(f"Bot error: {e}")
            await asyncio.sleep(60)  # Wait before retrying

if __name__ == "__main__":
    asyncio.run(main())