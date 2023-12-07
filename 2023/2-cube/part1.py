import os
import parse

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> list[dict]:
    games = []
    with open(file_name, 'r') as f:
        for line in f:
            line = line.strip()
            g = line.split(': ', 1)[1]
            rounds = []
            for round in g.split('; '):
                r = {}
                for color in round.split(', '):
                    c_value, c_name = parse.parse('{:d} {:w}', color)
                    r[c_name] = c_value
                rounds.append(r)
            games.append(rounds)

    return games


def valid_draw(draw: dict[int], bag: dict[int]) -> bool:
    return all([k in bag and v <= bag[k] for k, v in draw.items()])


def valid_game(game: list[dict[int]], bag: dict[int]) -> bool:
    return all([valid_draw(g, bag) for g in game])


test_games = read_data(test_input_file)
bag = {'red': 12, 'green': 13, 'blue': 14}

assert valid_game(test_games[0], bag)
assert valid_game(test_games[1], bag)
assert not valid_game(test_games[2], bag)
assert not valid_game(test_games[3], bag)
assert valid_game(test_games[4], bag)

games = read_data(input_file)
print(sum([i + 1 if valid_game(game, bag) else 0 for i, game in enumerate(games)]))
