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
    
    return list(map(lambda x: x[1], sorted_values)), [
        [x, x+1]
        for x in range(len(sorted_values)-1)
    ]

for x in range(tests):
    d, n = list(map(float, input().split()))
    n = int(n)
    patients, generalisations = solve(input().split())
    print(len(generalisations))
    for l, r in generalisations:
        print(patients[l], patients[r])
