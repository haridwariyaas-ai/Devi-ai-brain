from market_data.live_stream import start_stream

class DeviBrain:

    def run_cycle(self):

        data = start_stream()

        return {
            "NIFTY_PRICE": data["price"]
        }
