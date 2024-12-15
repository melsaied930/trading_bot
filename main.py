# main.py
import logging
from datetime import datetime
from brokers.broker import Broker
from logs.logger_manager import LoggerManager

def execute():
    broker = Broker()
    logger = LoggerManager()

    try:
        broker.connect()
        bars = broker.get_historical_data(
            symbol='AAPL',
            exchange='SMART',
            currency='USD',
            end_date='',
            duration='8 D',
            bar_size='1 min',
            what_to_show='TRADES',
            use_rth=True
        )

        current_date = datetime.now().strftime("%Y-%m-%d")
        file_name = f"logs/AAPL_{current_date}_1m.csv"
        logger.log_and_save_data(bars, file_name)
        logging.info(f"Data saved to {file_name}")
    except Exception as e:
        logging.error(f"Error occurred: {e}")

if __name__ == "__main__":
    execute()
