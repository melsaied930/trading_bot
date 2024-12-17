# brokers/broker.py
import yaml
from ib_insync import IB, Stock

from logs.logger_manager import LoggerManager


class Broker:
    def __init__(self, config_file="config/config.yaml"):
        self.ib = IB()
        self.host = None
        self.port = None
        self.client_id = None
        self.timeout = None
        self.logger = LoggerManager()
        self.load_config(config_file)

    def load_config(self, config_file):
        with open(config_file, "r") as file:
            config = yaml.safe_load(file)
            broker_config = config['broker']
            self.host = broker_config.get('host')
            self.port = broker_config.get('port')
            self.client_id = broker_config.get('client_id')
            self.timeout = broker_config.get('timeout')
            self.logger.logger.info(f"Broker configuration loaded: {broker_config}")

    def connect(self):
        try:
            self.ib.connect(self.host, self.port, self.client_id, self.timeout)
            self.logger.logger.info(f"Connected to IBKR at {self.host}:{self.port} with client ID {self.client_id}.")
        except Exception as e:
            self.logger.logger.error(f"Failed to connect: {e}")
            raise

    def get_historical_data(self, symbol, exchange, currency, end_date, duration, bar_size, what_to_show, use_rth):
        contract = Stock(symbol, exchange, currency)
        self.logger.logger.info(f"Requesting historical data for {symbol} from {exchange} in {currency}...")

        try:
            bars = self.ib.reqHistoricalData(
                contract,
                endDateTime=end_date,
                durationStr=duration,
                barSizeSetting=bar_size,
                whatToShow=what_to_show,
                useRTH=use_rth,
                timeout=self.timeout
            )

            if not bars:
                message = f"No historical data received for {symbol}."
                self.logger.logger.warning(message)
                raise ValueError(message)

            self.logger.logger.info(f"Successfully fetched {len(bars)} bars for {symbol}.")
            return bars

        except Exception as e:
            error_message = f"Failed to fetch historical data for {symbol}: {e}"
            self.logger.logger.error(error_message)
            raise RuntimeError(error_message)
