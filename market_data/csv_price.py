import pandas as pd
import random

def get_csv_price():

    try:
        df = pd.read_csv("data/nifty_history.csv")

        price = random.choice(df["price"].tolist())

        print("📊 CSV PRICE:", price)

        return price

    except Exception as e:
        print("❌ CSV ERROR:", e)
        return None 
