import pandas as pd
import yfinance as yf
from sklearn.ensemble import RandomForestClassifier


def train_model():

    data = yf.download("^NSEI", period="1y", interval="1d")

    data["EMA9"] = data["Close"].ewm(span=9).mean()
    data["EMA21"] = data["Close"].ewm(span=21).mean()

    data["Return"] = data["Close"].pct_change()
    data["Direction"] = (data["Return"] > 0).astype(int)

    data = data.dropna()

    X = data[["EMA9", "EMA21", "Volume"]]
    y = data["Direction"]

    model = RandomForestClassifier(n_estimators=200)

    model.fit(X, y)

    return model, data


def predict_signal(model, data):

    latest = data.iloc[-1]

    features = [[
        float(latest["EMA9"]),
        float(latest["EMA21"]),
        float(latest["Volume"])
    ]]

    prediction = model.predict(features)

    prob = model.predict_proba(features)

    bull = round(prob[0][1] * 100, 2)
    bear = round(prob[0][0] * 100, 2)

    signal = "Bullish" if prediction[0] == 1 else "Bearish"

    return signal, bull, bear, latest["Close"]
    prediction = model.predict(features)

    prob = model.predict_proba(features)

    bull = round(prob[0][1] * 100, 2)
    bear = round(prob[0][0] * 100, 2)

    signal = "Bullish" if prediction[0] == 1 else "Bearish"

    return signal, bull, bear, latest["Close"]    ]]

    prediction=model.predict(features)

    prob=model.predict_proba(features)

    bull=round(prob[0][1]*100,2)
    bear=round(prob[0][0]*100,2)

    signal="Bullish" if prediction[0]==1 else "Bearish"

    return signal,bull,bear,latest["Close"]
    model.fit(X,y)

    return model,data


def predict_signal(model,data):

    latest=data.iloc[-1]

    features=[[
        float(latest["EMA9"]),
        float(latest["EMA21"]),
        float(latest["Volume"]),
        float(latest["RSI"])
    ]]

    prediction=model.predict(features)

    prob=model.predict_proba(features)

    bull=round(prob[0][1]*100,2)
    bear=round(prob[0][0]*100,2)

    signal="Bullish" if prediction[0]==1 else "Bearish"

    return signal,bull,bear,latest    prediction = model.predict(features)
    prob = model.predict_proba(features)

    bull = round(prob[0][1]*100,2)
    bear = round(prob[0][0]*100,2)

    signal = "Bullish" if prediction[0]==1 else "Bearish"

    return signal,bull,bear,latest["Close"]
