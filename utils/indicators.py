# utils/indicators.py

import pandas as pd

def calculate_vwap(df):
    """
    VWAP calculation (intraday approximation)
    """
    df["vwap"] = (df["ltp"] * df["volume"]).cumsum() / df["volume"].cumsum()
    return df


def detect_volume_spike(df, multiplier=1.5):
    """
    Detect unusual volume activity
    """
    avg_vol = df["volume"].mean()
    df["volume_spike"] = df["volume"] > (multiplier * avg_vol)
    return df
