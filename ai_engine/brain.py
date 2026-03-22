from market_data.websocket_oi import start_websocket

class DeviBrain:

    def run_cycle(self):

        print("🔥 STARTING WEBSOCKET")

        data = start_websocket()

        print("🔥 LIVE DATA:", data)

        return {
            "NIFTY_PRICE": data["price"],
            "CALL_OI": data["call_oi"],
            "PUT_OI": data["put_oi"]
        }
