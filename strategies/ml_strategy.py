import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from .base import Strategy
import logging

logger = logging.getLogger(__name__)

class MLStrategy(Strategy):
    """Machine learning-based trading strategy using Random Forest."""
    
    def __init__(self):
        """Initialize the ML model."""
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.is_trained = False
    
    def train(self, data: pd.DataFrame):
        """Train the ML model on historical data.
        
        Args:
            data: DataFrame with 'close', 'volume' columns and target (1 for buy, 0 for hold/sell).
        """
        try:
            features = data[['close', 'volume']].pct_change().dropna()
            target = (data['close'].shift(-1) > data['close']).astype(int)[1:]  # Buy if price increases
            self.model.fit(features, target)
            self.is_trained = True
            logger.info("Trained ML model with %d samples", len(features))
        except Exception as e:
            logger.error("Failed to train ML model: %s", e)
    
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """Generate signals using the trained ML model.
        
        Args:
            data: DataFrame with 'close', 'volume' columns.
        
        Returns:
            Series of boolean signals (True for buy, False for no action).
        """
        if not self.is_trained:
            logger.warning("Model not trained; returning empty signals")
            return pd.Series([False] * len(data), index=data.index)
        try:
            features = data[['close', 'volume']].pct_change().dropna()
            predictions = self.model.predict(features)
            signals = pd.Series(predictions, index=features.index).astype(bool)
            logger.info("Generated %d ML signals", len(signals))
            return signals
        except Exception as e:
            logger.error("Failed to generate ML signals: %s", e)
            return pd.Series([False] * len(data), index=data.index)