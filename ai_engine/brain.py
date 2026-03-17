from market_data.price_data import get_nifty_price
from market_data.csv_price import get_csv_price  # ✅ IMPORTANT

from market_data.option_chain import get_option_chain

from utils.atm import find_atm

from analysis.oi_analysis import detect_bias
from analysis.pcr_analysis import calculate_pcr
from analysis.support_resistance import calculate_support_resistance
from analysis.candlestick_ai import detect_candle
from analysis.probability_engine import calculate_probability
from analysis.trend_detection import detect_trend
from analysis.volume_analysis import analyze_volume
from analysis.risk_manager import risk_manager
from analysis.trade_score import trade_score
from analysis.signal_classifier import classify_signal

from ai_engine.strategy_generator import generate_strategy
from ai_engine.decision_engine import final_decision


class DeviBrain:

    def run_cycle(self):

        # 🔥 FORCE CSV (NO API for now)
        price = get_csv_price()

        if price is None:
            price = get_nifty_price()

        print("🔥 FINAL PRICE USED:", price)

        atm = find_atm(price)

        option_chain = get_option_chain()
        call_oi = option_chain["call_oi"]
        put_oi = option_chain["put_oi"]

        pcr = calculate_pcr(call_oi, put_oi)
        bias = detect_bias(call_oi, put_oi)

        strategy = generate_strategy(bias, pcr)

        support, resistance = calculate_support_resistance(price)

        candle = detect_candle()

        probability = calculate_probability(bias, pcr)

        trend = detect_trend()

        volume, volume_strength = analyze_volume()

        risk = risk_manager(probability, trend)

        decision = final_decision(strategy, probability, risk)

        score = trade_score(probability, 70, trend, volume_strength)

        signal = classify_signal(score)

        result = {
            "NIFTY_PRICE": price,
            "ATM_STRIKE": atm,
            "CALL_OI": call_oi,
            "PUT_OI": put_oi,
            "PCR": pcr,
            "MARKET_BIAS": bias,
            "AI_STRATEGY": strategy,
            "SUPPORT": support,
            "RESISTANCE": resistance,
            "CANDLE_PATTERN": candle,
            "PROBABILITY": probability,
            "TREND": trend,
            "VOLUME": volume,
            "VOLUME_STRENGTH": volume_strength,
            "RISK_LEVEL": risk,
            "AI_DECISION": decision,
            "TRADE_SCORE": score,
            "AI_SIGNAL": signal
        }

        return result
