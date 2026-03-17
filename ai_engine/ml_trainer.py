import pandas as pd
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier()

def train_model():

    try:
        df = pd.read_csv("data/nifty_history.csv")

        X = df[["price"]]
        y = df["trend"]

        model.fit(X, y)

        return model

    except Exception as e:
        print("Training Error:", e)
        return None


def predict_trend(model, price):

    try:
        prediction = model.predict([[price]])

        return prediction[0]

    except:
        return "Sideways"
