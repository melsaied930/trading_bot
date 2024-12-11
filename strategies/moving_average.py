import pandas as pd
from strategies.base_strategy import BaseStrategy

class MovingAverageStrategy(BaseStrategy):
    def __init__(self, short_window=5, long_window=20):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, data: pd.DataFrame):
        data['SMA_Short'] = data['close'].rolling(window=self.short_window).mean()
        data['SMA_Long'] = data['close'].rolling(window=self.long_window).mean()

        # Ensure conversion is done using Pandas DataFrame structure
        data['Signal'] = pd.Series(data['SMA_Short'] > data['SMA_Long'], index=data.index).astype(int)

        return data
