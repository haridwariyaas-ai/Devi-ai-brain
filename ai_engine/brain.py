from market_data.upstox_data import get_nifty_price
from utils.atm import find_atm
from ai_engine.decision import market_bias
from ai_engine.strategy import build_strategy


class DeviBrain:

    def run_cycle(self):

        price = get_nifty_price()

        atm = find_atm(price)

        bias = market_bias()

        strategy = build_strategy(atm)

        return {

            "NIFTY_PRICE": price,
            "ATM_STRIKE": atm,
            "MARKET_BIAS": bias,
            "TRADE_IDEA": strategy

        }
