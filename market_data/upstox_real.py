import upstox_client
import threading
import os
import time

latest_nifty_price = 0.0

def on_message(feed):
    global latest_nifty_price
    nifty_feed = feed.get("NSE_INDEX|Nifty 50")
    if nifty_feed and hasattr(nifty_feed, 'ltpc'):
        latest_nifty_price = nifty_feed.ltpc.ltp

def start_websocket():
    token = os.getenv("UPSTOX_ACCESS_TOKEN")
    configuration = upstox_client.Configuration()
    configuration.access_token = token
    api_client = upstox_client.ApiClient(configuration)
    
    streamer = upstox_client.MarketDataStreamerV3(api_client)
    streamer.on("message", on_message)
    
    # Connect and wait for handshake to complete
    streamer.connect()
    time.sleep(3) 
    
    try:
        streamer.subscribe(["NSE_INDEX|Nifty 50"], "ltpc")
    except Exception as e:
        print(f"WS Subscription Error: {e}")

def get_nifty_price():
    global latest_nifty_price
    if not any(t.name == "UpstoxWS" for t in threading.enumerate()):
        threading.Thread(target=start_websocket, name="UpstoxWS", daemon=True).start()
    return latest_nifty_price
