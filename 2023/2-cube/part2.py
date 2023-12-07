import os
import parse
import operator
from functools import reduce

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


def max_cubes(game: list[dict[int]]) -> dict[int]:
    m = {'red': 0, 'green': 0, 'blue': 0}
    for draw in game:
        m = {c: max(m[c], draw.get(c, 0)) for c in m}
    return m


test_games = read_data(test_input_file)
assert max_cubes(test_games[0]) == {'red': 4, 'green': 2, 'blue': 6}
assert max_cubes(test_games[1]) == {'red': 1, 'green': 3, 'blue': 4}
assert max_cubes(test_games[2]) == {'red': 20, 'green': 13, 'blue': 6}
assert max_cubes(test_games[3]) == {'red': 14, 'green': 3, 'blue': 15}
assert max_cubes(test_games[4]) == {'red': 6, 'green': 3, 'blue': 2}

games = read_data(input_file)
print(reduce(operator.add, map(lambda game: reduce(operator.mul, max_cubes(game).values(), 1), games), 0))
