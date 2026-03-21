print("🔥🔥 NEW BRAIN FILE RUNNING 🔥🔥")

from market_data.upstox_real import get_upstox_price
from market_data.price_data import get_nifty_price
from market_data.nse_oi import get_nse_oi


class DeviBrain:

    def run_cycle(self):

        print("🔥 STEP 1 — PRICE FETCH")

        price = get_upstox_price()

        if price is None:
            print("⚠️ fallback price used")
            price = get_nifty_price()

        print("🔥 FINAL PRICE:", price)

        print("🔥 STEP 2 — CALLING NSE OI")

        oi_data = get_nse_oi(price)

        call_oi = oi_data["call_oi"]
        put_oi = oi_data["put_oi"]

        print("🔥 FINAL OI:", call_oi, put_oi)

        return {
            "NIFTY_PRICE": price,
            "CALL_OI": call_oi,
            "PUT_OI": put_oi
        }
