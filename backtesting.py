import backtrader as bt

class Backtester:
    def __init__(self):
        self.cerebro = bt.Cerebro()
        self.cerebro.broker.set_cash(10000.0)
        self.cerebro.broker.setcommission(commission=0.000005)  # Base Solana fee
        self.cerebro.broker.set_slippage(perc=0.005)  # 0.5% slippage

    def run(self, data, strategy):
        class BTStrategy(bt.Strategy):
            def __init__(self):
                self.strategy = strategy
                self.signals = self.strategy.generate_signals(data)
                self.signal_idx = 0

            def next(self):
                if self.signal_idx < len(self.signals) and self.signals.iloc[self.signal_idx]:
                    self.buy(size=0.1)
                self.signal_idx += 1

        bt_data = bt.feeds.PandasData(dataname=data)
        self.cerebro.adddata(bt_data)
        self.cerebro.addstrategy(BTStrategy)
        self.cerebro.run()
        return {"final_value": self.cerebro.broker.getvalue()}