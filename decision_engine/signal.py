def generate_signal(model, latest):

    features = [[
        float(latest["EMA9"]),
        float(latest["EMA21"]),
        float(latest["Volume"])
    ]]

    prediction = model.predict(features)
    prob = model.predict_proba(features)

    signal = "Bullish" if prediction[0] == 1 else "Bearish"

    bull_prob = round(prob[0][1]*100,2)
    bear_prob = round(prob[0][0]*100,2)

    return signal, bull_prob, bear_prob
