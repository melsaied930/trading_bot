# utils/config_loader.py

import yaml
from pathlib import Path


def load_config(config_file: str | Path) -> dict:
    try:
        with open(config_file, "r") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file '{config_file}' not found.")
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing configuration file: {e}")
