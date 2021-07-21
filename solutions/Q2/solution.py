"""
Solution uses DP. After sorting patients by priority:
DP[x][y] = With `y` "changes to Eye Color", how big of a contiguous subset, ending at index `x`, can we create that contains no duplicates != "changes to Eye Color".
COST[x][y] = COST of covering everything up to index `x`, allowing `y` "changes to Eye Color" at some point in time.
So solution is COST[z][max_k], where `z` is the last patient index.
O(n*(k^2))
"""

import datetime

filepath = input()

data = read_dataset(filepath)

print("Ready!")

# How many test cases?
t = int(input())

value_code = "94235-3"

DP = [[None for _ in range(11)] for _ in range(200001)]
COST = [[None for _ in range(11)] for _ in range(200001)]

for case in range(t):
    n, max_k, D, C = list(map(int, input().split()))
    prac_ids = input().split()
    patient_ids = list(set(sum([data['practitioners'][_id].patients for _id in prac_ids], start=[])))
    vals = list(sorted([
        (max([
            (datetime.datetime.fromisoformat(obs.effective), obs.value["value"]) 
            for obs_id in data['patients'][_id].observations 
            if (obs := data['observations'][obs_id]).code == value_code
        ]), _id)
        for _id in patient_ids
    ]))
    vals = [v[0][1] for v in vals]

    index = 0
    seen = {}
    for i in range(len(vals)):
        if vals[i] not in seen:
            seen[vals[i]] = index
            index += 1
        # Turn each string into an index, to speed things up.
        vals[i] = seen[vals[i]]

    for x in range(len(vals)+1):
        for y in range(max_k+1):
            DP[x][y] = None
            COST[x][y] = None

    for k in range(0, max_k+1):
        left, right = len(vals) - 1, len(vals) - 1
        counts = {}
        for v in vals:
            counts[v] = 0
        counts[vals[-1]] += 1
        changes = 0
        while right >= 0:
            while left >= 1 and changes <= k:
                left -= 1
                counts[vals[left]] += 1
                # Do we need a change to fit this?
                if counts[vals[left]] > 1:
                    changes += 1
            if changes <= k:
                # Left included. At the end of the list.
                DP[right][k] = right - left + 1
            else:
                # Best we can do from right is to left but not including!
                DP[right][k] = right - left
            counts[vals[right]] -= 1
            # Have we removed the need for a change?
            if counts[vals[right]] > 0:
                changes -= 1
            right -= 1

    for k in range(0, max_k+1):
        for i in range(0, len(vals)):
            best_cost = (D + C) * (len(vals)+1)
            for j in range(0, k+1):
                # Try using a divider with j changes.
                length = DP[i][j]
                best_cost = min(best_cost,
                    (COST[i-length][k-j] if i >= length else -D) + C * j + D
                )
            COST[i][k] = best_cost


    print(COST[len(vals)-1][max_k])
    

