# Solution idea:
# Relatively simple, you can waste the first seven days just figuring out what days of the week the rats are in the machine.
# After that, just binary search!
import datetime
import decimal

value_code = "29463-7"

filepath = input()

data = read_dataset(filepath)

patients_sorted = sorted([
    (max([
        (datetime.datetime.fromisoformat(obs.effective), decimal.Decimal(obs.value["value"])) 
        for obs_id in data['patients'][_id].observations 
        if (obs := data['observations'][obs_id]).code == value_code
    ])[1], _id)
    for _id in data['patients']
])

print("Ready!")

# How many test cases?
n = int(input())

def find_strongest_safe(ids, other, expect_low=True):
    # First, figure out when the result is trusted / not trusted.
    truth = [None] * 7
    for x in range(7):
        print("Q", other)
        res = input()
        # XOR
        # Should be DANGEROUS if low.
        truth[x] = int(res == "SAFE") + int(expect_low) == 1
    # Now binary search.
    lo = 0
    hi = len(ids)
    idx = 0
    bad = False
    while hi - lo > 1:
        mid = (hi + lo) // 2
        print("Q", ids[mid])
        res = input()
        if res == "FINISH":
            bad = True
            break
        # XOR
        # If telling the truth, SAFE means go lower.
        if int(truth[idx]) + int(res == "SAFE") != 1:
            hi = mid
        else:
            lo = mid
        idx = (idx+1) % 7
    return bad, ids[lo]

for x in range(n):
    in1, in2 = list(map(float, input().split()))
    l, r = None, None
    for y in range(len(patients_sorted)):
        if patients_sorted[y][0] >= in1 and l is None:
            l = y
        if patients_sorted[y][0] <= in2:
            r = y
    if l > 0:
        other = patients_sorted[0][1]
        bad, patient = find_strongest_safe(list(map(lambda x: x[1], patients_sorted[l:r+1])), other, expect_low=True)
    else:
        other = patients_sorted[-1][1]
        bad, patient = find_strongest_safe(list(map(lambda x: x[1], patients_sorted[l:r+1])), other, expect_low=False)
    if bad:
        continue
    print("A", patient)
