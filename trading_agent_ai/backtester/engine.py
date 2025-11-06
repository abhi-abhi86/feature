import pandas as pd
import vectorbt as vbt
from pathlib import Path
import argparse

# Add the project root to the Python path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from trading_agent_ai.src.core.logger import setup_logging
from trading_agent_ai.backtester.strategies import multi_fusion_strategy # Import the strategy logic

log = setup_logging("backtest_engine")

class BacktestEngine:
    """
    The core backtesting harness using vectorbt.
    """
    def __init__(self, data: pd.DataFrame, strategy_func, strategy_params: dict = None):
        """
        Initializes the BacktestEngine.

        Args:
            data (pd.DataFrame): DataFrame with price data (OHLCV).
            strategy_func: The function that generates entry and exit signals.
            strategy_params (dict): Parameters to pass to the strategy function.
        """
        if not isinstance(data.index, pd.DatetimeIndex):
            raise ValueError("Data index must be a DatetimeIndex.")
        
        self.data = data
        self.strategy_func = strategy_func
        self.strategy_params = strategy_params if strategy_params is not None else {}
        self.portfolio = None
        log.info("BacktestEngine initialized.")

    def run(
        self,
        initial_cash: float = 100000,
        commission: float = 0.001, # 0.1% commission
        slippage: float = 0.001,   # 0.1% slippage
        freq: str = 'D' # Daily frequency
    ):
        """
        Runs the backtest.

        Args:
            initial_cash (float): The starting cash for the portfolio.
            commission (float): The commission fee per trade.
            slippage (float): The slippage per trade.
            freq (str): The frequency of the data ('D' for daily, 'T' for minute, etc.).
        """
        log.info("Running backtest...")
        log.info(f"Parameters: Initial Cash=${initial_cash}, Commission={commission*100}%, Slippage={slippage*100}%")

        # Generate signals using the provided strategy function
        log.info(f"Generating signals with strategy: {self.strategy_func.__name__}")
        entries, exits = self.strategy_func(self.data, **self.strategy_params)

        # Ensure signals are boolean arrays
        entries = entries.vbt.signals.to_boolean_array()
        exits = exits.vbt.signals.to_boolean_array()

        # Create the portfolio
        self.portfolio = vbt.Portfolio.from_signals(
            close=self.data['close'],
            entries=entries,
            exits=exits,
            freq=freq,
            init_cash=initial_cash,
            fees=commission,
            slippage=slippage
        )

        log.info("Backtest completed.")
        return self.portfolio.stats()

    def get_stats(self):
        """Returns the performance statistics of the backtest."""
        if self.portfolio is None:
            log.warning("Portfolio not created. Run the backtest first.")
            return None
        return self.portfolio.stats()

    def plot(self):
        """Plots the backtest results."""
        if self.portfolio is None:
            log.warning("Portfolio not created. Run the backtest first.")
            return
        self.portfolio.plot().show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a backtest using the vectorbt engine.")
    parser.add_argument("--data", type=str, default="data/processed/feature_rich_data.csv", help="Path to the feature-rich data file for backtesting.")
    parser.add_argument("--plot", action="store_true", help="If set, plots the backtest results.")

    args = parser.parse_args()

    project_root = Path(__file__).parent.parent
    data_path = project_root / args.data

    if not data_path.exists():
        log.error(f"Data file not found: {data_path}")
    else:
        # Load data
        price_data = pd.read_csv(data_path, index_col='date', parse_dates=True)

        # Define strategy parameters (example)
        params = {
            'rsi_period': 14,
            'entry_rsi': 30,
            'exit_rsi': 70
        }

        # Initialize and run the engine
        engine = BacktestEngine(price_data, multi_fusion_strategy, strategy_params=params)
        stats = engine.run()

        # Print stats
        print("\n--- Backtest Results ---")
        print(stats)
        print("------------------------\n")

        if args.plot:
            log.info("Displaying plot...")
            engine.plot()
