# data/data_fetcher.py

from brokers.broker import Broker
import pandas as pd
from pathlib import Path
from utils.config_loader import load_config


class DataFetcher:
    def __init__(self, config_file: str | Path = None):
        base_dir = Path(__file__).parent
        config_file = config_file or base_dir / "../config/config.yaml"

        self.broker: Broker = Broker(config_file)
        self.data_config: dict = load_config(config_file)['data_fetcher']
        self.broker.connect()

    def download_historical_data(self) -> pd.DataFrame:
        try:
            bars = self.broker.get_historical_data(
                symbol=self.data_config['default_symbol'],
                exchange=self.data_config['exchange'],
                currency=self.data_config['currency'],
                end_date=self.data_config['end_date'],
                duration=self.data_config['duration'],
                bar_size=self.data_config['bar_size'],
                what_to_show=self.data_config['what_to_show'],
                use_rth=self.data_config['use_rth']
            )

            if not bars:
                print(f"No historical data for {self.data_config['default_symbol']}.")
                return pd.DataFrame()

            df = pd.DataFrame([bar.__dict__ for bar in bars])
            print(f"Downloaded {len(df)} records for {self.data_config['default_symbol']}.")
            return df

        except Exception as e:
            print(f"Error downloading historical data: {e}")
            return pd.DataFrame()

if __name__ == "__main__":
    data_fetcher = DataFetcher()
    historical_data = data_fetcher.download_historical_data()

    if not historical_data.empty:
        output_dir = Path(__file__).parent / data_fetcher.data_config['output_dir']
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / f"{data_fetcher.data_config['default_symbol']}_historical_data.csv"
        historical_data.to_csv(str(output_file), index=False)
        print(f"Data saved to {output_file}.")
