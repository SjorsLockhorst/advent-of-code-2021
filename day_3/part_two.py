class LifeSupportRatingFinder:
    def __init__(self, selected_bit: int, path: str = "input.txt"):
        """Open file from path, parse to inputs and init selected bit"""
        f = open(path)
        self.inputs = [line.strip() for line in f]
        if not selected_bit == 0 or selected_bit == 1:
            raise Exception(f"selected_bit arg must be 0 or 1, not {selected_bit}")

        self.selected_bit = selected_bit

    def select_bit(self, most_common_bit: int):
        """
        Select bit based on the selected bit.
        Selects least common bit if selected bit == 0,
        and most selected bit if selected bit == 1.
        """
        return abs(most_common_bit - (1 - self.selected_bit))

    def find(self):
        """Wrapper for the recursive method _find."""
        return self._find(self.inputs, 0)

    def _find(self, inputs, i):
        """
        Recursive function to find the result to the puzzle.
        Takes inputs, checks each input at position i if the bit is either
        most or least common. Then drops all that do not match the selected bit, and
        recursively call itself untill only 1 number remains.
        """
        if len(inputs) > 1:
            half = len(inputs) / 2
            bit_amount = 0
            for entry in inputs:
                bit_amount += int(entry[i])
            most_common_bit = int(bit_amount >= half)
            selected_bit = self.select_bit(most_common_bit)
            inputs = [entry for entry in inputs if int(entry[i]) == selected_bit]
            i += 1
            return self._find(inputs, i)
        return int(inputs[0], 2)


oxygen_generator_finder = LifeSupportRatingFinder(1)
co_2_generator_finder = LifeSupportRatingFinder(0)

print(oxygen_generator_finder.find() * co_2_generator_finder.find())
