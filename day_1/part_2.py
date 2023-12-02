from pathlib import Path

INPUT_FILE = Path("input.txt")

NUMBER_MAP = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def find_numberlike_values(input_line):
    result = []
    i = 0
    while i < len(input_line):
        if input_line[i].isdigit():
            result.append(input_line[i])
            i += 1
            continue

        # you would think a regexp would be better here, but it's not
        # it consumes tokens that we might need in the case of overlapping words
        # so instead we use a simple loop / sliding window approach
        for word, number in NUMBER_MAP.items():
            if input_line[i : i + len(word)] == word:
                result.append(number)
                i += 1
                break
        else:
            i += 1

    return result


running_sum = 0
for line in INPUT_FILE.open().readlines():
    numbers = find_numberlike_values(line)
    if not numbers:
        continue
    running_sum += int(f"{numbers[0]}{numbers[-1]}")

print(running_sum)
