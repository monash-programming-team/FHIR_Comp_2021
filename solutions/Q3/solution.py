"""
For the most part, either grouping everything together or nothing at all seems to dominate, after some analysis.
So try both and pick the best.
"""

import decimal
import datetime
import math

filepath = input()

data = read_dataset(filepath)

print("Ready!")

# How many test cases?
tests = int(input())

value_code = "8302-2"

d = 0

def solve_single(sorted_values):   
    return list(map(lambda x: x[1], sorted_values)), [[0, len(sorted_values)-1]]

def solve_all(sorted_values):    
    return list(map(lambda x: x[1], sorted_values)), [
        [x, x+1]
        for x in range(len(sorted_values)-1)
    ]

for x in range(tests):
    d, n = list(map(float, input().split()))
    n = int(n)
    sorted_values = sorted([
        (max([
            (datetime.datetime.fromisoformat(obs.effective), obs.value["value"])
            for obs_id in data['patients'][_id].observations 
            if (obs := data['observations'][obs_id]).code == value_code
        ])[1], _id)
        for _id in input().split()
    ])[::-1]
    patients, generalisations1 = solve_single(sorted_values)
    patients, generalisations2 = solve_all(sorted_values)
    cost1 = 0
    cost2 = 0
    for pat1, pat2 in generalisations1:
        cost1 += math.log(
            # Difference in height
            abs(sorted_values[pat1][0] - sorted_values[pat2][0]) / 
            # d * (difference in position + 1)
            (d * (abs(pat1 - pat2) + 1))
        )
    for pat1, pat2 in generalisations2:
        cost2 += math.log(
            # Difference in height
            abs(sorted_values[pat1][0] - sorted_values[pat2][0]) / 
            # d * (difference in position + 1)
            (d * (abs(pat1 - pat2) + 1))
        )
    if cost2 < cost1:
        generalisations1, generalisations2 = generalisations2, generalisations1
    print(len(generalisations1))
    for pat1, pat2 in generalisations1:
        print(patients[pat1], patients[pat2])
