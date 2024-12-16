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
        if not logging.getLogger().hasHandlers():
            logging.basicConfig(
                level=logging.INFO,
                format="%(asctime)s - %(levelname)s - %(message)s",
                handlers=[
                    logging.FileHandler(self.log_file),
                    logging.StreamHandler()
                ]
            )

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
                logging.info(f"{time} | Open: {bar.open} | High: {bar.high} | "
                             f"Low: {bar.low} | Close: {bar.close} | Volume: {bar.volume}")
