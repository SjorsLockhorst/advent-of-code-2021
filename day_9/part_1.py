from pprint import pprint
from typing import List

# f = open("test.txt")
f = open("input.txt")

cave: List[List[int]] = []

for line in f:
    row = [int(row) for row in line.strip()]
    row.insert(0, 10)
    row.append(10)
    cave.append(row)

buffer = [10 for _ in range(len(cave[0]))]

cave.insert(0, buffer)
cave.append(buffer)

total = 0
for i in range(1, len(cave) - 1):
    for j in range(1, len(cave[0]) - 1):
        current = cave[i][j]

        left = cave[i - 1][j]
        right = cave[i + 1][j]
        up = cave[i][j + 1]
        down = cave[i][j - 1]

        if current < left and current < right and current < up and current < down:
            total += 1 + current
