import decimal
import heapq
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
    """bad_ids = [
        _id
        for _id in ids
        if len([
            obs_id
            for obs_id in data['patients'][_id].observations 
            if (obs := data['observations'][obs_id]).code == value_code
        ]) == 0
    ]
    print(bad_ids)"""
    sorted_values = sorted([
        (min([
            (datetime.datetime.fromisoformat(obs.effective), decimal.Decimal(obs.value["value"])) 
            for obs_id in data['patients'][_id].observations 
            if (obs := data['observations'][obs_id]).code == value_code
        ])[1], _id)
        for _id in ids
    ])
    indexed = [(x, i) for i, x in enumerate(sorted_values)]
    # Left / Right pointer solution.
    left = 0
    right = 1
    heapq.heapify(min_heap := [])
    heapq.heapify(max_heap := [])
    heapq.heappush(min_heap, indexed[0])
    heapq.heappush(max_heap, ((-indexed[0][0][0], indexed[0][0][1]), indexed[0][1]))
    best_score = 1
    while left < len(indexed):
        while right < len(indexed):
            if right == left or possible(right - left, min_heap[0][0][0], -max_heap[0][0][0]):
                best_score = max(best_score, right - left + 1)
                heapq.heappush(min_heap, indexed[right])
                heapq.heappush(max_heap, ((-indexed[right][0][0], indexed[right][0][1]), indexed[right][1]))
                right += 1
            else:
                break
        left += 1
        while len(min_heap) >= 1 and min_heap[0][1] < left:
            heapq.heappop(min_heap)
        while len(max_heap) >= 1 and max_heap[0][1] < left:
            heapq.heappop(max_heap)
    print(best_score)

for x in range(n):
    solve(input())
