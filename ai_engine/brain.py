from market_data.upstox_real import get_upstox_price
from market_data.price_data import get_nifty_price
from market_data.upstox_oi import get_real_oi  # ✅ NEW

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

        # 🔥 STEP 1 — REAL PRICE
        price = get_upstox_price()

        if price is None:
            print("⚠️ Upstox price failed → fallback")
            price = get_nifty_price()

        print("🔥 FINAL PRICE:", price)

        # 🔥 STEP 2 — REAL OI (NEW)
        oi_data = get_real_oi()

        call_oi = oi_data["call_oi"]
        put_oi = oi_data["put_oi"]

        print("📊 REAL OI:", call_oi, put_oi)

        # ATM
        atm = find_atm(price)

        # PCR
        pcr = calculate_pcr(call_oi, put_oi)

        # Bias
        bias = detect_bias(call_oi, put_oi)

        # Strategy
        strategy = generate_strategy(bias, pcr)

        # Support / Resistance
        support, resistance = calculate_support_resistance(price)

        # Candle
        candle = detect_candle()

        # Probability
        probability = calculate_probability(bias, pcr)

        # Trend
        trend = detect_trend()

        # Volume
        volume, volume_strength = analyze_volume()

        # Risk
        risk = risk_manager(probability, trend)

        # Decision
        decision = final_decision(strategy, probability, risk)

        # Trade Score
        score = trade_score(probability, 70, trend, volume_strength)

        # Signal
        signal = classify_signal(score)

        # Final Output
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
