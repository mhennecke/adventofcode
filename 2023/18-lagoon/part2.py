import os
import numpy as np

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> list[tuple[str, list[int]]]:
    data = []
    with open(file_name, 'r') as f:
        for line in f:
            data.append(line.strip().split(' '))
    return data


def lagoon_size(dig_map: list[tuple[str, str, str]]) -> int:
    directions = {
        '0': 1,
        '1': -1j,
        '2': -1,
        '3': 1j,
    }

    steps = []
    for _, _, c in dig_map:
        steps.append(int(c[2:-2], 16) * directions[c[-2]])
    vertices = np.cumsum(steps)
    x = np.int64(vertices.real)
    y = np.int64(vertices.imag)
    # greens theorem -> Triangle formula: 2A = sum_{i=1}^n det(v_i | v_{i+1}) = x^T y' - y^T x'
    # where x' = (x_n, x_0, x_1, ..., x_{n-1}
    # where y' = (y_n, y_0, y_1, ..., y_{n-1}
    # here, we need to add half of the circumference + 1 to accomodate for trenches outside (positive) boundary
    circumference = sum(np.abs(steps))

    return int(np.abs(x.T @ np.roll(y, 1) - y.T @ np.roll(x, 1)) / 2 + circumference / 2 + 1)


test_data = read_data(test_input_file)
assert lagoon_size(test_data) == 952408144115


data = read_data(input_file)
print(lagoon_size(data))
