import yfinance as yf
import pandas as pd

def get_market_data():

    data = yf.download("^NSEI", period="1y", interval="1d")

    data["EMA9"] = data["Close"].ewm(span=9).mean()
    data["EMA21"] = data["Close"].ewm(span=21).mean()

    data = data.dropna()

    return data
