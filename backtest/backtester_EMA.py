import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the CSV file into a DataFrame
file_path = '../data/data/AAPL_data_2024-01-01_to_2024-12-17.csv'  # Replace with your CSV file path
data = pd.read_csv(file_path, parse_dates=['date'])

data.set_index('date', inplace=True)

# Calculate the 200 EMA
data['EMA200'] = data['close'].ewm(span=200, adjust=False).mean()

# Define trading conditions
data['Long'] = (data['close'].shift(1) > data['EMA200'].shift(1)) & (data['open'] > data['EMA200'])
data['Short'] = (data['close'].shift(1) < data['EMA200'].shift(1)) & (data['open'] < data['EMA200'])

data['Position'] = np.where(data['Long'], 1, np.where(data['Short'], -1, 0))

data['Position'] = data['Position'].replace(to_replace=0, method='ffill').fillna(0)

# Calculate returns
data['Market_Return'] = data['close'].pct_change()
data['Strategy_Return'] = data['Market_Return'] * data['Position'].shift(1)

# Calculate cumulative returns
data['Cumulative_Market_Return'] = (1 + data['Market_Return']).cumprod() - 1
data['Cumulative_Strategy_Return'] = (1 + data['Strategy_Return']).cumprod() - 1

# Plot the results
plt.figure(figsize=(14, 7))
plt.plot(data.index, data['Cumulative_Market_Return'], label='Market Return')
plt.plot(data.index, data['Cumulative_Strategy_Return'], label='Strategy Return')
plt.title('Trading Strategy Backtest')
plt.xlabel('Date')
plt.ylabel('Cumulative Return')
plt.legend()
plt.show()
