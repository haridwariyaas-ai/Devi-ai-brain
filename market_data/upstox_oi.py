import pandas as pd
import requests
import os

def get_upstox_oi(price):

    # 🔥 CSV load
    df = pd.read_csv("data/NSE_FO.csv")

    # 🔥 NIFTY options filter
    df = df[df["name"] == "NIFTY"]

    # 🔥 expiry ko date format me convert
    df["expiry"] = pd.to_datetime(df["expiry"])

    # 🔥 nearest expiry
    nearest_expiry = df["expiry"].min()
    df = df[df["expiry"] == nearest_expiry]

    # 🔥 ATM strike
    atm = round(price / 50) * 50

    # 🔥 closest strike find
    df["diff"] = abs(df["strike_price"] - atm)
    atm_strike = df.sort_values("diff").iloc[0]["strike_price"]

    df = df[df["strike_price"] == atm_strike]

    # 🔥 CE / PE select
    ce_row = df[df["instrument_type"] == "CE"].iloc[0]
    pe_row = df[df["instrument_type"] == "PE"].iloc[0]

    ce_key = ce_row["instrument_key"]
    pe_key = pe_row["instrument_key"]

    print("🎯 KEYS:", ce_key, pe_key)

    # 🔥 API call
    token = os.getenv("UPSTOX_ACCESS_TOKEN")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    url = "https://api.upstox.com/v2/market-quote/quotes"

    params = {
        "instrument_key": f"{ce_key},{pe_key}"
    }

    r = requests.get(url, headers=headers, params=params)
    data = r.json()

    if "data" not in data:
        print("❌ BAD RESPONSE:", data)
        return {"call_oi": 0, "put_oi": 0}

    call_oi = data["data"][ce_key]["oi"]
    put_oi = data["data"][pe_key]["oi"]

    print("✅ OI:", call_oi, put_oi)

    return {
        "call_oi": call_oi,
        "put_oi": put_oi
    }
