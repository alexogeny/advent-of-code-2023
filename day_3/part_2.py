"""
--- Part Two ---

The engineer finds the missing part and installs it in the engine! As the engine springs to life, you jump in the closest gondola, finally ready to ascend to the water source.

You don't seem to be going very fast, though. Maybe something is still wrong? Fortunately, the gondola has a phone labeled "help", so you pick it up and the engineer answers.

Before you can explain the situation, she suggests that you look out the window. There stands the engineer, holding a phone in one hand and waving with the other. You're going so slowly that you haven't even left the station. You exit the gondola.

The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced.

Consider the same engine schematic again:

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

In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.
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
    gear_map = {}
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
                matching_symbol = next(
                    (x for x in indices_to_check if x in symbol_locations), None
                )
                if matching_symbol is not None:
                    part_numbers.append(int(current_number))
                    symbol_text = input[matching_symbol[0]][matching_symbol[1]]
                    if symbol_text == "*":
                        if matching_symbol not in gear_map:
                            gear_map[matching_symbol] = []
                        gear_map[matching_symbol].append(int(current_number))
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
                        symbol_text = input[symbol[0]][symbol[1]]
                        symbol_locations.append(symbol)
                        part_numbers.append(int(current_number))
                        if symbol_text == "*":
                            if symbol not in gear_map:
                                gear_map[symbol] = []
                            gear_map[symbol].append(int(current_number))
    gear_ratio_sum = 0
    for gear in gear_map:
        if len(gear_map[gear]) < 2:
            continue
        ratio = gear_map[gear][0]
        for multiplier in gear_map[gear][1:]:
            ratio *= multiplier
        gear_ratio_sum += ratio

    return gear_ratio_sum


print(find_and_sum_part_numbers(INPUT))
