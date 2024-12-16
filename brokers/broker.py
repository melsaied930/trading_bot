# brokers/broker.py
import yaml
from ib_insync import IB, Stock


class Broker:
    def __init__(self, config_file="config/config.yaml"):
        self.ib = IB()
        self.host = None
        self.port = None
        self.client_id = None
        self.timeout = None
        self.load_config(config_file)

    def load_config(self, config_file):
        with open(config_file, "r") as file:
            config = yaml.safe_load(file)
            broker_config = config['broker']
            self.host = broker_config.get('host')
            self.port = broker_config.get('port')
            self.client_id = broker_config.get('client_id')
            self.timeout = broker_config.get('timeout')

    def connect(self):
        self.ib.connect(self.host, self.port, self.client_id, self.timeout)

    def get_historical_data(self, symbol, exchange, currency, end_date, duration, bar_size, what_to_show, use_rth):
        contract = Stock(symbol, exchange, currency)

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
                raise ValueError("No historical data received.")
            return bars

        except Exception as e:
            raise RuntimeError(f"Failed to fetch historical data: {e}")
