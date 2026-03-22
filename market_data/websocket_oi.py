import websocket
import json
import threading
import time
import os

live_data = {
    "price": None,
    "call_oi": None,
    "put_oi": None
}


def on_message(ws, message):

    data = json.loads(message)

    print("📡 RAW:", data)

    try:
        feeds = data.get("data", {})

        for key, val in feeds.items():

            # 🔥 PRICE
            if "ltp" in val:
                live_data["price"] = val.get("ltp")

            # 🔥 OI
            if "oi" in val:
                if "CE" in key:
                    live_data["call_oi"] = val.get("oi")
                elif "PE" in key:
                    live_data["put_oi"] = val.get("oi")

    except Exception as e:
        print("❌ ERROR:", e)


def on_open(ws):

    print("🔥 CONNECTED")

    sub_data = {
        "guid": "abc",
        "method": "sub",
        "data": {
            "mode": "full",
            "instrumentKeys": [
                "NSE_INDEX|Nifty 50"
            ]
        }
    }

    ws.send(json.dumps(sub_data))


def start_websocket():

    token = os.getenv("UPSTOX_ACCESS_TOKEN")

    url = f"wss://api.upstox.com/v2/feed/market-data-feed?access_token={token}"

    ws = websocket.WebSocketApp(
        url,
        on_open=on_open,
        on_message=on_message
    )

    thread = threading.Thread(target=ws.run_forever)
    thread.daemon = True
    thread.start()

    # 🔥 WAIT LOOP (IMPORTANT FIX)
    for _ in range(10):
        if live_data["price"] is not None:
            break
        time.sleep(1)

    return live_data
