from market_data.upstox_real import get_upstox_price

class DeviBrain:

    def run_cycle(self):

        price = get_upstox_price()

        return {
            "NIFTY_PRICE": price
        }
