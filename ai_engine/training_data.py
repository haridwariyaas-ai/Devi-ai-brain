import pandas as pd

def load_data():

    try:
        df = pd.read_csv("data/nifty_history.csv")
        return df

    except:
        return None
