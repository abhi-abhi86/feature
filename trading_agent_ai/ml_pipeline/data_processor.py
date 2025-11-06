import pandas as pd
import argparse
import os
from pathlib import Path

# Add the project root to the Python path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from trading_agent_ai.src.core.logger import setup_logging

log = setup_logging("data_processor")

def process_data(input_path: Path, output_path: Path):
    """
    Cleans raw historical data, handles missing values, and saves it to the processed data folder.

    Args:
        input_path (Path): The path to the raw CSV data file.
        output_path (Path): The path to save the processed CSV data file.
    """
    if not input_path.exists():
        log.error(f"Input file not found: {input_path}")
        return

    log.info(f"Starting processing for {input_path.name}...")

    try:
        # Load the raw data
        df = pd.read_csv(input_path)

        # --- Data Cleaning Logic ---

        # 1. Standardize column names (e.g., to lowercase)
        df.columns = [col.lower() for col in df.columns]

        # 2. Ensure essential columns are present
        required_cols = ['date', 'open', 'high', 'low', 'close', 'volume']
        if not all(col in df.columns for col in required_cols):
            log.error(f"Missing one or more required columns in {input_path.name}. Required: {required_cols}")
            return

        # 3. Handle 'date' column
        # Convert to datetime and set as index
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date').sort_index()

        # 4. Handle missing values (NaNs)
        # Forward-fill is a common strategy for time-series data
        initial_nans = df.isnull().sum().sum()
        if initial_nans > 0:
            log.warning(f"Found {initial_nans} missing values. Applying forward-fill.")
            df.fillna(method='ffill', inplace=True)
            # Backward-fill for any remaining NaNs at the beginning of the file
            df.fillna(method='bfill', inplace=True)

        # 5. Correct data types
        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = pd.to_numeric(df[col])

        # 6. Remove duplicate rows (if any)
        initial_rows = len(df)
        df.drop_duplicates(inplace=True)
        if len(df) < initial_rows:
            log.warning(f"Removed {initial_rows - len(df)} duplicate rows.")

        # --- End of Cleaning Logic ---

        # Ensure the output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Save the processed data
        df.to_csv(output_path)
        log.info(f"Successfully processed data and saved to {output_path}")

    except Exception as e:
        log.error(f"Failed to process {input_path.name}. Error: {e}", exc_info=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process and clean raw financial data.")
    parser.add_argument("input_file", type=str, help="Name of the raw data file in the data/raw/ directory.")
    parser.add_argument("output_file", type=str, help="Name of the processed file to be saved in data/processed/.")

    args = parser.parse_args()

    # Construct full paths
    project_root = Path(__file__).parent.parent
    raw_data_dir = project_root / "data" / "raw"
    processed_data_dir = project_root / "data" / "processed"

    input_file_path = raw_data_dir / args.input_file
    output_file_path = processed_data_dir / args.output_file

    process_data(input_file_path, output_file_path)
