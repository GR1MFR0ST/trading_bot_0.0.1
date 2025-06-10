import pandas as pd

class MomentumStrategy:
    def __init__(self, lookback_period=10, threshold=0.05):
        self.lookback_period = lookback_period
        self.threshold = threshold

    def generate_signals(self, data):
        data['returns'] = data['close'].pct_change()
        data['momentum'] = data['returns'].rolling(window=self.lookback_period).mean()
        signals = (data['momentum'] > self.threshold)
        return signals