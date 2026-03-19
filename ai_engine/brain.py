print("🔥🔥 NEW BRAIN FILE RUNNING 🔥🔥")

from market_data.upstox_fetch_csv import fetch_and_save_data
from market_data.price_data import get_nifty_price

class DeviBrain:

    def run_cycle(self):

        print("🔥 FETCH FUNCTION START")

        # 🔥 FORCE Upstox call
        price = fetch_and_save_data()

        print("🔥 FETCH FUNCTION END:", price)

        if price is None:
            print("⚠️ FALLBACK TRIGGERED")
            price = get_nifty_price()

        print("🔥 FINAL PRICE USED:", price)

        return {
            "NIFTY_PRICE": price,
            "STATUS": "RUNNING"
        }
