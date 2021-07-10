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
    # Find the two weighted coins among a list of coins

    # First handle the small cases
    if len(nums) == 2:
        return nums
    elif len(nums) == 3:
        print("Q 1 1", nums[0], nums[1])
        res = input()
        if res == LEFT:
            return nums[0], nums[2]
        elif res == RIGHT:
            return nums[1], nums[2]
        return nums[0], nums[1]
    elif len(nums) == 4:
        print("Q 2 2", " ".join(nums))
        res = input()
        if res == LEFT:
            return nums[0], nums[1]
        elif res == RIGHT:
            return nums[2], nums[3]
        return find1(nums[:2]), find1(nums[2:])
    elif len(nums) == 5:
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
        return nums[3], nums[4]
    
    # Now, break into sixths
    size = len(nums) // 6
    a1 = nums[:size]
    a2 = nums[size:2*size]
    b1 = nums[2*size:3*size]
    b2 = nums[3*size:4*size]
    c1 = nums[4*size:5*size]
    c2 = nums[5*size:6*size]
    leftover = nums[6*size:]
    # Weigh a against b
    print(f"Q {2*size} {2*size}", " ".join(a1 + a2 + b1 + b2))
    res = input()
    if res == LEFT:
        # None in b
        print(f"Q {2*size} {2*size}", " ".join(a1 + c1 + a2 + c2))
        res = input()
        if res == LEFT:
            # Both in a1 + c1.
            return find2(a1 + c1 + leftover)
        elif res == RIGHT:
            # Both in a2 + c2
            return find2(a2 + c2 + leftover)
        # 3 options: 
        # a1 a2
        # a1 c2
        # c1 a2
        print(f"Q {size} {size}", " ".join(a1 + a2))
        res = input()
        if res == LEFT:
            return find1(a1), find1(c2)
        elif res == RIGHT:
            return find1(a2), find1(c1)
        return find1(a1), find1(a2)
    elif res == RIGHT:
        # None in a
        print(f"Q {2*size} {2*size}", " ".join(b1 + c1 + b2 + c2))
        res = input()
        if res == LEFT:
            # None in b2, c2, a1, a2.
            return find2(b1 + c1 + leftover)
        elif res == RIGHT:
            # None in b1, c1, a1, a2.
            return find2(b2 + c2 + leftover)
        # 3 options: 
        # b1 b2
        # b1 c2
        # c1 b2
        print(f"Q {size} {size}", " ".join(b1 + b2))
        res = input()
        if res == LEFT:
            return find1(b1), find1(c2)
        elif res == RIGHT:
            return find1(b2), find1(c1)
        return find1(b1), find1(b2)
    # Equal - 1 in a, 1 in b or 2 in c + leftovers
    print(f"Q {2*size} {2*size}", " ".join(a1 + b1 + c1 + c2))
    res = input()
    if res == LEFT:
        return find1(a1 + a2), find1(b1 + b2)
    elif res == RIGHT:
        return find2(c1 + c2 + leftover)
    # Either 1 in a2, 1 in b2, or both in leftover.
    print(f"Q {size} {size}", " ".join(a1 + a2))
    res = input()
    if res == RIGHT:
        return find1(a2), find1(b2)
    else:
        # left not possible
        return find2(leftover)

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