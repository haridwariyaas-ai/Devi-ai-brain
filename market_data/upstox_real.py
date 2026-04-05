import upstox_client
import threading
import os
import streamlit as st

# Global variable to store the latest Nifty price
latest_nifty_price = 0.0

def on_message(feed):
    """Callback function triggered when a new tick arrives."""
    global latest_nifty_price
    try:
        # The SDK automatically decodes the Protobuf message
        # We look for the Nifty 50 Index feed
        nifty_feed = feed.get("NSE_INDEX|Nifty 50")
        if nifty_feed and hasattr(nifty_feed, 'ltpc'):
            latest_nifty_price = nifty_feed.ltpc.ltp
    except Exception as e:
        print(f"WS Message Error: {e}")

def start_websocket():
    """Initializes and connects the Upstox Market Data Streamer."""
    access_token = os.getenv("UPSTOX_ACCESS_TOKEN")
    
    # 1. Configuration
    configuration = upstox_client.Configuration()
    configuration.access_token = access_token
    api_client = upstox_client.ApiClient(configuration)
    
    # 2. Initialize Streamer
    # We subscribe to Nifty 50 Index (NSE_INDEX|Nifty 50)
    streamer = upstox_client.MarketDataStreamerV3(api_client)
    
    # 3. Set Callbacks
    streamer.on("message", on_message)
    streamer.on("error", lambda err: print(f"WS Error: {err}"))
    
    # 4. Connect and Subscribe
    streamer.connect()
    streamer.subscribe(["NSE_INDEX|Nifty 50"], "ltpc")

def get_nifty_price():
    """Starts the WebSocket thread if not running and returns current price."""
    global latest_nifty_price
    
    # Check if the background thread is already running
    if not any(t.name == "UpstoxWebSocket" for t in threading.enumerate()):
        ws_thread = threading.Thread(target=start_websocket, name="UpstoxWebSocket", daemon=True)
        ws_thread.start()
        print("🚀 WebSocket Thread Started")
        
    return latest_nifty_price
