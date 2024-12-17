import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the CSV file into a DataFrame
file_path = '../data/data/AAPL_data_2024-01-01_to_2024-12-17.csv'  # Replace with your CSV file path
data = pd.read_csv(file_path, parse_dates=['date'], date_parser=lambda x: pd.to_datetime(x, utc=True))

# Ensure the index is a DatetimeIndex
data.set_index('date', inplace=True)

# Calculate the 200 EMA for 1-minute intervals
data['EMA200'] = data['close'].ewm(span=200, adjust=False).mean()

# Define trading conditions: Long at 8:30, close at 14:59
data['Position'] = 0

# Apply intraday position logic
intraday_data = data.between_time('08:30', '14:59')
data.loc[intraday_data.index, 'Position'] = 1

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
plt.plot(data.index, data['EMA200'], label='EMA 200', linestyle='--', color='orange')
plt.title('Intraday Long Strategy Backtest (8:30 to 14:59) with EMA 200')
plt.xlabel('Date')
plt.ylabel('Cumulative Return')
plt.legend()
plt.show()
