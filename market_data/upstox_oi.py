import pandas as pd
import requests
import os
import io
from datetime import datetime

# ✅ MUST BE NAMED get_oi_data TO MATCH app.py
def get_oi_data(price):
    """Fetches Live OI for the given spot price."""
    try:
        # 1. Get Token from Streamlit Secrets
        token = os.getenv("UPSTOX_ACCESS_TOKEN")
        if not token:
            return {"strike": 0, "call_oi": 0, "put_oi": 0, "error": "No Token"}

        # 2. Update CSV if needed
        csv_path = "data/NSE_FO.csv"
        if not os.path.exists("data"): os.makedirs("data")
        
        # Download latest master if missing or old
        if not os.path.exists(csv_path) or (datetime.now() - datetime.fromtimestamp(os.path.getmtime(csv_path))).days >= 1:
            url = "https://assets.upstox.com/market-quote/instruments/exchange/complete.csv.gz"
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                df_all = pd.read_csv(io.BytesIO(res.content), compression='gzip')
                df_all[df_all['exchange'] == 'NSE_FO'].to_csv(csv_path, index=False)

        # 3. ATM Strike Selection
        atm = int(round(float(price) / 50) * 50)

        # 4. Filter for Nifty
        df = pd.read_csv(csv_path)
        df.columns = [str(col).lower().strip() for col in df.columns]
        df = df[(df["exchange"] == "nse_fo") & (df["tradingsymbol"].str.startswith("NIFTY"))].copy()
        
        df["expiry"] = pd.to_datetime(df["expiry"])
        df = df[df["expiry"] >= pd.Timestamp.today().normalize()]
        nearest_expiry = df["expiry"].min()
        df = df[df["expiry"] == nearest_expiry]

        # 5. Get Instrument Keys
        strike_df = df[df["strike"] == atm]
        ce_key = strike_df[strike_df["tradingsymbol"].str.endswith("CE")]["instrument_key"].values[0]
        pe_key = strike_df[strike_df["tradingsymbol"].str.endswith("PE")]["instrument_key"].values[0]

        # 6. Live API Call
        url = "https://api.upstox.com/v2/market-quote/quotes"
        headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
        res = requests.get(url, headers=headers, params={"symbol": f"{ce_key},{pe_key}"}).json()

        if res.get("status") == "success":
            data = res.get("data", {})
            return {
                "strike": atm,
                "call_oi": data.get(ce_key, {}).get("oi", 0),
                "put_oi": data.get(pe_key, {}).get("oi", 0),
                "time": datetime.now().strftime("%H:%M:%S")
            }
        return {"strike": atm, "call_oi": 0, "put_oi": 0}

    except Exception as e:
        return {"strike": 0, "call_oi": 0, "put_oi": 0, "error": str(e)}
