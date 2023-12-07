"""
--- Day 3: Gear Ratios ---

You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you up to the water source, but this is as far as he can bring you. You go inside.

It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.

"Aaah!"

You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer to help.

The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?
"""

import re
from pathlib import Path

INPUT = Path("input.txt").open().readlines()
test_input = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..""".split("\n")

SYMBOL = re.compile(r"[^\d\.]")
NUMBER_PATTERN = re.compile(r"\d")


def find_and_sum_part_numbers(input: list[str]) -> int:
    input = [i.strip() for i in input]
    part_numbers = []
    scanned_number_indices = []
    symbol_locations = []
    for row, line in enumerate(input):
        for col, character in enumerate(line):
            if (
                character == "."
                or SYMBOL.match(character)
                or (row, col) in scanned_number_indices
            ):
                continue
            if NUMBER_PATTERN.match(character):
                current_number = f"{character}"
                current_indices = [(row, col)]
                next_col = col + 1
                while next_col < len(line) and NUMBER_PATTERN.match(line[next_col]):
                    current_number += f"{line[next_col]}"
                    current_indices += [(row, next_col)]
                    scanned_number_indices.append((row, next_col))
                    next_col += 1
                check_frame_row_start = max(0, row - 1)
                check_frame_row_end = min(len(input), row + 1)
                check_frame_col_start = max(0, col - 1)
                check_frame_col_end = min(len(line), current_indices[-1][1] + 1)
                indices_to_check = []
                for row_to_check in range(
                    check_frame_row_start, check_frame_row_end + 1
                ):
                    for col_to_check in range(
                        check_frame_col_start, check_frame_col_end + 1
                    ):
                        if (row_to_check, col_to_check) in current_indices:
                            continue
                        indices_to_check.append((row_to_check, col_to_check))

                if [x for x in indices_to_check if x in symbol_locations]:
                    part_numbers.append(int(current_number))
                else:
                    symbol = next(
                        (
                            (r, c)
                            for r, c in indices_to_check
                            if r < len(input)
                            and c < len(input[r])
                            and SYMBOL.match(input[r][c])
                        ),
                        None,
                    )
                    if symbol is not None:
                        symbol_locations.append(symbol)
                        part_numbers.append(int(current_number))
    return sum(part_numbers)


print(find_and_sum_part_numbers(INPUT))
