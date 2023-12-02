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


def would_game_be_possible(game, bag):
    for draw in game:
        for cube in draw:
            if cube["color"] not in bag:
                return False
            if bag[cube["color"]] < cube["count"]:
                return False
    return True


def get_possible_games(games, bag):
    possible_games = []
    for game in games:
        if would_game_be_possible(games[game], bag):
            possible_games.append(game)
    return possible_games


bag = {"red": 12, "green": 13, "blue": 14}
games = parse_games("".join(lines))
possible_games = get_possible_games(games, bag)
print(sum(int(game.split(" ")[1]) for game in possible_games))
