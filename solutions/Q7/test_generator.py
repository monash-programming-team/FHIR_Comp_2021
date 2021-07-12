import random

with open(f"solutions/Q7/1.in", "w") as f:
    print(20, file=f)
    for x in range(20):
        print(random.randint(1, 100), file=f)
