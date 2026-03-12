
import json
import os

class LearningBrain:

    def __init__(self):

        self.file = "data/memory.json"

        if not os.path.exists("data"):
            os.makedirs("data")

    def store(self, trade):

        try:
            with open(self.file,"r") as f:
                data = json.load(f)
        except:
            data = []

        data.append(trade)

        with open(self.file,"w") as f:
            json.dump(data,f,indent=4)
