from market_data.upstox_price import get_price
from market_data.upstox_oi import get_oi


class DeviBrain:

    def run_cycle(self):

        price = get_price()
        oi = get_oi(price)

        return {
            "price": price,
            "oi": oi
        }
