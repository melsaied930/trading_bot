# brokers/broker.py

from ib_insync import IB, Stock
from logs.logger_manager import LoggerManager
from utils.config_loader import load_config
from pathlib import Path


class Broker:
    def __init__(self, config_file: str | Path = None):
        base_dir = Path(__file__).parent
        config_file = config_file or base_dir / "../config/config.yaml"

        self.ib: IB = IB()
        self.logger = LoggerManager()
        self.config: dict = load_config(config_file)
        self.host: str = self.config['broker'].get('host', "")
        self.port: int = self.config['broker'].get('port', 0)
        self.client_id: int = self.config['broker'].get('client_id', 0)
        self.timeout: int = self.config['broker'].get('timeout', 0)

        self.logger.logger.info(f"Broker configuration loaded: {self.config['broker']}")

    def connect(self) -> None:
        try:
            self.ib.connect(self.host, self.port, self.client_id, self.timeout)
            self.logger.logger.info(f"Connected to IBKR at {self.host}:{self.port} with client ID {self.client_id}.")
        except Exception as e:
            self.logger.logger.error(f"Failed to connect: {e}")
            raise

    def get_historical_data(self, symbol: str, exchange: str, currency: str, end_date: str, duration: str, bar_size: str, what_to_show: str, use_rth: bool):
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
