def get_upstox_oi(price):
    import requests
    import os

    token = os.getenv("UPSTOX_ACCESS_TOKEN")

    strike = round(price / 50) * 50  # ATM strike

    ce_key = f"NSE_FO|NIFTY{strike}CE"
    pe_key = f"NSE_FO|NIFTY{strike}PE"

    url = "https://api.upstox.com/v2/market-quote/quotes"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "instrument_key": f"{ce_key},{pe_key}"
    }

    r = requests.get(url, headers=headers, params=params)

    print("OI RAW:", r.text)

    data = r.json()

    if "data" not in data:
        raise Exception(f"OI API Failed: {data}")

    ce_oi = data["data"][ce_key]["oi"]
    pe_oi = data["data"][pe_key]["oi"]

    return {
        "CE_OI": ce_oi,
        "PE_OI": pe_oi,
        "strike": strike
    }
