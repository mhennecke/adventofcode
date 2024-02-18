import os
from operator import itemgetter
from itertools import batched

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> list[tuple]:
    data = []
    with open(file_name, 'r') as f:
        data = list(batched(map(int, f.read().split()), 3))
    return data


def valid_triangles(triangles: list[tuple]) -> int:
    checks = [
        itemgetter(0, 1, 2),
        itemgetter(0, 2, 1),
        itemgetter(1, 2, 0)
    ]
    valid = 0
    for triangle in triangles:
        valid += all(map(lambda check: sum(check(triangle)[:2]) > check(triangle)[2], checks))
    return valid

assert valid_triangles([[5, 10, 25]]) == 0

print(valid_triangles(read_data(input_file)))
