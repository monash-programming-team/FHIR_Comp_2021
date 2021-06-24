import datetime
import decimal

filepath = input()

data = read_dataset(filepath)

print("Ready!")

# How many test cases?
t = int(input())

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
    required_distance = sum(max(v) - min(v) for v in vals)
    print(1)
    print("C", required_distance, "P", " ".join(pat_ids))
