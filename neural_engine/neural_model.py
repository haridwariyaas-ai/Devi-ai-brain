import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

def build_model():

    model = Sequential()

    model.add(Dense(32, activation="relu", input_shape=(3,)))
    model.add(Dense(16, activation="relu"))
    model.add(Dense(2, activation="softmax"))

    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model


def train_neural_model(data):

    data["Return"] = data["Close"].pct_change()
    data["Direction"] = (data["Return"] > 0).astype(int)

    data = data.dropna()

    X = data[["EMA9","EMA21","Volume"]].values
    y = data["Direction"].values

    model = build_model()

    model.fit(X, y, epochs=5, batch_size=16, verbose=0)

    return model
    return model
import numpy as np

def neural_predict(model, latest):

    features = np.array([[
        float(latest["EMA9"]),
        float(latest["EMA21"]),
        float(latest["Volume"])
    ]])

    prob = model.predict(features)

    bull = round(prob[0][1]*100,2)
    bear = round(prob[0][0]*100,2)

    signal = "Bullish" if bull > bear else "Bearish"

    return signal, bull, bear
