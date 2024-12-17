import pandas as pd
import os
import logging

# Define paths
data_folder = "data"
output_file = "combined.csv"
log_file = "combine_csv.log"

# Ensure the log directory exists
log_dir = os.path.dirname(log_file)
if log_dir:
    os.makedirs(log_dir, exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

def combine_csv_files(input_folder=data_folder, output_file=output_file):
    try:
        # Collect all CSV files in the input folder
        csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]

        if not csv_files:
            logging.error("No CSV files found in the input folder.")
            return

        dataframes = []
        for file in csv_files:
            file_path = os.path.join(input_folder, file)
            try:
                logging.info(f"Reading file: {file_path}")
                df = pd.read_csv(file_path)

                if df.empty:
                    logging.warning(f"File {file_path} is empty.")
                    continue

                dataframes.append(df)
                logging.info(f"Successfully read {file_path} with {len(df)} rows.")

            except pd.errors.EmptyDataError:
                logging.error(f"File {file_path} has no data or is corrupted.")
            except Exception as e:
                logging.error(f"Unexpected error reading {file_path}: {e}")

        if not dataframes:
            logging.error("No valid CSV files were processed.")
            return

        # Combine all DataFrames
        combined_df = pd.concat(dataframes, ignore_index=True)

        # Remove duplicates
        cleaned_df = combined_df.drop_duplicates()

        # Save the combined CSV
        cleaned_df.to_csv(output_file, index=False)
        logging.info(f"Combined CSV saved to: {output_file}")

    except Exception as e:
        logging.error(f"Error during CSV combining: {e}")

if __name__ == "__main__":
    combine_csv_files()
