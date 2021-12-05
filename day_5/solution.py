import re
from pprint import pprint
from math import sqrt
from dataclasses import dataclass
from typing import List

f = open("input.txt")

lines = [line.strip() for line in f]


@dataclass
class Coordinate:
    """Dataclass to store Coordinate."""

    x: int
    y: int

    def __sub__(self, other: "Coordinate") -> "Coordinate":
        """Definition for - opeartor for Coordinate."""
        return Coordinate(self.x - other.x, self.y - other.y)

    def get_line(self, other: "Coordinate", part: str = "two") -> List["Coordinate"]:
        """
        Get line between current coordinate and some other coordinate,
        supports modes to solve part 1 and 2.
        """
        coordinates: List[Coordinate] = []

        new = self - other

        if part == "one":

            new.x = abs(new.x)
            new.y = abs(new.y)
            base = None

            if new.x == 0:  # Line is vertical
                if self.y > other.y:
                    base = other
                else:
                    base = self

                for i in range(new.y + 1):
                    coordinates.append(Coordinate(base.x, base.y + i))

            elif new.y == 0:  # Line is horizontal
                if self.x > other.x:
                    base = other
                else:
                    base = self

                for i in range(new.x + 1):
                    coordinates.append(Coordinate(base.x + i, base.y))

            return coordinates

        if part == "two":

            x_diff = 0
            y_diff = 0

            if new.x > 0:
                x_diff = -1
            elif new.x < 0:
                x_diff = 1

            if new.y > 0:
                y_diff = -1
            elif new.y < 0:
                y_diff = 1

            for i in range(max(abs(new.x), abs(new.y)) + 1):
                new_x = other.x + new.x + x_diff * i
                new_y = other.y + new.y + y_diff * i

                coordinates.append(Coordinate(new_x, new_y))

            return coordinates

        raise NotImplementedError(
            f"Provided argument {part} does not have an existing implementation"
        )


SOLVE_PART = "one"

# Get max coordinate by getting max value in input
max_coordinate = int(max([max(re.split(",| -> ", l)) for l in lines])) + 1

# Generate x by y 'ocean' based on maximum coordinate that was found
ocean = [[0 for _ in range(max_coordinate)] for _ in range(max_coordinate)]

total_overlap = 0

for l in lines:
    coordinates = l.split(" -> ")  # Split by arrow to get first and second coordinate

    x1, y1 = [int(coordinate) for coordinate in coordinates[0].split(",")]
    x2, y2 = [int(coordinate) for coordinate in coordinates[1].split(",")]

    cor1 = Coordinate(x1, y1)  # Create first coordinate
    cor2 = Coordinate(x2, y2)  # Create second coordinate

    line = cor1.get_line(cor2, part=SOLVE_PART)  # Get line between coordinates

    for cor in line:
        # First instance that overlaps on this coordinate, add 1 to total
        if ocean[cor.x][cor.y] == 1:
            total_overlap += 1

        # Increment position in ocean with 1
        ocean[cor.x][cor.y] += 1


print(total_overlap)  # Let user know the final total amount of overlap
