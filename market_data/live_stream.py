from upstox_api.api import *

import os
import time

live_data = {
    "price": None
}

def start_stream():

    access_token = os.getenv("UPSTOX_ACCESS_TOKEN")

    u = Upstox(access_token, "ce332ba7-0561-4057-9972-8cbe1b859ce6")

    def on_tick(tick):

        print("📡 TICK:", tick)

        try:
            live_data["price"] = tick['ltp']
        except:
            pass

    u.set_on_tick(on_tick)

    u.subscribe('NSE_INDEX|Nifty 50', LiveFeedType.Full)

    u.start_websocket(False)

    # wait for data
    for _ in range(10):
        if live_data["price"] is not None:
            break
        time.sleep(1)

    return live_data
