import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from .base import Strategy

class MLStrategy(Strategy):
    """Machine learning-based trading strategy."""
    
    def __init__(self):
        """Initialize the ML model."""
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.is_trained = False
    
    def train(self, features: pd.DataFrame, target: pd.Series):
        """Train the ML model.
        
        Args:
            features: DataFrame of input features.
            target: Series of target labels (e.g., 1 for buy, 0 for hold/sell).
        """
        self.model.fit(features, target)
        self.is_trained = True
    
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """Generate signals using the trained ML model.
        
        Args:
            data: DataFrame with features.
        
        Returns:
            Series of boolean signals (True for buy, False for no action).
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before generating signals.")
        # Simplified feature engineering
        features = data[['close']].pct_change().dropna()
        predictions = self.model.predict(features)
        return pd.Series(predictions, index=features.index).astype(bool)