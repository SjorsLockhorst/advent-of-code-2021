from typing import List, Tuple, Set

f = open("input.txt")


cave: List[List[int]] = []  # Init list to store cave in

for line in f:

    # Read row from file
    row = [int(row) for row in line.strip()]

    # Add 10's at beginning and end
    row.insert(0, 10)
    row.append(10)
    cave.append(row)

buffer_row = [10 for _ in range(len(cave[0]))]

cave.insert(0, buffer_row)
cave.append(buffer_row)


def get_bassin_neighbors(
    cave: List[List[int]], cursor: Tuple[int, int, int], seen: set
):
    """
    Get bassin neighbors based on criteria.
    It can not be seen already, and it has to be bigger relative to the cursor
    """
    i, j, val = cursor

    neighbors = [
        (i - 1, j, cave[i - 1][j]),
        (i + 1, j, cave[i + 1][j]),
        (i, j + 1, cave[i][j + 1]),
        (i, j - 1, cave[i][j - 1]),
    ]

    # Only return unseen neighbors that are les than the cursor
    return [pos for pos in neighbors if pos not in seen and pos[2] < 9 and val < pos[2]]


bassins: List[Set[Tuple[int, int, int]]] = []
seen = set()

# Loop over each position in the cave, except for the buffer
for i in range(1, len(cave) - 1):
    for j in range(1, len(cave[0]) - 1):

        current = cave[i][j]

        neighbors = [
            (-1, 0, cave[i - 1][j]),
            (1, 0, cave[i + 1][j]),
            (0, 1, cave[i][j + 1]),
            (0, -1, cave[i][j - 1]),
        ]

        # Check if current place in the cave is lowest relative to neighbors
        is_lowest = True
        for _, _, pos in neighbors:
            if current >= pos:
                is_lowest = False

        # If it is the lowest, it must be the end point of a basin
        if is_lowest:
            bassin = set()

            bassin_neighbors: List[Tuple[int, int, int]] = []

            # Init first element to start search from
            cursor = (i, j, current)
            bassin_neighbors.append(cursor)

            while len(bassin_neighbors) != 0:

                # Get first neighbor as current cursor
                cursor = bassin_neighbors.pop(0)

                # Make sure we never consider this cursor again
                seen.add(cursor)

                # Get current cursors valid neighbors
                bassin_neighbors += get_bassin_neighbors(cave, cursor, seen)

                # Add cursor to our basin
                bassin.add(cursor)

            # Append total basin to list of basins
            bassins.append(bassin)

# Get size of each basin in a list, sort in order of largest first
sizes = [len(bassin) for bassin in bassins]
sizes.sort(reverse=True)
answer = 1

# Get product of the size of the first three basins as the answer
for size in sizes[:3]:
    answer *= size

print(answer)
