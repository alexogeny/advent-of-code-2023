import re
from pathlib import Path

INPUT_FILE = Path("input.txt")
NUMBERLIKE = re.compile(r"\d")


def get_numbers_as_string(line):
    if not NUMBERLIKE.findall(line):
        return ()
    first_number = NUMBERLIKE.findall(line)[0]
    last_number = NUMBERLIKE.findall(line)[-1]
    return first_number, last_number


running_sum = 0
for line in INPUT_FILE.open().readlines():
    first_number, last_number = get_numbers_as_string(line)
    if not first_number or not last_number:
        continue
    running_sum += int(f"{first_number}{last_number}")

print(running_sum)
