
from market_data.nifty_price import get_nifty_price
from market_data.option_chain import get_option_chain
from utils.atm_selector import find_atm
from ai_engine.decision_engine import make_decision
from ai_engine.strategy_engine import build_trade
from ai_engine.learning_brain import LearningBrain

class DeviBrain:

    def __init__(self):
        self.memory = LearningBrain()

    def run_cycle(self):

        price = get_nifty_price()
        chain = get_option_chain()

        atm = find_atm(price, chain)

        decision = make_decision(chain)

        trade = build_trade(decision, atm)

        self.memory.store(trade)

        return {
            "nifty_price": price,
            "atm_strike": atm,
            "decision": decision,
            "trade_plan": trade
        }
