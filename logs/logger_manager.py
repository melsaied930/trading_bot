# logs/logger_manager.py
import logging
import csv
import os

class LoggerManager:
    def __init__(self, log_file="logs/bot.log"):
        self.log_file = log_file
        self.ensure_log_directory()
        self.setup_logger()

    def ensure_log_directory(self):
        log_dir = os.path.dirname(self.log_file)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            print(f"Created directory: {log_dir}")

    def setup_logger(self):
        # Correct logging format with timestamp and log level
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )

    @staticmethod
    def log_and_save_data(bars, csv_file):
        with open(csv_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Date", "Time", "Open", "High", "Low", "Close", "Volume"])

            for bar in bars:
                date = bar.date.strftime("%Y-%m-%d")
                time = bar.date.strftime("%H:%M:%S")
                row = [date, time, bar.open, bar.high, bar.low, bar.close, bar.volume]

                writer.writerow(row)
                logging.info(f"{time} | Open: {bar.open} | High: {bar.high} | "
                             f"Low: {bar.low} | Close: {bar.close} | Volume: {bar.volume}")
