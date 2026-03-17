import pandas as pd
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier()

def train_model():

    try:
        df = pd.read_csv("data/nifty_history.csv")

        # Features (X)
        X = df[["price"]]

        # Target (Y)
        y = df["trend"]

        model.fit(X, y)

        return model

    except Exception as e:
        print("Training Error:", e)
        return None
