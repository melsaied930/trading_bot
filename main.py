# main.py
import logging
import yaml
from datetime import datetime
from brokers.broker import Broker
from logs.logger_manager import LoggerManager


def load_config(config_file="config/config.yaml"):
    with open(config_file, "r") as file:
        return yaml.safe_load(file)


def execute():
    config = load_config()
    broker = Broker(config_file="config/config.yaml")
    logger = LoggerManager()
    try:
        broker.connect()
        request_config = config['request']
        watchlist = request_config['watchlist']
        for symbol in watchlist:
            bars = broker.get_historical_data(
                symbol=symbol,
                exchange=request_config['exchange'],
                currency=request_config['currency'],
                end_date=request_config['end_date'],
                duration=request_config['duration'],
                bar_size=request_config['bar_size'],
                what_to_show=request_config['what_to_show'],
                use_rth=request_config['use_rth']
            )
            if not bars:
                raise RuntimeError(f"No data received for {symbol}. Please check the request parameters.")
            file_name = f"logs/{symbol}_{request_config['duration'].replace(' ', '-')}_{request_config['end_date'].split(' ')[0]}_{request_config['bar_size'].replace(' ', '-')}.csv"
            logger.log_and_save_data(bars, file_name)
            logging.info(f"Data for {symbol} saved to {file_name}")
    except Exception as e:
        logging.error(f"Error occurred: {e}")


if __name__ == "__main__":
    execute()
