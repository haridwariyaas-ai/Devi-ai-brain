import pandas as pd
import requests
import os
from datetime import datetime

def get_oi_data(price):
    try:
        token = os.getenv("UPSTOX_ACCESS_TOKEN")

        if not token or price <= 0:
            print("❌ Error: Token missing or invalid price.")
            return {"strike": 0, "call_oi": 0, "put_oi": 0}

        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {token}"
        }

        # 1. ✅ CORRECT STRIKE SELECTION (ATM)
        # Nifty strikes are in multiples of 50
        atm = int(round(float(price) / 50) * 50)
        print(f"🎯 Spot: {price} | Selected ATM Strike: {atm}")

        # 2. LOAD AND FILTER CSV
        # Make sure the path "data/NSE_FO.csv" is correct
        if not os.path.exists("data/NSE_FO.csv"):
            print("❌ Error: NSE_FO.csv file not found.")
            return {"strike": atm, "call_oi": 0, "put_oi": 0}

        df = pd.read_csv("data/NSE_FO.csv")

        # Filter for Nifty Options
        df = df[
            (df["exchange"] == "NSE_FO") &
            (df["instrument_type"] == "OPTIDX") &
            (df["root_instrument"] == "NIFTY") # Better than str.contains
        ].copy()

        # Handle Expiry
        df["expiry"] = pd.to_datetime(df["expiry"])
        today = pd.Timestamp.now().normalize()
        df = df[df["expiry"] >= today]

        # Get the nearest expiry date
        nearest_expiry = df["expiry"].min()
        df = df[df["expiry"] == nearest_expiry]

        # 3. FIND EXACT INSTRUMENT KEYS
        df["strike"] = df["strike"].astype(float).astype(int)
        
        # Get CE and PE rows for the calculated ATM strike
        strike_df = df[df["strike"] == atm]

        if strike_df.empty:
            print(f"❌ ATM Strike {atm} not found in CSV for expiry {nearest_expiry.date()}")
            return {"strike": atm, "call_oi": 0, "put_oi": 0}

        # Extract specific keys
        try:
            ce_key = strike_df[strike_df["option_type"] == "CE"]["instrument_key"].values[0]
            pe_key = strike_df[strike_df["option_type"] == "PE"]["instrument_key"].values[0]
        except IndexError:
            print("❌ CE or PE key not found for this strike.")
            return {"strike": atm, "call_oi": 0, "put_oi": 0}

        # 4. API CALL
        url = "https://api.upstox.com/v2/market-quote/quotes"
        params = {"symbol": f"{ce_key},{pe_key}"}
        
        response = requests.get(url, headers=headers, params=params)
        res_data = response.json()

        if res_data.get("status") != "success":
            print("📡 API Error:", res_data)
            return {"strike": atm, "call_oi": 0, "put_oi": 0}

        # 5. ✅ CORRECT OI EXTRACTION
        # The keys in res_data['data'] are the instrument_keys themselves
        data = res_data.get("data", {})
        
        ce_oi = data.get(ce_key, {}).get("oi", 0)
        pe_oi = data.get(pe_key, {}).get("oi", 0)

        print(f"✅ Success! Strike: {atm} | CE OI: {ce_oi} | PE OI: {pe_oi}")

        return {
            "strike": atm,
            "call_oi": ce_oi,
            "put_oi": pe_oi
        }

    except Exception as e:
        print("🚨 SYSTEM ERROR:", str(e))
        return {"strike": 0, "call_oi": 0, "put_oi": 0}

# Example Usage:
# print(get_oi_data(22432.50))
