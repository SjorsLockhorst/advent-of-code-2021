from typing import List

f = open("input.txt")

fishies = [int(x) for x in f.readline().strip().split(",")]


def part_1(n: int):
    def next_gen(fishies: List[int], gen: int = 1) -> List[int]:
        """
        Recursively finds the n'th generation of fishies.
        """

        if gen != n + 1:  # Only calculate next generation if not at last gen

            new_fishies: List[int] = []  # Place to store new generation

            n_new_fishies = 0  # Amount of new fishies to add

            for fish in fishies:  # Implementation of the rules of the fishies
                if fish == 0:
                    new_fishies.append(6)
                    n_new_fishies += 1
                else:
                    new_fishies.append(fish - 1)

            for _ in range(n_new_fishies):  # Finally adding new fishies to next gen
                new_fishies.append(8)

            return next_gen(
                new_fishies, gen=gen + 1
            )  # Recursive call to next generation

        return fishies  # At the last generation, just return the fishies

    return len(next_gen(fishies))


def part_2(n: int):
    def next_gen(fishies: List[int], gen: int = 1) -> List[int]:
        """
        Recursively finds n'th gen of fishies, in a smarter way using an array
        that stores the amount of fishies per digit.
        """

        if gen != n + 1:  # Stop if last gen has been found
            new_fishies = [0 for _ in range(9)]  # Store digits of new fishies

            gen_parents = fishies[0]  # Store fishies that are parents for new gen

            for i in range(8, -1, -1):  # Move each batch of fishies one position down
                new_fishies[i - 1] = fishies[i]

            new_fishies[6] += gen_parents  # Move parents to 6'th position
            new_fishies[8] = gen_parents  # Add children to 8'th position

            return next_gen(new_fishies, gen=gen + 1)  # Get next generation

        return fishies

    first_gen = [0 for _ in range(9)]  # Create place to store fishies

    for fish in fishies:  # Count amount of fishies per digit
        first_gen[fish] += 1

    return sum(next_gen(first_gen))  # Find amount of fishies in n'th generation


print(f"Part 1: {part_1(80)} \n")
print(f"Part 2 {part_2(256)}")
