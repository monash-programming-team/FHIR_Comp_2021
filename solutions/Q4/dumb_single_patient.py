import decimal
from dateutil import parser
from ..read_data import read_dataset

filepath = input()

data = read_dataset(filepath)

print("Ready!")

# How many test cases?
t = int(input())

value_code1 = "XXXX-X"
value_code2 = "XXXX-X"
value_code3 = "XXXX-X"

for case in range(1, t+1):
    pat_ids = list(map(int, input().split()))
    # vals[x][y] = patient y, value code x.
    vals = [
        [
            min([
                (parser.parse(obs.effective), decimal.Decimal(obs.value["value"])) 
                for obs_id in data['patients'][_id].observations 
                if (obs := data['observations'][obs_id]).code == value_code
            ])[1]
            for _id in pat_ids
        ]
        for value_code in [value_code1, value_code2, value_code3]
    ]
    print(len(vals[0]))
    for pid in pat_ids:
        print("C 0 P", pid)
