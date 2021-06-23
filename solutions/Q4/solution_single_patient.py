import decimal
import datetime

filepath = input()

data = read_dataset(filepath)

print("Ready!")

# How many test cases?
t = int(input())

value_code1 = "XXXX-X"
value_code2 = "XXXX-X"

for case in range(1, t+1):
    pat_ids = input().split()
    # vals[x][y] = patient y, value code x.
    vals = [
        [
            min([
                (datetime.datetime.fromisoformat(obs.effective), decimal.Decimal(obs.component[x]["valueQuantity"]["value"])) 
                for obs_id in data['patients'][_id].observations 
                if (obs := data['observations'][obs_id]).code == "55284-4"
            ])[1]
            for _id in pat_ids
        ]
        for x in range(2)
    ]
    print(len(vals[0]))
    for pid in pat_ids:
        print("C 0 P", pid)
