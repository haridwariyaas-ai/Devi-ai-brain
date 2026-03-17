from market_data.price_data import get_nifty_price
from market_data.option_chain import get_option_chain
from market_data.upstox_option_chain import get_upstox_option_chain
from market_data.upstox_live import get_upstox_live_chain
from market_data.upstox_real import get_upstox_price  # ✅ NEW

from utils.atm import find_atm

from analysis.oi_analysis import detect_bias
from analysis.pcr_analysis import calculate_pcr
from analysis.support_resistance import calculate_support_resistance
from analysis.candlestick_ai import detect_candle
from analysis.probability_engine import calculate_probability
from analysis.trend_detection import detect_trend
from analysis.volume_analysis import analyze_volume
from analysis.risk_manager import risk_manager
from analysis.oi_heatmap import oi_heatmap
from analysis.trade_score import trade_score
from analysis.signal_classifier import classify_signal

from ai_engine.strategy_generator import generate_strategy
from ai_engine.memory import save_memory
from ai_engine.decision_engine import final_decision
from ai_engine.ml_model import predict_market

# V11 Learning
from ai_engine.training_data import load_data
from ai_engine.learning_engine import evaluate_trade
from ai_engine.accuracy_tracker import update_accuracy

# ML Training
from ai_engine.ml_trainer import train_model, predict_trend


class DeviBrain:

    def run_cycle(self):

        # 🔥 V12 REAL PRICE (Upstox + fallback)
        price = get_upstox_price()

        if price is None:
            price = get_nifty_price()

        # ATM
        atm = find_atm(price)

        # Option Chain
        option_chain = get_option_chain()

        call_oi = option_chain["call_oi"]
        put_oi = option_chain["put_oi"]

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

        # Heatmap
        live_chain = get_upstox_option_chain()
        heatmap_support, heatmap_resistance = oi_heatmap(live_chain)

        # ML Prediction
        ml_prediction = predict_market()

        # Trade Score
        score = trade_score(probability, ml_prediction["confidence"], trend, volume_strength)

        # Signal
        signal = classify_signal(score)

        # ML Training Prediction
        ml_model = train_model()
        ml_trend = predict_trend(ml_model, price)

        # Memory Save
        memory_data = {
            "price": price,
            "bias": bias,
            "strategy": strategy,
            "trend": trend
        }

        save_memory(memory_data)

        # Learning
        actual_market = "Bullish"
        trade_result = evaluate_trade(ml_prediction["direction"], actual_market)
        accuracy = update_accuracy(trade_result)

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

            "HEATMAP_SUPPORT": heatmap_support,
            "HEATMAP_RESISTANCE": heatmap_resistance,

            "ML_DIRECTION": ml_prediction["direction"],
            "ML_CONFIDENCE": ml_prediction["confidence"],

            "TRADE_SCORE": score,
            "AI_SIGNAL": signal,

            "ML_TREND_PREDICTION": ml_trend,

            "TRADE_RESULT": trade_result,
            "ACCURACY": accuracy

        }

        return result
