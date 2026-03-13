from market.nifty_data import get_nifty_price
from market.option_chain import get_option_chain
from utils.atm import find_atm
from ai_engine.decision import market_bias
from ai_engine.strategy import build_strategy
from utils.risk import position_size
from ai_engine.learning import LearningBrain


class DeviBrain:

    def __init__(self):

        self.memory = LearningBrain()

    def run_cycle(self):

        price = get_nifty_price()

        option_chain = get_option_chain()

        atm = find_atm(price)

        bias = market_bias(option_chain["PCR"])

        strategy = build_strategy(bias, atm)

        size = position_size(100000, 2)

        trade = {
            "price": price,
            "atm": atm,
            "bias": bias,
            "strategy": strategy,
            "size": size
        }

        self.memory.store(trade)

        return trade
