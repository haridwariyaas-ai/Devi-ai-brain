from sklearn.ensemble import RandomForestClassifier

def train_model(data):

    data["Return"] = data["Close"].pct_change()
    data["Direction"] = (data["Return"] > 0).astype(int)

    data = data.dropna()

    X = data[["EMA9","EMA21","Volume"]]
    y = data["Direction"]

    model = RandomForestClassifier(n_estimators=200)

    model.fit(X,y)

    return model
