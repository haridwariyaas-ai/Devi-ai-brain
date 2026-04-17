# scanners/equity_scanner.py

from utils.indicators import calculate_vwap, detect_volume_spike

def scan_equity(df):
    """
    Apply intraday trading logic
    """

    df = calculate_vwap(df)
    df = detect_volume_spike(df)

    results = []

    for _, row in df.iterrows():

        signals = []

        # 1. Breakout logic
        if row["ltp"] > row["high"]:
            signals.append("Intraday High Breakout")

        # 2. VWAP confirmation
        if row["ltp"] > row["vwap"]:
            signals.append("Trading Above VWAP")

        # 3. Volume spike
        if row["volume_spike"]:
            signals.append("Unusual Volume Activity")

        # Only return strong candidates
        if len(signals) >= 2:
            results.append({
                "symbol": row["symbol"],
                "ltp": row["ltp"],
                "signals": signals
            })

    return results
