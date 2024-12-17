import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging
from datetime import datetime

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Backtester:
    def __init__(self, data, start_time="08:30:00", end_time="14:59:00", initial_balance=100000, commission_rate=0.0005, max_trade_risk=0.01):
        self.data = data
        self.data['timestamp'] = pd.to_datetime(self.data['Date'] + ' ' + self.data['Time'])
        self.data.set_index('timestamp', inplace=True)
        self.start_time = start_time
        self.end_time = end_time
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.positions = []
        self.trade_log = []
        self.commission_rate = commission_rate
        self.max_trade_risk = max_trade_risk
        self.calculate_bollinger_bands()

    def calculate_bollinger_bands(self, window=20):
        self.data['MA'] = self.data['Close'].rolling(window).mean()
        self.data['STD'] = self.data['Close'].rolling(window).std()
        self.data['Upper'] = self.data['MA'] + 2 * self.data['STD']
        self.data['Lower'] = self.data['MA'] - 2 * self.data['STD']

    def simulate(self):
        for date, day_data in self.data.groupby(self.data.index.date):
            logging.info(f"Starting backtest for {date}")
            try:
                self.trade_day(day_data)
                self.close_all_positions(day_data.index[-1])
                logging.info(f"Ending balance for {date}: {self.balance}")
            except KeyError as e:
                logging.error(f"KeyError encountered on {date}: {e}")

    def trade_day(self, day_data):
        intraday_data = day_data.between_time(self.start_time, self.end_time)
        for timestamp, row in intraday_data.iterrows():
            self.check_signals(timestamp, row)

    def check_signals(self, timestamp, row):
        if row['Close'] <= row['Lower'] and not any(p['side'] == "BUY" for p in self.positions):
            position_size = self.calculate_position_size(row['Close'])
            if position_size > 0:
                self.open_position(timestamp, row['Close'], "BUY", position_size, row['Lower'], row['MA'])

        if row['Close'] >= row['Upper'] and not any(p['side'] == "SELL" for p in self.positions):
            position_size = self.calculate_position_size(row['Close'])
            if position_size > 0:
                self.open_position(timestamp, row['Close'], "SELL", position_size, row['Upper'], row['MA'])

        for position in self.positions[:]:
            if position['side'] == "BUY" and (row['Close'] >= position['target_price'] or row['Close'] <= position['stop_loss']):
                self.close_position(timestamp, row['Close'], position)
            if position['side'] == "SELL" and (row['Close'] <= position['target_price'] or row['Close'] >= position['stop_loss']):
                self.close_position(timestamp, row['Close'], position)

    def calculate_position_size(self, price):
        max_risk = self.balance * self.max_trade_risk  # 1% of current balance
        position_size = int(max_risk / (price * self.commission_rate))
        if position_size * price * (1 + self.commission_rate) > self.balance:
            return 0  # Avoid opening positions larger than available balance
        return max(position_size, 1)

    def open_position(self, timestamp, price, side, size, stop_loss, target_price):
        commission = size * price * self.commission_rate
        total_cost = size * price + commission
        if total_cost > self.balance:
            logging.warning(f"Insufficient funds to open position at {price}. Skipping...")
            return
        self.positions.append({
            "entry_time": timestamp,
            "price": price,
            "side": side,
            "size": size,
            "stop_loss": stop_loss,
            "target_price": target_price,
            "commission": commission
        })
        self.balance -= total_cost
        logging.info(f"Opened {side} position at {price} on {timestamp}, Size: {size}, Cost: {round(total_cost, 2)}, Remaining Balance: {round(self.balance, 2)}")

    def close_position(self, timestamp, close_price, position):
        commission = position['size'] * close_price * self.commission_rate
        pnl = ((close_price - position['price']) * position['size'] if position['side'] == "BUY" else (position['price'] - close_price) * position['size']) - position['commission'] - commission
        self.balance += close_price * position['size'] - commission
        self.trade_log.append({
            "entry_time": position['entry_time'],
            "exit_time": timestamp,
            "entry_price": position['price'],
            "exit_price": close_price,
            "size": position['size'],
            "pnl": round(pnl, 2),
            "commission": round(position['commission'] + commission, 2)
        })
        logging.info(f"Closed {position['side']} position from {position['entry_time']} at {close_price}. PnL: {round(pnl, 2)} (Total Commission: {round(position['commission'] + commission, 2)})")
        self.positions.remove(position)

    def close_all_positions(self, timestamp):
        for position in self.positions[:]:
            close_price = self.data.loc[timestamp, 'Close']
            self.close_position(timestamp, close_price, position)

    def report(self):
        if not self.trade_log:
            logging.error("No trades were executed.")
            return

        results = pd.DataFrame(self.trade_log)
        total_pnl = results['pnl'].sum()
        max_drawdown = results['pnl'].cumsum().min()
        win_rate = (results['pnl'] > 0).mean() * 100
        sharpe_ratio = results['pnl'].mean() / results['pnl'].std() if results['pnl'].std() != 0 else 0

        logging.info(f"Final Balance: {round(self.balance, 2)}")
        logging.info(f"Total PnL: {round(total_pnl, 2)}")
        logging.info(f"Maximum Drawdown: {round(max_drawdown, 2)}")
        logging.info(f"Win Rate: {round(win_rate, 2)}%")
        logging.info(f"Sharpe Ratio: {round(sharpe_ratio, 2)}")

        if not results.empty:
            results['pnl'].cumsum().plot(title="Cumulative PnL", figsize=(10, 6))
            plt.show()

# Example Usage
# Load your historical data assuming a CSV file format
data = pd.read_csv("historical_data.csv")

# Initialize and run backtest
backtester = Backtester(data)
backtester.simulate()
backtester.report()
