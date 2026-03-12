import pandas as pd
import yfinance as yf
from sklearn.ensemble import RandomForestClassifier

def train_model():

    data = yf.download("^NSEI", period="1y", interval="1d")

    data["Return"] = data["Close"].pct_change()

    data["Direction"] = (data["Return"] > 0).astype(int)

    data["EMA9"] = data["Close"].ewm(span=9).mean()

    data["EMA21"] = data["Close"].ewm(span=21).mean()

    data = data.dropna()

    X = data[["EMA9","EMA21","Volume"]]
    y = data["Direction"]

    model = RandomForestClassifier()

    model.fit(X,y)

    return model
