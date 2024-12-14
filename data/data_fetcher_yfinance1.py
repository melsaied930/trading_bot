import quandl
import pandas as pd
from datetime import datetime, timedelta

# Define API key (replace with your actual API key)
quandl.ApiConfig.api_key = "YOUR_API_KEY_HERE"

# Define stock symbol and date range
stock_symbol = "AAPL.US"  # Correct format for the EOD dataset
start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
end_date = datetime.now().strftime("%Y-%m-%d")

try:
    # Fetch historical data from EOD
    data = quandl.get(f"EOD/{stock_symbol}", start_date=start_date, end_date=end_date)
    print(data)

    # Ensure data is not empty
    if data.empty:
        print("No data returned from Quandl.")
    else:
        # Reset index
        data.reset_index(inplace=True)

        # Select and format columns if available
        required_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        available_columns = [col for col in required_columns if col in data.columns]

        # Save to CSV if columns exist
        if available_columns:
            csv_file = f"{stock_symbol}_quandl_data.csv"
            data[available_columns].to_csv(csv_file, index=False)

            print(f"Formatted historical data for {stock_symbol} saved to {csv_file}")
            print(data[available_columns])
        else:
            print("Required columns not found in the fetched data.")

except Exception as e:
    print(f"Failed to fetch data: {e}")
