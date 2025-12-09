import math
import os
import itertools

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_files = [os.path.join(script_dir, f'test.input{i}') for i in range(1)]


def read_data(file_name: str) -> list[tuple[int, int]]:
    with open(file_name, 'r') as f:
        return [tuple(map(int, line.split(','))) for line in f.read().splitlines()]


def largest_tile(tiles: list[tuple[int, int]]) -> int:
    pairs = itertools.combinations(tiles, 2)
    areas = sorted((math.prod([abs(a-b)+1 for a, b in list(zip(p1, p2))]) for p1, p2 in pairs))
    return areas[-1]


assert largest_tile(read_data(test_input_files[0])) == 50

data = read_data(input_file)
print(largest_tile(data))
