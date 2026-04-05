import pandas as pd
import requests
import os

def get_oi_data(price):
    try:
        # 1. Setup credentials
        token = os.getenv("UPSTOX_ACCESS_TOKEN")
        if not token or price <= 0:
            return {"strike": 0, "call_oi": 0, "put_oi": 0}

        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {token}"
        }

        # 2. ✅ Correct Strike Selection (ATM)
        # Rounding to nearest 50 for NIFTY
        atm = int(round(float(price) / 50) * 50)
        print(f"🎯 Calculated ATM Strike: {atm}")

        # 3. Load and Filter CSV
        if not os.path.exists("data/NSE_FO.csv"):
            print("❌ File data/NSE_FO.csv not found!")
            return {"strike": atm, "call_oi": 0, "put_oi": 0}

        df = pd.read_csv("data/NSE_FO.csv")

        # Filter for Nifty Options only
        df = df[
            (df["exchange"] == "NSE_FO") &
            (df["instrument_type"] == "OPTIDX") &
            (df["root_instrument"] == "NIFTY")
        ].copy()

        # Handle Expiry (Nearest Expiry)
        df["expiry"] = pd.to_datetime(df["expiry"])
        df = df[df["expiry"] >= pd.Timestamp.today().normalize()]
        nearest_expiry = df["expiry"].min()
        df = df[df["expiry"] == nearest_expiry]

        # 4. Get Instrument Keys for CE and PE
        df["strike"] = df["strike"].astype(float).astype(int)
        exact_df = df[df["strike"] == atm]

        if exact_df.empty:
            print(f"❌ Strike {atm} not found in CSV.")
            return {"strike": atm, "call_oi": 0, "put_oi": 0}

        # Extract the exact keys required for the API
        ce_key = exact_df[exact_df["option_type"] == "CE"]["instrument_key"].values[0]
        pe_key = exact_df[exact_df["option_type"] == "PE"]["instrument_key"].values[0]

        # 5. API Call
        url = "https://api.upstox.com/v2/market-quote/quotes"
        params = {"symbol": f"{ce_key},{pe_key}"}
        
        res = requests.get(url, headers=headers, params=params).json()

        # 6. ✅ FIX: Extract OI using the Instrument Key
        # Upstox returns data mapped to the instrument_key itself
        data = res.get("data", {})
        
        # Accessing data directly using the keys we found in the CSV
        ce_oi = data.get(ce_key, {}).get("oi", 0)
        pe_oi = data.get(pe_key, {}).get("oi", 0)

        print(f"📡 API Response Received for {ce_key} and {pe_key}")
        
        return {
            "strike": atm,
            "call_oi": ce_oi,
            "put_oi": pe_oi
        }

    except Exception as e:
        print(f"🚨 Error: {e}")
        return {"strike": 0, "call_oi": 0, "put_oi": 0}

# Usage:
# result = get_oi_data(22436.50)
# print(result)
