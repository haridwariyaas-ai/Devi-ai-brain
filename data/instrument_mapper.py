import pandas as pd

def load_instruments():
    df = pd.read_csv("https://assets.upstox.com/market-quote/instruments/exchange/NSE.csv")
    return df

def get_instrument_key(symbol):
    df = load_instruments()
    row = df[df["tradingsymbol"] == symbol]
    
    if row.empty:
        return None
    
    return row.iloc[0]["instrument_key"]
