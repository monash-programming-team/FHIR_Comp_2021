# This solution is n^2 * k
# As for every DP, we search until a collision is met
# In reality probably n^{3/2} given the test data.

import datetime

filepath = input()

data = read_dataset(filepath)

print("Ready!")

# How many test cases?
t = int(input())

value_code = "94235-3"

DP = [[None for _ in range(21)] for _ in range(200001)]

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

    # Actual solution part.
    for i in range(len(vals)+1):
        for k in range(max_k+1):
            DP[i][k] = None

    def solve(i, k):
        if DP[i][k] is not None:
            return DP[i][k]
        # What's the minimum cost, starting from index i and with k replacements remaining?
        current = set()
        best = len(vals) * (D + C + 1)
        used = 0
        for x in range(i, len(vals)):
            if vals[x] in current:
                # (i - x) already in current.
                best = min(best, C * used + D + solve(x, k - used))
                used += 1
                if used > k:
                    break
            current.add(vals[x])
        if used <= k:
            best = min(best, C * used)
        DP[i][k] = best
        return DP[i][k]

    print(solve(0, max_k))
    

