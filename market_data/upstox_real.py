import upstox_client
import threading
import os
import time

# Dictionary to store all live prices
live_prices = {
    "NIFTY": 0.0,
    "BANK_NIFTY": 0.0,
    "SENSEX": 0.0
}

def on_message(feed):
    global live_prices
    nifty = feed.get("NSE_INDEX|Nifty 50")
    bank_nifty = feed.get("NSE_INDEX|Nifty Bank")
    sensex = feed.get("BSE_INDEX|SENSEX")
    
    if nifty: live_prices["NIFTY"] = nifty.ltpc.ltp
    if bank_nifty: live_prices["BANK_NIFTY"] = bank_nifty.ltpc.ltp
    if sensex: live_prices["SENSEX"] = sensex.ltpc.ltp

def start_websocket():
    token = os.getenv("UPSTOX_ACCESS_TOKEN")
    
    # Wait 10 seconds before starting to let any old connections clear
    time.sleep(10)
    
    configuration = upstox_client.Configuration()
    # Corrected: Setting access_token after initialization
    configuration.access_token = token
    api_client = upstox_client.ApiClient(configuration)
    
    streamer = upstox_client.MarketDataStreamerV3(api_client)
    streamer.on("message", on_message)
    
    try:
        streamer.connect()
        time.sleep(5) # Wait for connection handshake
        streamer.subscribe(["NSE_INDEX|Nifty 50", "NSE_INDEX|Nifty Bank", "BSE_INDEX|SENSEX"], "ltpc")
    except Exception as e:
        print(f"WS Error: {e}")
        time.sleep(30) # Cool down on error

def get_all_indices():
    if not any(t.name == "UpstoxWS" for t in threading.enumerate()):
        threading.Thread(target=start_websocket, name="UpstoxWS", daemon=True).start()
    return live_prices
