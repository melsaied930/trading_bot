from alpha_vantage.timeseries import TimeSeries
import pandas as pd

# Initialize Alpha Vantage API
api_key = 'YOUR_ALPHA_VANTAGE_API_KEY'
ts = TimeSeries(key=api_key, output_format='pandas')

# Fetch intraday data
data, meta_data = ts.get_intraday(symbol='AAPL', interval='1min', outputsize='full')

# Format and save
data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
csv_file = "AAPL_alpha_vantage_data.csv"
data.to_csv(csv_file, index=True)

print(f"Data saved to {csv_file}")
