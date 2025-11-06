import pandas as pd
import talib
import argparse
from pathlib import Path

# Add the project root to the Python path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from trading_agent_ai.src.core.logger import setup_logging

log = setup_logging("feature_engineering")

def add_features(
    input_path: Path,
    output_path: Path,
    rsi_period: int = 14,
    macd_fast: int = 12,
    macd_slow: int = 26,
    macd_signal: int = 9,
    bollinger_period: int = 20,
    bollinger_dev: int = 2
):
    """
    Adds technical analysis features to the processed data.

    Args:
        input_path (Path): Path to the processed data file.
        output_path (Path): Path to save the feature-rich data file.
        rsi_period (int): Period for RSI calculation.
        macd_fast (int): Fast period for MACD.
        macd_slow (int): Slow period for MACD.
        macd_signal (int): Signal period for MACD.
        bollinger_period (int): Period for Bollinger Bands.
        bollinger_dev (int): Standard deviations for Bollinger Bands.
    """
    if not input_path.exists():
        log.error(f"Input file not found: {input_path}")
        return

    log.info(f"Starting feature engineering for {input_path.name}...")

    try:
        df = pd.read_csv(input_path, index_col='date', parse_dates=True)

        # --- Feature Engineering Logic ---

        # 1. Relative Strength Index (RSI)
        df['rsi'] = talib.RSI(df['close'], timeperiod=rsi_period)

        # 2. Moving Average Convergence Divergence (MACD)
        macd, macdsignal, _ = talib.MACD(
            df['close'],
            fastperiod=macd_fast,
            slowperiod=macd_slow,
            signalperiod=macd_signal
        )
        df['macd'] = macd
        df['macd_signal'] = macdsignal

        # 3. Bollinger Bands
        upper, middle, lower = talib.BBANDS(
            df['close'],
            timeperiod=bollinger_period,
            nbdevup=bollinger_dev,
            nbdevdn=bollinger_dev,
            matype=0  # SMA
        )
        df['bollinger_upper'] = upper
        df['bollinger_middle'] = middle
        df['bollinger_lower'] = lower

        # 4. Average True Range (ATR) - a measure of volatility
        df['atr'] = talib.ATR(df['high'], df['low'], df['close'], timeperiod=14)
        
        # 5. Simple Moving Averages (SMA)
        df['sma_50'] = talib.SMA(df['close'], timeperiod=50)
        df['sma_200'] = talib.SMA(df['close'], timeperiod=200)

        # --- End of Feature Engineering ---

        # Drop rows with NaN values created by the indicators
        initial_rows = len(df)
        df.dropna(inplace=True)
        log.info(f"Removed {initial_rows - len(df)} rows with NaN values after feature creation.")

        # Ensure the output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Save the feature-rich data
        df.to_csv(output_path)
        log.info(f"Successfully added features and saved to {output_path}")

    except Exception as e:
        log.error(f"Failed to add features to {input_path.name}. Error: {e}", exc_info=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add technical analysis features to processed data.")
    parser.add_argument("input_file", type=str, help="Name of the processed data file in the data/processed/ directory.")
    parser.add_argument("output_file", type=str, help="Name of the feature-rich file to be saved in data/processed/.")

    args = parser.parse_args()

    # Construct full paths
    project_root = Path(__file__).parent.parent
    processed_data_dir = project_root / "data" / "processed"

    input_file_path = processed_data_dir / args.input_file
    output_file_path = processed_data_dir / args.output_file

    add_features(input_file_path, output_file_path)
