import numpy as np
import pandas as pd
import talib


def multi_fusion_strategy(data: pd.DataFrame, rsi_period: int = 14, entry_rsi: float = 30.0, exit_rsi: float = 70.0, **kwargs) -> (pd.Series, pd.Series):
    """
    A simple example strategy for backtesting that uses the Relative Strength Index (RSI).
    This function is designed to be vectorized and compatible with vectorbt.

    In the future, this will be expanded to include the full multi-fusion logic
    (YOLO signals, news sentiment, and predictive model outputs), but those signals
    will need to be added as columns to the input `data` DataFrame first.

    Args:
        data (pd.DataFrame): DataFrame containing at least a 'close' price column.
        rsi_period (int): The time period for the RSI calculation.
        entry_rsi (float): The RSI level below which a BUY signal is generated.
        exit_rsi (float): The RSI level above which a SELL signal is generated.
        **kwargs: Catches any other strategy parameters passed from the engine.

    Returns:
        (pd.Series, pd.Series): A tuple of boolean Series for entries and exits.
    """
    # --- Placeholder for future, more complex data ---
    # For the real multi-fusion strategy, you would expect columns like:
    # 'yolo_pattern', 'sentiment_score', 'prediction_signal'
    # and the logic would be: e.g.,
    # entries = (data['yolo_pattern'] == 'BULLISH') & (data['sentiment_score'] > 0.2)

    # --- Simple RSI-based logic for MVP backtesting ---
    
    # Calculate RSI
    rsi = talib.RSI(data['close'], timeperiod=rsi_period)

    # Generate entry signals
    # An entry signal is True when the RSI crosses below the entry_rsi threshold.
    entries = (rsi.shift(1) >= entry_rsi) & (rsi < entry_rsi)
    
    # Generate exit signals
    # An exit signal is True when the RSI crosses above the exit_rsi threshold.
    exits = (rsi.shift(1) <= exit_rsi) & (rsi > exit_rsi)

    # Vectorbt expects boolean Series. Let's ensure there are no NaNs.
    entries.fillna(False, inplace=True)
    exits.fillna(False, inplace=True)

    return entries, exits

# You can define other strategies here as well.
# For example, a simple moving average crossover strategy:

def ma_crossover_strategy(data: pd.DataFrame, fast_period: int = 50, slow_period: int = 200, **kwargs) -> (pd.Series, pd.Series):
    """
    A simple moving average (MA) crossover strategy.
    Generates a BUY signal when the fast MA crosses above the slow MA.
    Generates a SELL signal when the fast MA crosses below the slow MA.
    """
    fast_ma = talib.SMA(data['close'], timeperiod=fast_period)
    slow_ma = talib.SMA(data['close'], timeperiod=slow_period)

    # Entry signal: fast MA crosses above slow MA
    entries = (fast_ma.shift(1) <= slow_ma.shift(1)) & (fast_ma > slow_ma)

    # Exit signal: fast MA crosses below slow MA
    exits = (fast_ma.shift(1) >= slow_ma.shift(1)) & (fast_ma < slow_ma)

    entries.fillna(False, inplace=True)
    exits.fillna(False, inplace=True)

    return entries, exits
