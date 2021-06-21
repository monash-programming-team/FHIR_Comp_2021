import decimal
import datetime

filepath = input()

data = read_dataset(filepath)

print("Ready!")

# How many test cases?
n = int(input())

value_code = "32623-1"

def possible(patients, c_min, c_max):
    return (pow(c_max - c_min, 2) * patients) / 1000000 < 3

def solve(line):
    ids = line.split()
    # For each patient, find the latest observation with the correct value code.
    # We are guaranteed that every patient has at least one of these records.
    sorted_values = sorted([
        (min([
            (datetime.datetime.fromisoformat(obs.effective), decimal.Decimal(obs.value["value"])) 
            for obs_id in data['patients'][_id].observations 
            if (obs := data['observations'][obs_id]).code == value_code
        ])[1], _id)
        for _id in ids
    ])
    indexed = [(x, i) for i, x in enumerate(sorted_values)]
    # Try maximise every left point.
    best = 0
    for left in range(len(indexed)):
        right = left
        curmin = indexed[left][0][0]
        curmax = indexed[left][0][0]
        while possible(right - left, curmin, curmax) and right < len(indexed):
            curmin = min(curmin, indexed[right][0][0])
            curmax = max(curmax, indexed[right][0][0])
            right += 1
        best = max(best, right - left)
    print(best)

for x in range(n):
    solve(input())
