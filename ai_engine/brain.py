from market_data.price_data import get_nifty_price
from market_data.option_chain import get_option_chain

from utils.atm import find_atm

from analysis.oi_analysis import detect_bias
from analysis.pcr_analysis import calculate_pcr
from analysis.support_resistance import calculate_support_resistance
from analysis.candlestick_ai import detect_candle
from analysis.probability_engine import calculate_probability
from analysis.trend_detection import detect_trend
from analysis.volume_analysis import analyze_volume

from ai_engine.strategy_generator import generate_strategy
from ai_engine.memory import save_memory


class DeviBrain:

    def run_cycle(self):

        # 1️⃣ Price
        price = get_nifty_price()

        # 2️⃣ ATM
        atm = find_atm(price)

        # 3️⃣ Option Chain
        option_chain = get_option_chain()

        call_oi = option_chain["call_oi"]
        put_oi = option_chain["put_oi"]

        # 4️⃣ PCR
        pcr = calculate_pcr(call_oi, put_oi)

        # 5️⃣ Bias
        bias = detect_bias(call_oi, put_oi)

        # 6️⃣ Strategy
        strategy = generate_strategy(bias, pcr)

        # 7️⃣ Support Resistance
        support, resistance = calculate_support_resistance(price)

        # 8️⃣ Candle Pattern
        candle = detect_candle()

        # 9️⃣ Probability
        probability = calculate_probability(bias, pcr)

        # 🔟 Trend Detection
        trend = detect_trend()

        # 11️⃣ Volume Analysis
        volume, volume_strength = analyze_volume()

        # 12️⃣ Memory Save
        memory_data = {

            "price": price,
            "bias": bias,
            "strategy": strategy,
            "trend": trend

        }

        save_memory(memory_data)

        # 13️⃣ Final Output
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
            "VOLUME_STRENGTH": volume_strength

        }

        return result
