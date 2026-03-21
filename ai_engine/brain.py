from market_data.upstox_real import get_upstox_price
from market_data.upstox_oi import get_upstox_oi


class DeviBrain:

    def run_cycle(self):

        print("🔥 FETCH PRICE")

        price = get_upstox_price()

        print("🔥 PRICE:", price)

        print("🔥 FETCH OI")

        oi_data = get_upstox_oi(price)

        call_oi = oi_data["call_oi"]
        put_oi = oi_data["put_oi"]

        print("🔥 OI:", call_oi, put_oi)

        return {
            "NIFTY_PRICE": price,
            "CALL_OI": call_oi,
            "PUT_OI": put_oi
        }
