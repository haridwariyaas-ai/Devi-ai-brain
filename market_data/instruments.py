import pandas as pd

def load_instruments():
    df = pd.read_csv("complete.csv")

    nifty_df = df[
        (df["exchange"] == "NSE_FO") &
        (df["instrument_type"] == "OPTIDX") &
        (df["tradingsymbol"].str.contains("NIFTY"))
    ].copy()

    nifty_df["expiry"] = pd.to_datetime(nifty_df["expiry"])

    return nifty_df


def get_nearest_expiry_df(nifty_df):
    today = pd.Timestamp.today().normalize()

    future_exp = nifty_df[nifty_df["expiry"] >= today]
    nearest_expiry = future_exp["expiry"].min()

    return nifty_df[nifty_df["expiry"] == nearest_expiry]


def get_atm_options(nifty_exp_df, nifty_ltp):

    nifty_exp_df["strike_diff"] = abs(nifty_exp_df["strike"] - nifty_ltp)

    atm_strike = nifty_exp_df.sort_values("strike_diff").iloc[0]["strike"]

    nifty_exp_df["option_type"] = nifty_exp_df["tradingsymbol"].str[-2:]

    ce_df = nifty_exp_df[nifty_exp_df["option_type"] == "CE"]
    pe_df = nifty_exp_df[nifty_exp_df["option_type"] == "PE"]

    ce_df["strike_diff"] = abs(ce_df["strike"] - nifty_ltp)
    pe_df["strike_diff"] = abs(pe_df["strike"] - nifty_ltp)

    atm_ce = ce_df.sort_values("strike_diff").iloc[0]
    atm_pe = pe_df.sort_values("strike_diff").iloc[0]

    return atm_ce["instrument_key"], atm_pe["instrument_key"], atm_strike
