# main.py
from importlib import import_module
from config.config import settings

if __name__ == "__main__":
    try:
        # Dynamically load strategy class
        StrategyClass = getattr(import_module(settings["STRATEGY_MODULE"]), settings["STRATEGY_CLASS"])

        # Initialize the strategy and run the bot
        strategy = StrategyClass()
        # Main execution loop moved here
        strategy.run_bot()

    except Exception as e:
        print(f"Failed to initialize: {e}")
