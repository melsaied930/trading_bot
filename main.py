# # main.py
# import logging
#
# import yaml
#
# from brokers.broker import Broker
# from logs.logger_manager import LoggerManager
#
#
# def load_config(config_file="config/config.yaml"):
#     with open(config_file, "r") as file:
#         return yaml.safe_load(file)
#
#
# def execute():
#     config = load_config()
#     broker = Broker(config_file="config/config.yaml")
#     logger = LoggerManager()
#     try:
#         broker.connect()
#         request_config = config['request']
#         watchlist = request_config['watchlist']
#         for symbol in watchlist:
#             bars = broker.get_historical_data(
#                 symbol=symbol,
#                 exchange=request_config['exchange'],
#                 currency=request_config['currency'],
#                 end_date=request_config['end_date'],
#                 duration=request_config['duration'],
#                 bar_size=request_config['bar_size'],
#                 what_to_show=request_config['what_to_show'],
#                 use_rth=request_config['use_rth']
#             )
#             if not bars:
#                 raise RuntimeError(f"No data received for {symbol}. Please check the request parameters.")
#             file_name = f"logs/{symbol}_{request_config['duration'].replace(' ', '-')}_{request_config['end_date'].split(' ')[0]}_{request_config['bar_size'].replace(' ', '-')}.csv"
#             logger.log_and_save_data(bars, file_name)
#             logging.info(f"Data for {symbol} saved to {file_name}")
#     except Exception as e:
#         logging.error(f"Error occurred: {e}")
#
#
# if __name__ == "__main__":
#     execute()


import logging
from datetime import datetime, timedelta
from brokers.broker import Broker
from logs.logger_manager import LoggerManager

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/request_data.log"),
        logging.StreamHandler()
    ]
)


def execute():
    # Hardcoded broker and request settings
    broker = Broker()
    logger = LoggerManager()

    watchlist = ["AAPL", "MSFT", "NVDA"]  # Symbols to request
    # watchlist = ["AAPL"]  # Symbols to request
    exchange = "SMART"
    currency = "USD"
    bar_size = "1 min"
    what_to_show = "TRADES"
    use_rth = False

    combined_file_name = "logs/data3/combined_data.csv"

    try:
        broker.connect()

        for symbol in watchlist:
            # Start 2 years back from the current date
            current_date = datetime.now()
            start_date = current_date - timedelta(days=65)

            while start_date < current_date:
                # Calculate end date for each month
                end_date = start_date + timedelta(days=30)

                # Correct IBKR date format: yyyymmdd hh:mm:ss UTC
                end_date_str = end_date.strftime("%Y%m%d %H:%M:%S UTC")

                logging.info(f"Requesting {symbol} data ending at {end_date_str}...")

                # Corrected historical data request
                bars = broker.get_historical_data(
                    symbol=symbol,
                    exchange=exchange,
                    currency=currency,
                    end_date=end_date_str,
                    duration="1 M",
                    bar_size=bar_size,
                    what_to_show=what_to_show,
                    use_rth=use_rth
                )

                if not bars:
                    logging.warning(f"No data received for {symbol} ending at {end_date_str}.")
                else:
                    logger.log_and_save_data(bars, combined_file_name, append=True)
                    logging.info(f"Data for {symbol} ending at {end_date_str} saved.")

                # Move to the next month
                start_date = end_date

        logging.info(f"All data saved to {combined_file_name}")

    except Exception as e:
        logging.error(f"Error occurred: {e}")


if __name__ == "__main__":
    execute()
