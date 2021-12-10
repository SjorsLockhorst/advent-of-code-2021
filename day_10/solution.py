from math import floor
from typing import List

f = open("input.txt")
inputs = [line.strip() for line in f]

bracket_map = {"}": "{", ")": "(", ">": "<", "]": "["}

incomplete_lines = 0
total_syntax_err = 0

autocomplete_scores: List[int] = []
for line in inputs:

    chars: List[str] = []

    syntax_error = False
    i = 0

    while not syntax_error and i < len(line):

        char = line[i]
        if char in bracket_map.values():
            chars.append(char)
        else:
            check = chars.pop()
            if not check == bracket_map[char]:
                syntax_error = True

                if char == "}":
                    total_syntax_err += 1197
                elif char == ")":
                    total_syntax_err += 3
                elif char == "]":
                    total_syntax_err += 57
                elif char == ">":
                    total_syntax_err += 25137

        i += 1

    if not syntax_error and len(chars) != 0:
        incomplete_lines += 1
        total_autocomplete = 0
        while chars:
            to_close = chars.pop()
            total_autocomplete *= 5
            if to_close == "{":
                total_autocomplete += 3
            elif to_close == "(":
                total_autocomplete += 1
            elif to_close == "[":
                total_autocomplete += 2
            elif to_close == "<":
                total_autocomplete += 4
        autocomplete_scores.append(total_autocomplete)

autocomplete_scores.sort()
part_2 = autocomplete_scores[floor(len(autocomplete_scores) / 2)]

print(f"Answer part 1 {total_syntax_err}")
print(f"Answer part 2 {part_2}")
