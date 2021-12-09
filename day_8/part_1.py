f = open("input.txt")


def part_1():
    signal_patterns = []
    outputs = []

    for line in f:
        values = line.strip().split("|")

        signal_patterns.append([num for num in values[0].split(" ") if num])

        outputs.append([num for num in values[1].split(" ") if num])

    unique_amounts = [2, 4, 3, 7]

    total = 0

    for vals in outputs:
        for val in vals:
            if len(val) in unique_amounts:
                total += 1

    print(total)
