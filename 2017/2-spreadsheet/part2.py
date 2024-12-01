import os

from itertools import combinations

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input2')


def read_data(file_name: str) -> list[list[int]]:
    with open(file_name, 'r') as f:
        return list(map(lambda line: list(map(int, line.split())), f.readlines()))


def checksum(rows: list[list[int]]) -> int:
    def row_checksum(row: list[int]):
        return next(y // x for x, y in combinations(sorted(row), 2) if not y % x)

    return sum(map(row_checksum, rows))


assert checksum(read_data(test_input_file)) == 9


c = checksum(read_data(input_file))
print(c)
