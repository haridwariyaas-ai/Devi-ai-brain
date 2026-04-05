import pandas as pd
import requests
import os
import io
import time
import streamlit as st
from datetime import datetime

def update_instrument_csv():
    """Downloads the latest NSE_FO instruments if needed."""
    url = "https://assets.upstox.com/market-quote/instruments/exchange/complete.csv.gz"
    csv_path = "data/NSE_FO.csv"
    if not os.path.exists("data"): os.makedirs("data")
    
    if os.path.exists(csv_path):
        file_age = datetime.now() - datetime.fromtimestamp(os.path.getmtime(csv_path))
        if file_age.days < 1: return

    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            df_all = pd.read_csv(io.BytesIO(response.content), compression='gzip')
            df_fo = df_all[df_all['exchange'] == 'NSE_FO']
            df_fo.to_csv(csv_path, index=False)
    except Exception as e:
        st.error(f"CSV Update Failed: {e}")

def get_live_oi(price):
    """Fetches the actual data from Upstox."""
    token = os.getenv("UPSTOX_ACCESS_TOKEN") # Ensure this is in Streamlit Secrets!
    if not token:
        return None, "Missing Token"

    try:
        update_instrument_csv()
        atm = int(round(float(price) / 50) * 50)
        
        df = pd.read_csv("data/NSE_FO.csv")
        df.columns = [str(col).lower().strip() for col in df.columns]
        
        # Filter for Nifty Current Expiry
        df = df[(df["exchange"] == "nse_fo") & (df["tradingsymbol"].str.startswith("NIFTY"))].copy()
        df["expiry"] = pd.to_datetime(df["expiry"])
        df = df[df["expiry"] >= pd.Timestamp.now().normalize()]
        nearest_expiry = df["expiry"].min()
        df = df[df["expiry"] == nearest_expiry]
        
        # Get Keys
        strike_df = df[df["strike"] == atm]
        ce_key = strike_df[strike_df["tradingsymbol"].str.endswith("CE")]["instrument_key"].values[0]
        pe_key = strike_df[strike_df["tradingsymbol"].str.endswith("PE")]["instrument_key"].values[0]

        # API Call
        url = "https://api.upstox.com/v2/market-quote/quotes"
        headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
        res = requests.get(url, headers=headers, params={"symbol": f"{ce_key},{pe_key}"}).json()

        if res.get("status") == "success":
            data = res.get("data", {})
            return {
                "strike": atm,
                "ce_oi": data.get(ce_key, {}).get("oi", 0),
                "pe_oi": data.get(pe_key, {}).get("oi", 0),
                "time": datetime.now().strftime("%H:%M:%S")
            }, None
        return None, "API Error"
    except Exception as e:
        return None, str(e)

# --- STREAMLIT UI SECTION ---
st.title("Live Nifty OI Tracker")
spot_input = st.number_input("Enter Nifty Spot Price", value=22500.0)

# This container will be overwritten every second
placeholder = st.empty()

if st.button("Start Live Feed"):
    while True:
        data, err = get_live_oi(spot_input)
        
        with placeholder.container():
            if err:
                st.error(f"Error: {err}")
                if "Sunday" in datetime.now().strftime("%A"):
                    st.warning("Note: Markets are closed today (Sunday). OI will likely stay at 0.")
            else:
                col1, col2, col3 = st.columns(3)
                col1.metric("ATM Strike", data['strike'])
                col2.metric("Call OI", f"{data['ce_oi']:,}")
                col3.metric("Put OI", f"{data['pe_oi']:,}")
                st.caption(f"Last Updated: {data['time']}")
        
        time.sleep(1) # Refresh every 1 second (Tick-by-Tick)
