"""
Data Collector Tool
Downloads historical market data from broker APIs and saves to data/raw/
"""

import sys
from pathlib import Path
import pandas as pd
import logging

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from core.config_loader import ConfigLoader
from data_handler.api_client import APIClient

logger = logging.getLogger(__name__)

class DataCollector:
    def __init__(self):
        self.config = ConfigLoader()
        self.api_client = APIClient(self.config)
        self.raw_data_dir = Path("data/raw")
        self.raw_data_dir.mkdir(parents=True, exist_ok=True)

    def collect_historical_data(self, ticker: str, interval: str = "1day", days: int = 365):
        """
        Collects historical data for a given ticker.
        """
        try:
            from datetime import datetime, timedelta
            
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Format dates for API
            start_str = start_date.strftime("%Y-%m-%d")
            end_str = end_date.strftime("%Y-%m-%d")
            
            # Fetch data from broker API
            data = self.api_client.get_historical_data(
                ticker=ticker,
                interval=interval,
                from_date=start_str,
                to_date=end_str
            )
            
            # Convert to DataFrame and save
            df = pd.DataFrame(data)
            filename = f"{ticker}_{interval}_{days}days.csv"
            filepath = self.raw_data_dir / filename
            
            df.to_csv(filepath, index=False)
            logger.info(f"Saved {len(df)} records to {filepath}")
            
        except Exception as e:
            logger.error(f"Error collecting data for {ticker}: {e}")

if __name__ == "__main__":
    collector = DataCollector()
    
    # Example: Collect data for major Indian indices
    tickers = ["NIFTY", "BANKNIFTY", "RELIANCE", "TCS", "INFY"]
    
    for ticker in tickers:
        print(f"Collecting data for {ticker}...")
        collector.collect_historical_data(ticker)
    
    print("Data collection complete!")
