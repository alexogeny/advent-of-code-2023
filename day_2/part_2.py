from pathlib import Path

INPUT_FILE = Path("input.txt")

lines = INPUT_FILE.open().readlines()


def parse_games(input_text):
    games = input_text.split("Game ")[1:]

    parsed_data = {}

    for game in games:
        game_number, game_data = game.split(":", 1)

        draws = game_data.strip().split(";")

        parsed_draws = []
        for draw in draws:
            cubes = draw.strip().split(",")

            parsed_cubes = []
            for cube in cubes:
                count, color = cube.strip().split(" ")
                parsed_cubes.append({"count": int(count), "color": color})

            parsed_draws.append(parsed_cubes)

        parsed_data["Game " + game_number.strip()] = parsed_draws

    return parsed_data


def minimum_cubes_needed_for_game(game):
    minimum_cubes = {}
    for draw in game:
        for cube in draw:
            if cube["color"] not in minimum_cubes:
                minimum_cubes[cube["color"]] = 0
            if cube["count"] > minimum_cubes[cube["color"]]:
                minimum_cubes[cube["color"]] = cube["count"]
    return minimum_cubes


def power_of_cubes(minimum_cubes):
    power = 1
    for color in minimum_cubes:
        power *= minimum_cubes[color]
    return power


bag = {"red": 12, "green": 13, "blue": 14}
games = parse_games("".join(lines))
minimum_cubes_for_games = [minimum_cubes_needed_for_game(games[game]) for game in games]
power_of_cubes_for_games = [
    power_of_cubes(minimum_cubes) for minimum_cubes in minimum_cubes_for_games
]
print(sum(power_of_cubes_for_games))
