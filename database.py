from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import Config
import logging

logger = logging.getLogger(__name__)

Base = declarative_base()

class TradeLog(Base):
    """Database model for trade logs."""
    __tablename__ = "trades"
    id = Column(Integer, primary_key=True)
    asset = Column(String)
    side = Column(String)
    quantity = Column(Float)
    price = Column(Float)
    order_id = Column(String)
    timestamp = Column(DateTime, default=pd.Timestamp.now)

class PortfolioValue(Base):
    """Database model for portfolio value logs."""
    __tablename__ = "portfolio_values"
    id = Column(Integer, primary_key=True)
    value = Column(Float)
    timestamp = Column(DateTime, default=pd.Timestamp.now)

class DatabaseManager:
    """Manages database interactions."""
    
    def __init__(self, config: Config):
        """Initialize database connection.
        
        Args:
            config: Config object with database settings.
        """
        self.engine = create_engine(config.DATABASE_URL)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        logger.info("Database initialized with URL: %s", config.DATABASE_URL)
    
    def log_trade(self, asset: str, side: str, quantity: float, price: float, order_id: str):
        """Log a trade to the database.
        
        Args:
            asset: Asset symbol.
            side: 'buy' or 'sell'.
            quantity: Trade quantity.
            price: Trade price.
            order_id: Unique order identifier.
        """
        session = self.Session()
        trade = TradeLog(asset=asset, side=side, quantity=quantity, price=price, order_id=order_id)
        session.add(trade)
        session.commit()
        session.close()
        logger.info("Logged trade: %s - %s %f at $%.2f", asset, side, quantity, price)
    
    def log_portfolio_value(self, value: float):
        """Log portfolio value to the database.
        
        Args:
            value: Current portfolio value.
        """
        session = self.Session()
        portfolio_value = PortfolioValue(value=value)
        session.add(portfolio_value)
        session.commit()
        session.close()
        logger.debug("Logged portfolio value: $%.2f", value)