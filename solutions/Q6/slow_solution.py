# Stress that each test is independent.
import datetime
import decimal

value_code = "718-7"

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

# We don't actually use any data for this problem.
print("Ready!")

# How many test cases?
n = int(input())

# We can solve this with the least number of test cases like so:

LEFT = "LEFT"
RIGHT = "RIGHT"
EQUAL = "EQUAL"

def find1(nums):
    # Find the single weighed coin among a list of coins
    if len(nums) == 1:
        return nums[0]
    elif len(nums) <= 3:
        print("Q 1 1", nums[0], nums[1])
        res = input()
        if res == LEFT:
            return nums[0]
        elif res == RIGHT:
            return nums[1]
        return nums[2]
    size = len(nums)//3
    print(f"Q {size} {size}", " ".join(nums[:2*size]))
    res = input()
    if res == LEFT:
        return find1(nums[:size])
    elif res == RIGHT:
        return find1(nums[size:2*size])
    return find1(nums[2*size:])

def find2(nums):
    if len(nums) == 2:
        return nums[0], nums[1]
    elif len(nums) <= 5:
        print("Q 1 1", nums[0], nums[1])
        res = input()
        if res == LEFT:
            return nums[0], find1(nums[2:])
        elif res == RIGHT:
            return nums[1], find1(nums[2:])
        print("Q 1 1", nums[0], nums[2])
        res = input()
        if res == LEFT:
            return nums[0], nums[1]
        elif res == RIGHT:
            return nums[2], find1(nums[3:])
        return find2(nums[3:])
    size = len(nums)//6
    print(f"Q {2*size} {2*size}", " ".join(nums[:4*size]))
    res = input()
    if res == LEFT:
        # Nothing in RHS
        return find2(nums[:2*size] + nums[4*size:])
    elif res == RIGHT:
        # Nothing in LHS
        return find2(nums[2*size:])
    # Both here or both not.
    print(f"Q {size} {size}", " ".join(nums[:2*size]))
    res = input()
    if res == LEFT:
        return find1(nums[:size]), find1(nums[2*size:4*size])
    elif res == RIGHT:
        return find1(nums[size:2*size]), find1(nums[2*size:4*size])
    return find2(nums[4*size:])


for x in range(n):
    in1, in2 = list(map(float, input().split()))
    l, r = None, None
    for y in range(len(patients_sorted)):
        if patients_sorted[y][0] >= in1 and l is None:
            l = y
        if patients_sorted[y][0] <= in2:
            r = y
    ids = find2(list(map(lambda x: x[1], patients_sorted[l:r+1])))
    print("A", " ".join(ids))
