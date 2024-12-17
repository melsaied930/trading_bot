# data/data_fetcher.py

from brokers.broker import Broker
import pandas as pd
from pathlib import Path
from utils.config_loader import load_config
from datetime import datetime, timedelta


class DataFetcher:
    def __init__(self, config_file: str | Path = None):
        base_dir = Path(__file__).parent
        config_file = config_file or base_dir / "../config/config.yaml"

        self.broker: Broker = Broker(config_file)
        self.data_config: dict = load_config(config_file)['data_fetcher']
        self.broker.connect()

    def download_historical_data(
            self, stock_symbol: str, exchange: str, currency: str, start_date: str, end_date: str,
            duration: str = "1 D", bar_size: str = "1 min", what_to_show: str = "TRADES", use_rth: bool = False
    ) -> pd.DataFrame:
        all_data = []

        current_date = datetime.strptime(end_date, "%Y-%m-%d")
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")

        while current_date >= start_date_obj:
            try:
                bars = self.broker.get_historical_data(
                    symbol=stock_symbol,
                    exchange=exchange,
                    currency=currency,
                    end_date=current_date.strftime("%Y%m%d %H:%M:%S"),
                    duration=duration,
                    bar_size=bar_size,
                    what_to_show=what_to_show,
                    use_rth=use_rth
                )

                if not bars:
                    print(f"No historical data for {stock_symbol} on {current_date.strftime('%Y-%m-%d')}.")
                    break

                data = pd.DataFrame([bar.__dict__ for bar in bars])
                all_data.append(data)
                print(f"Downloaded {len(data)} records for {stock_symbol} on {current_date.strftime('%Y-%m-%d')}.")

                # Move to the previous day
                current_date -= timedelta(days=1)

            except Exception as e:
                print(f"Error downloading historical data on {current_date.strftime('%Y-%m-%d')}: {e}")
                break

        if not all_data:
            return pd.DataFrame()

        # Combine all data and remove duplicates
        combined_data = pd.concat(all_data, ignore_index=True).drop_duplicates()
        combined_data.sort_values(by="date", inplace=True)
        return combined_data


if __name__ == "__main__":
    data_fetcher = DataFetcher()

    selected_symbol = data_fetcher.data_config['default_symbol']
    selected_exchange = data_fetcher.data_config['exchange']
    selected_currency = data_fetcher.data_config['currency']
    selected_start_date = "2024-01-01"
    selected_end_date = "2024-12-17"

    historical_data = data_fetcher.download_historical_data(
        stock_symbol=selected_symbol,
        exchange=selected_exchange,
        currency=selected_currency,
        start_date=selected_start_date,
        end_date=selected_end_date,
        duration="1 D",
        bar_size="1 min"
    )

    if not historical_data.empty:
        output_dir = Path(__file__).parent / data_fetcher.data_config['output_dir']
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / f"{selected_symbol}_data_{selected_start_date}_to_{selected_end_date}.csv"
        historical_data.to_csv(str(output_file), index=False)
        print(f"Data saved to {output_file}.")
