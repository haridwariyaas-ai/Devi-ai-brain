import pandas as pd
import yfinance as yf
from sklearn.ensemble import RandomForestClassifier

def train_model():

    # download latest market data
    data = yf.download("^NSEI", period="2y", interval="1d")

    # features
    data["EMA9"] = data["Close"].ewm(span=9).mean()
    data["EMA21"] = data["Close"].ewm(span=21).mean()

    data["Return"] = data["Close"].pct_change()
    data["Direction"] = (data["Return"] > 0).astype(int)

    data = data.dropna()

    X = data[["EMA9","EMA21","Volume"]]
    y = data["Direction"]

    model = RandomForestClassifier(n_estimators=200)

    model.fit(X,y)

    return model, data
