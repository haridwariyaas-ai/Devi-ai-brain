import websocket
import json
import threading
import time
import os

# 🔥 GLOBAL DATA STORE
live_data = {
    "price": None,
    "call_oi": None,
    "put_oi": None
}

def on_message(ws, message):

    data = json.loads(message)

    print("📡 RAW:", data)

    try:
        feeds = data.get("feeds", {})

        for key, val in feeds.items():

            # price
            if "ltp" in val:
                live_data["price"] = val["ltp"]

            # OI
            if "oi" in val:
                if "CE" in key:
                    live_data["call_oi"] = val["oi"]
                elif "PE" in key:
                    live_data["put_oi"] = val["oi"]

    except Exception as e:
        print("❌ PARSE ERROR:", e)


def on_open(ws):

    print("🔥 WebSocket Connected")

    # 🔥 SUBSCRIBE (temporary example keys)
    data = {
        "guid": "test",
        "method": "sub",
        "data": {
            "instrumentKeys": [
                "NSE_INDEX|Nifty 50"
            ]
        }
    }

    ws.send(json.dumps(data))


def start_websocket():

    token = os.getenv("UPSTOX_ACCESS_TOKEN")

    url = f"wss://api.upstox.com/v2/feed/market-data-feed?access_token={token}"

    ws = websocket.WebSocketApp(
        url,
        on_message=on_message,
        on_open=on_open
    )

    thread = threading.Thread(target=ws.run_forever)
    thread.daemon = True
    thread.start()

    time.sleep(2)  # wait for data

    return live_data
