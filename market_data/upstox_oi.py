import pandas as pd
import requests
import os
import io
from datetime import datetime

def update_instrument_csv():
    """Ensures the local CSV is fresh."""
    url = "https://assets.upstox.com/market-quote/instruments/exchange/complete.csv.gz"
    csv_path = "data/NSE_FO.csv"
    
    if not os.path.exists("data"):
        os.makedirs("data")

    # Only download if file is older than 24 hours
    if os.path.exists(csv_path):
        file_age = datetime.now() - datetime.fromtimestamp(os.path.getmtime(csv_path))
        if file_age.days < 1:
            return

    try:
        print("📥 Updating NSE_FO.csv...")
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            df_all = pd.read_csv(io.BytesIO(response.content), compression='gzip')
            df_fo = df_all[df_all['exchange'] == 'NSE_FO']
            df_fo.to_csv(csv_path, index=False)
            print("✅ CSV Updated")
    except Exception as e:
        print(f"⚠️ CSV Update Warning: {e}")

def get_oi_data(price):
    try:
        update_instrument_csv()
        
        # 1. Check Token
        token = os.getenv("UPSTOX_ACCESS_TOKEN")
        if not token:
            print("❌ ERROR: UPSTOX_ACCESS_TOKEN is empty in environment variables!")
            return {"strike": 0, "call_oi": 0, "put_oi": 0}

        # 2. ATM Strike Selection
        atm = int(round(float(price) / 50) * 50)

        # 3. Load CSV
        if not os.path.exists("data/NSE_FO.csv"):
            print("❌ ERROR: data/NSE_FO.csv not found")
            return {"strike": atm, "call_oi": 0, "put_oi": 0}

        df = pd.read_csv("data/NSE_FO.csv")
        df.columns = [str(col).lower().strip() for col in df.columns]

        # 4. Filter for Nifty Nearest Expiry
        df = df[
            (df["exchange"].str.lower() == "nse_fo") & 
            (df["instrument_type"] == "OPTIDX") & 
            (df["tradingsymbol"].str.startswith("NIFTY"))
        ].copy()

        df["expiry"] = pd.to_datetime(df["expiry"])
        df = df[df["expiry"] >= pd.Timestamp.now().normalize()]
        nearest_expiry = df["expiry"].min()
        df = df[df["expiry"] == nearest_expiry]

        # 5. Get Instrument Keys
        df["strike"] = df["strike"].astype(float).astype(int)
        strike_df = df[df["strike"] == atm]

        if strike_df.empty:
            print(f"❌ ERROR: Strike {atm} not found in CSV for current expiry")
            return {"strike": atm, "call_oi": 0, "put_oi": 0}

        ce_key = strike_df[strike_df["tradingsymbol"].str.endswith("CE")]["instrument_key"].values[0]
        pe_key = strike_df[strike_df["tradingsymbol"].str.endswith("PE")]["instrument_key"].values[0]

        # 6. API Call
        url = "https://api.upstox.com/v2/market-quote/quotes"
        headers = {"Accept": "application/json", "Authorization": f"Bearer {token}"}
        params = {"symbol": f"{ce_key},{pe_key}"}
        
        res = requests.get(url, headers=headers, params=params).json()

        if res.get("status") != "success":
            print(f"❌ API REJECTED: {res.get('errors')}")
            return {"strike": atm, "call_oi": 0, "put_oi": 0}

        # 7. Extract OI
        data = res.get("data", {})
        ce_oi = data.get(ce_key, {}).get("oi", 0)
        pe_oi = data.get(pe_key, {}).get("oi", 0)

        # Log for debugging
        print(f"DEBUG: Found keys {ce_key} and {pe_key}. Raw OI values: CE={ce_oi}, PE={pe_oi}")

        return {
            "strike": atm,
            "call_oi": ce_oi,
            "put_oi": pe_oi
        }

    except Exception as e:
        print(f"🚨 CRITICAL CRASH in upstox_oi.py: {e}")
        return {"strike": 0, "call_oi": 0, "put_oi": 0}
