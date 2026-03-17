import json
import os

FILE = "data/accuracy.json"

def update_accuracy(result):

    if not os.path.exists(FILE):
        data = {"WIN": 0, "LOSS": 0}
    else:
        with open(FILE, "r") as f:
            data = json.load(f)

    data[result] += 1

    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

    return data
