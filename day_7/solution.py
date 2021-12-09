import math

f = open("input.txt")
# f = open("test.txt")

inputs = [int(string) for string in f.readline().strip().split(",")]


def part_1():
    least_error = 10000000000
    for i in range(max(inputs) + 1):
        err = 0

        for num in inputs:
            err += abs(num - i)

        if err < least_error:
            least_error = err

    print(least_error)


def part_2():
    def calc_fuel(num: int) -> int:
        return int((num * (num + 1)) / 2)

    input_map = {}

    for num in inputs:
        if not num in input_map:
            input_map[num] = 1
        else:
            input_map[num] += 1

    least_error = 10000000000000

    for i in range(max(input_map)):
        err = 0

        for num in input_map:
            err += calc_fuel(abs(num - i)) * input_map[num]

        if err < least_error:
            least_error = err

    print(least_error)


part_2()
