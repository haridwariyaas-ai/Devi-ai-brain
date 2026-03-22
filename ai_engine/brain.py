from market_data.upstox_real import get_upstox_price
from market_data.upstox_oi import get_upstox_oi

class DeviBrain:

    def run_cycle(self):

        price = get_upstox_price()

        oi = get_upstox_oi(price)

        return {
            "NIFTY_PRICE": price,
            "CALL_OI": oi["call_oi"],
            "PUT_OI": oi["put_oi"]
        }
