import upstox_client
import os
import streamlit as st

def get_all_indices():
    """Fetches Nifty, Bank Nifty, and Sensex using the REST API (LTP Quote)"""
    token = os.getenv("UPSTOX_ACCESS_TOKEN")
    
    # Setup configuration
    conf = upstox_client.Configuration()
    conf.access_token = token
    api_client = upstox_client.ApiClient(conf)
    
    # Initialize the Market Quote API
    api_instance = upstox_client.MarketQuoteV3Api(api_client)
    
    # Instrument keys for Nifty, Bank Nifty, and Sensex
    instruments = "NSE_INDEX|Nifty 50,NSE_INDEX|Nifty Bank,BSE_INDEX|SENSEX"
    
    try:
        # One request to get all three prices
        api_response = api_instance.get_ltp(instruments)
        data = api_response.data
        
        return {
            "NIFTY": data.get("NSE_INDEX|Nifty 50").last_price,
            "BANK_NIFTY": data.get("NSE_INDEX|Nifty Bank").last_price,
            "SENSEX": data.get("BSE_INDEX|SENSEX").last_price
        }
    except Exception as e:
        # Return zeros if there's an error so the app doesn't crash
        print(f"API Error: {e}")
        return {"NIFTY": 0.0, "BANK_NIFTY": 0.0, "SENSEX": 0.0}
