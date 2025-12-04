import os
import math

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_files = [os.path.join(script_dir, f'test.input{i}') for i in range(1)]


def read_data(file_name: str) -> list[str]:
    with open(file_name, 'r') as f:
        return f.read().splitlines()


def accessible_paperrolls(data: list[str], iterations: int) -> int:
    directions = [(0, 1), (1, 0), (1, 1), (1, -1), (-1, 0), (0, -1), (-1, -1), (-1, 1)]
    data_extended = []
    data_extended.append('.' * (len(data[0]) + 2))
    for line in data:
        data_extended.append('.' + line + '.')
    data_extended.append('.' * (len(data[0]) + 2))
    total_accessible = 0
    while iterations > 0:
        nr_accessible = 0
        for y in range(1, len(data_extended) - 1):
            for x in range(1, len(data_extended[0]) - 1):
                if data_extended[y][x] == '@':
                    if len(list(filter(lambda p: p in ['@', 'x'], (data_extended[y + dy][x + dx] for dx, dy in directions)))) < 4:
                        nr_accessible += 1
                        data_extended[y] = data_extended[y][:x] + 'x' + data_extended[y][x + 1:]

        if nr_accessible == 0:
            break
        else:
            total_accessible += nr_accessible
            for y in range(1, len(data_extended) - 1):
                for x in range(1, len(data_extended[0]) - 1):
                    if 'x' in data_extended[y][x]:
                        data_extended[y] = data_extended[y].replace('x', '.')
        iterations -= 1
    return total_accessible


assert accessible_paperrolls(read_data(test_input_files[0]), 1) == 13
assert accessible_paperrolls(read_data(test_input_files[0]), math.inf) == 43

data = read_data(input_file)
print(accessible_paperrolls(data, 1))
print(accessible_paperrolls(data, math.inf))
