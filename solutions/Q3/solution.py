import decimal
import datetime

filepath = input()

data = read_dataset(filepath)

print("Ready!")

# How many test cases?
tests = int(input())

value_code = "8302-2"

d = 0

def solve(patients):   
    sorted_values = sorted([
        (min([
            (datetime.datetime.fromisoformat(obs.effective), decimal.Decimal(obs.value["value"])) 
            for obs_id in data['patients'][_id].observations 
            if (obs := data['observations'][obs_id]).code == value_code
        ])[1], _id)
        for _id in patients
    ])[::-1]

    cur_left = 0
    generalisations = []

    for cur_right in range(1, len(sorted_values)):
        # Is this next patient too steep?
        height_diff = sorted_values[cur_right-1][0] - sorted_values[cur_right][0]
        if height_diff < 2 * d:
            # Better to keep apart - Smooth.
            generalisations.append((cur_left, cur_right))
            cur_left = cur_right
    
    if cur_left != len(sorted_values) - 1:
        generalisations.append((cur_left, len(sorted_values)-1))
    
    return list(map(lambda x: x[1], sorted_values)), generalisations

for x in range(tests):
    d, n = list(map(int, input().split()))
    patients, generalisations = solve(input().split())
    print(len(generalisations))
    for l, r in generalisations:
        print(patients[l], patients[r])
