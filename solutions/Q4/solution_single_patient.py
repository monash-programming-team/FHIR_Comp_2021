import decimal
import datetime

filepath = input()

data = read_dataset(filepath)

print("Ready!")

# How many test cases?
t = int(input())

for case in range(1, t+1):
    pat_ids = input().split()
    print(len(pat_ids))
    for pid in pat_ids:
        print("C 0 P", pid)