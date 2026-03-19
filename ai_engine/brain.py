from market_data.upstox_real import get_upstox_price
from market_data.price_data import get_nifty_price
from market_data.nse_oi import get_nse_oi  # ✅ NSE OI

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

        # 🔥 STEP 1 — REAL PRICE (Upstox)
        price = get_upstox_price()

        if price is None:
            print("⚠️ Upstox failed → fallback")
            price = get_nifty_price()

        print("🔥 FINAL PRICE:", price)

        # 🔥 STEP 2 — REAL OI (NSE)
        oi_data = get_nse_oi(price)

        call_oi = oi_data["call_oi"]
        put_oi = oi_data["put_oi"]

        print("📊 NSE OI:", call_oi, put_oi)

        # 🔥 STEP 3 — ATM
        atm = find_atm(price)

        # 🔥 STEP 4 — PCR
        pcr = calculate_pcr(call_oi, put_oi)

        # 🔥 STEP 5 — BIAS
        bias = detect_bias(call_oi, put_oi)

        # 🔥 STEP 6 — STRATEGY
        strategy = generate_strategy(bias, pcr)

        # 🔥 STEP 7 — SUPPORT / RESISTANCE
        support, resistance = calculate_support_resistance(price)

        # 🔥 STEP 8 — CANDLE
        candle = detect_candle()

        # 🔥 STEP 9 — PROBABILITY
        probability = calculate_probability(bias, pcr)

        # 🔥 STEP 10 — TREND
        trend = detect_trend()

        # 🔥 STEP 11 — VOLUME
        volume, volume_strength = analyze_volume()

        # 🔥 STEP 12 — RISK
        risk = risk_manager(probability, trend)

        # 🔥 STEP 13 — DECISION
        decision = final_decision(strategy, probability, risk)

        # 🔥 STEP 14 — SCORE
        score = trade_score(probability, 70, trend, volume_strength)

        # 🔥 STEP 15 — SIGNAL
        signal = classify_signal(score)

        # 🔥 FINAL OUTPUT
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
