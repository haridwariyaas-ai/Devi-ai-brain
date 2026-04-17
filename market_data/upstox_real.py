import upstox_client
import threading
import os
import time

latest_nifty_price = 0.0
# Track connection attempts to prevent rapid retries
connection_attempts = 0

def on_message(feed):
    global latest_nifty_price
    nifty_feed = feed.get("NSE_INDEX|Nifty 50")
    if nifty_feed and hasattr(nifty_feed, 'ltpc'):
        latest_nifty_price = nifty_feed.ltpc.ltp

def start_websocket():
    global connection_attempts
    token = os.getenv("UPSTOX_ACCESS_TOKEN")
    
    # Wait longer with each attempt (max 60s) to clear 429 errors
    wait_time = min(connection_attempts * 10, 60)
    time.sleep(wait_time)
    
    configuration = upstox_client.Configuration()
    configuration.access_token = token
    api_client = upstox_client.ApiClient(configuration)
    
    streamer = upstox_client.MarketDataStreamerV3(api_client)
    streamer.on("message", on_message)
    
    try:
        connection_attempts += 1
        streamer.connect()
        time.sleep(5) # Crucial wait for handshake to finish
        streamer.subscribe(["NSE_INDEX|Nifty 50"], "ltpc")
    except Exception as e:
        print(f"WS Connection Failed: {e}")
        # Reset if successful, but here we just wait before allowing a retry
        time.sleep(30)

def get_nifty_price():
    global latest_nifty_price
    if not any(t.name == "UpstoxWS" for t in threading.enumerate()):
        threading.Thread(target=start_websocket, name="UpstoxWS", daemon=True).start()
    return latest_nifty_price
