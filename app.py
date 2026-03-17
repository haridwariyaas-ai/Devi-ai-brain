print("🔥🔥 APP NEW VERSION RUNNING 🔥🔥")

from ai_engine.brain import DeviBrain

import random
print("🔥 TEST PRICE:", random.randint(22000, 23000))

brain = DeviBrain()
result = brain.run_cycle()

print(result)
