# This is an N^5 operation
# This doesn't solve the problem completely, as there are some edge case rectangle selections that get ignored.
# It does a pretty good job though.

import sys
import decimal
import datetime

sys.setrecursionlimit(1000)

filepath = input()

data = read_dataset(filepath)

print("Ready!")

# How many test cases?
t = int(input())

DP = [[[[None for _ in range(31)] for __ in range(31)] for ___ in range(31)] for ____ in range(31)]

def cost(x1, y1, x2, y2):
    return 10 + pow(float(abs(x2 - x1)) + float(abs(y2 - y1)), 1.5)

for case in range(1, t+1):
    pat_ids = input().split()
    # vals[x][y] = patient y, value code x.
    vals = [
        [
            (max([
                (datetime.datetime.fromisoformat(obs.effective), decimal.Decimal(obs.component[x]["valueQuantity"]["value"])) 
                for obs_id in data['patients'][_id].observations 
                if (obs := data['observations'][obs_id]).code == "55284-4"
            ])[1], _id)
            for _id in pat_ids
        ]
        for x in range(2)
    ]
    
    # Now map every point to a row / column based on position.
    dim_0_map = {}
    dim_0_positions = list(sorted([v for v in vals[0]], key=lambda x: x[0]))
    for i, (v, _id) in enumerate(dim_0_positions):
        dim_0_map[_id] = i
    dim_1_map = {}
    dim_1_positions = list(sorted([v for v in vals[1]], key=lambda x: x[0]))
    for i, (v, _id) in enumerate(dim_1_positions):
        dim_1_map[_id] = i
    x_pos = list(map(lambda x: x[0], dim_0_positions))
    y_pos = list(map(lambda x: x[0], dim_1_positions))

    filled = [[False for _ in range(len(y_pos))] for __ in range(len(x_pos))]

    # We have a mapping from _ids to indicies.
    for _id in pat_ids:
        filled[dim_0_map[_id]][dim_1_map[_id]] = True

    for x1 in range(len(DP)):
        for x2 in range(len(DP[0])):
            for x3 in range(len(DP[0][0])):
                for x4 in range(len(DP[0][0][0])):
                    DP[x1][x2][x3][x4] = None

    # DP[x1][y1][x2][y2] := Cost of covering everyone in the rectangle (x1, y1) -> (x2, y2) inclusive.
    # Start by setting the cost of each indivual square.
    for x in range(len(x_pos)):
        for y in range(len(y_pos)):
            if filled[x][y]:
                DP[x][y][x][y] = (cost(x_pos[x], y_pos[y], x_pos[x], y_pos[y]), "ME")
            else:
                DP[x][y][x][y] = (0, None)
    
    def solve(x1, y1, x2, y2):
        if DP[x1][y1][x2][y2] is not None:
            return DP[x1][y1][x2][y2]
        # One option: cover everything with one big rectangle.
        cur_best = cost(x_pos[x1], y_pos[y1], x_pos[x2], y_pos[y2])
        cur_rect = "ME"
        # Other option: Break up the rectangle in some way.
        for x in range(x1, x2):
            candidate = solve(x1, y1, x, y2)[0] + solve(x+1, y1, x2, y2)[0]
            if candidate < cur_best:
                cur_best = candidate
                cur_rect = ((x1, y1, x, y2), (x+1, y1, x2, y2))
        for y in range(y1, y2):
            candidate = solve(x1, y1, x2, y)[0] + solve(x1, y+1, x2, y2)[0]
            if candidate < cur_best:
                cur_best = candidate
                cur_rect = ((x1, y1, x2, y), (x1, y+1, x2, y2))
        DP[x1][y1][x2][y2] = (cur_best, cur_rect)
        return DP[x1][y1][x2][y2]

    # Populate all necessary DP spots.
    solve(0, 0, len(x_pos)-1, len(y_pos)-1)

    def generate_rects(root):
        path = DP[root[0]][root[1]][root[2]][root[3]][1]
        if path is None:
            return []
        elif path == "ME":
            return [root]
        else:
            return generate_rects(path[0]) + generate_rects(path[1])

    rects = generate_rects((0, 0, len(x_pos)-1, len(y_pos)-1))

    print(len(rects))
    for x1, y1, x2, y2 in rects:
        if x2 == x1 and y2 == y1:
            distance = 0
        else:
            distance = abs(x_pos[x2] - x_pos[x1]) + abs(y_pos[y2] - y_pos[y1])
        print("C", distance, "P", end="")
        for pat in pat_ids:
            if x1 <= dim_0_map[pat] <= x2 and y1 <= dim_1_map[pat] <= y2:
                print(" " + str(pat), end="")
        print("\n", end="")
