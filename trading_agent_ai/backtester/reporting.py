import pandas as pd
import quantstats as qs
from pathlib import Path
import argparse

# Add the project root to the Python path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from trading_agent_ai.src.core.logger import setup_logging
from trading_agent_ai.backtester.engine import BacktestEngine
from trading_agent_ai.backtester.strategies import ma_crossover_strategy

log = setup_logging("reporting")

# Extend quantstats to work with pandas 2.x
qs.extend_pandas()

def generate_html_report(returns: pd.Series, output_path: Path):
    """
    Generates a full, standalone HTML report of performance metrics and plots.

    Args:
        returns (pd.Series): A Series of portfolio returns (daily, etc.).
        output_path (Path): The path to save the HTML report file.
    """
    log.info(f"Generating full HTML performance report to {output_path}...")
    try:
        qs.reports.html(returns, output=str(output_path), title="Strategy Backtest Report")
        log.info("HTML report generated successfully.")
    except Exception as e:
        log.error(f"Failed to generate HTML report: {e}", exc_info=True)

def print_summary_report(stats: pd.Series):
    """
    Prints a summary of the most important backtest statistics to the console.

    Args:
        stats (pd.Series): The stats object from a vectorbt portfolio.
    """
    if stats is None:
        log.error("Received None stats object. Cannot generate report.")
        return

    log.info("--- Performance Summary ---")
    
    # Key metrics to display
    key_metrics = [
        'Start', 'End', 'Duration', 'Total Return [%]', 'Benchmark Return [%]',
        'Max Drawdown [%]', 'Sharpe Ratio', 'Sortino Ratio', 'Calmar Ratio',
        'Total Trades', 'Win Rate [%]', 'Best Trade [%]', 'Worst Trade [%]', 'Avg Trade [%]'
    ]
    
    for metric in key_metrics:
        if metric in stats.index:
            value = stats[metric]
            # Format percentages and floats nicely
            if "[%]" in metric or isinstance(value, float):
                print(f"{metric:<25}: {value:.2f}")
            else:
                print(f"{metric:<25}: {value}")
        else:
            print(f"{metric:<25}: Not Available")
            
    log.info("---------------------------")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate performance reports from a backtest.")
    parser.add_argument("--data", type=str, default="data/processed/feature_rich_data.csv", help="Path to the data file for backtesting.")
    parser.add_argument("--report_name", type=str, default="backtest_report.html", help="Name of the output HTML report file.")

    args = parser.parse_args()

    project_root = Path(__file__).parent.parent
    data_path = project_root / args.data
    report_output_path = project_root / "backtester" / args.report_name

    if not data_path.exists():
        log.error(f"Data file not found: {data_path}")
    else:
        # Load data
        price_data = pd.read_csv(data_path, index_col='date', parse_dates=True)

        # --- Run a sample backtest to get stats ---
        # Using the MA Crossover strategy as an example
        engine = BacktestEngine(price_data, ma_crossover_strategy, strategy_params={'fast_period': 20, 'slow_period': 50})
        stats = engine.run()
        # -------------------------------------------

        # 1. Print a summary to the console
        print_summary_report(stats)

        # 2. Generate the full HTML report
        portfolio_returns = engine.portfolio.returns()
        generate_html_report(portfolio_returns, report_output_path)
