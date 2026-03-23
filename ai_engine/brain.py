from market_data.upstox_real import get_upstox_price, get_upstox_oi


class DeviBrain:

    def run_cycle(self):

        price = get_upstox_price()
        oi = get_upstox_oi(price)

        result = {
            "price": price,
            "oi": oi
        }

        return result
