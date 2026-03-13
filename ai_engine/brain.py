from market_data.price_data import get_nifty_price
from utils.atm import find_atm
from analysis.oi_analysis import detect_bias
from ai_engine.strategy_generator import generate_strategy

class DeviBrain:

    def run_cycle(self):

        price = get_nifty_price()

        atm = find_atm(price)

        call_oi = 120000
        put_oi = 180000

        bias = detect_bias(call_oi, put_oi)

        strategy = generate_strategy(bias)

        return {

            "NIFTY_PRICE": price,
            "ATM_STRIKE": atm,
            "MARKET_BIAS": bias,
            "AI_STRATEGY": strategy

        }
