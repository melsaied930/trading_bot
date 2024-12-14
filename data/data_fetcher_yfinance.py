import yfinance as yf
from datetime import datetime, timedelta

stock_symbol = "AAPL"

end_date = datetime.now().date()
start_date = end_date - timedelta(days=7)
data = yf.download(stock_symbol, start=start_date, end=end_date, interval="1m")

data[['Open', 'High', 'Low', 'Close']] = data[['Open', 'High', 'Low', 'Close']].round(2)
data['Volume'] = data['Volume'].astype(int)

data.reset_index(inplace=True)
data = data[['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']]
data.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']

print(data)

csv_file = f"{stock_symbol}_1m_historical_data.csv"
data.to_csv(csv_file, index=False, header=True)
