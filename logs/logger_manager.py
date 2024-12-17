# logs/logger_manager.py
import csv
import logging
import os


class LoggerManager:
    def __init__(self, log_file="logs/bot.log"):
        self.log_file = log_file
        self.ensure_log_directory()
        self.logger = self.setup_logger()  # Corrected attribute initialization

    def ensure_log_directory(self):
        log_dir = os.path.dirname(self.log_file)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            print(f"Created directory: {log_dir}")

    def setup_logger(self):
        logger = logging.getLogger(__name__)
        if not logger.hasHandlers():
            logger.setLevel(logging.INFO)
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

            # File handler
            file_handler = logging.FileHandler(self.log_file)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        return logger

    @staticmethod
    def log_and_save_data(bars, csv_file, append=False):
        mode = 'a' if append and os.path.exists(csv_file) else 'w'

        with open(csv_file, mode, newline='') as csvfile:
            writer = csv.writer(csvfile)

            if mode == 'w':
                writer.writerow(["Date", "Time", "Open", "High", "Low", "Close", "Volume"])

            for bar in bars:
                date = bar.date.strftime("%Y-%m-%d")
                time = bar.date.strftime("%H:%M:%S")
                row = [date, time, bar.open, bar.high, bar.low, bar.close, bar.volume]

                writer.writerow(row)
                logging.info(f"Date: {date} | Time: {time} | Open: {bar.open} | High: {bar.high} | "
                             f"Low: {bar.low} | Close: {bar.close} | Volume: {bar.volume}")
