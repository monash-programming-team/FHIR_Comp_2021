filepath = input()

data = read_dataset(filepath)

print("Ready!")

# How many test cases?
n = int(input())

value_code = "32623-1"

def possible(patients, c_min, c_max):
    return (pow(c_max - c_min, 2) * patients) / 1000000 < 3

def solve(line):
    ids = line.split()
    print(len(ids))

for x in range(n):
    solve(input())