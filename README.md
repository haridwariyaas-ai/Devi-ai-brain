
# Devi AI Brain V2

Advanced architecture for an AI‑assisted options trading system.

## Core Features

• Live NIFTY price module
• Option Chain analysis
• ATM strike detection
• AI decision engine
• Strategy module (option selling)
• Learning memory (stores outcomes)
• Risk management module
• Streamlit dashboard

## Architecture

app.py → UI Dashboard

ai_engine/
    brain.py
    decision_engine.py
    strategy_engine.py
    learning_brain.py

market_data/
    nifty_price.py
    option_chain.py

utils/
    atm_selector.py
    risk_manager.py
    logger.py

data/
    memory.json

## Run

pip install -r requirements.txt
streamlit run app.py
