import math
import os
from parse import parse


script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_files = [os.path.join(script_dir, f'test.input{i}') for i in range(1)]


def read_data(file_name: str) -> list[tuple[int, list[int]]]:
    with open(file_name, 'r') as f:
        return [parse('{:d}x{:d}: {:d} {:d} {:d} {:d} {:d} {:d}', line).fixed for line in f.read().splitlines()[31:]]


def valid_regions(data: list[list[str]]) -> int:
    return sum([math.prod(d[:2]) >= 9 * sum(d[2:]) for d in data])


# assert valid_regions(read_data(test_input_files[0])) == 2

data = read_data(input_file)
print(valid_regions(data))
