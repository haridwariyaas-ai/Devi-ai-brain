from market_data.upstox_price import get_nifty_ltp
from market_data.upstox_oi import get_option_oi
from market_data.instruments import (
    load_instruments,
    get_nearest_expiry_df,
    get_atm_options
)


class DeviBrain:

    def run_cycle(self):

        nifty_df = load_instruments()
        nifty_exp_df = get_nearest_expiry_df(nifty_df)

        price = get_nifty_ltp()

        if price == 0:
            return {"error": "Price not available"}

        ce_key, pe_key, strike = get_atm_options(nifty_exp_df, price)

        oi = get_option_oi(ce_key, pe_key)

        return {
            "price": price,
            "strike": strike,
            "oi": oi,
            "ce_key": ce_key,
            "pe_key": pe_key
        }
