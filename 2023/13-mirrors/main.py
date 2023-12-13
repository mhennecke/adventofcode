import os
import numpy as np
from typing import Callable

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> list[np.ndarray]:
    data = []
    with open(file_name, 'r') as f:
        valley = []
        for line in f:
            line = line.strip()
            if not line:
                data.append(np.array(valley, np.int8))
                valley = []
            else:
                valley.append([int(v == '#') for v in line])
        else:
            data.append(np.array(valley, np.int8))
    return data


def find_reflection(valley: np.ndarray, match: Callable[[np.ndarray, np.ndarray], bool]) -> int:
    for d in range(valley.ndim):
        v = np.rollaxis(valley, d)
        for i in range(1, v.shape[0]):
            w = min(i, v.shape[0] - i)    # width to compare
            a = v[max(0, i - w):i, :]     # left side of axis
            b = v[2 * i - 1:i - 1:-1, :]  # flipped right side of axis
            if match(a, b):
                return i * 100**(1 - d)
    raise AttributeError('no mirror axis')


def all_reflections(valleys: list[np.ndarray],  match: Callable[[np.ndarray, np.ndarray], bool]) -> int:
    return sum([find_reflection(v, match) for v in valleys])


test_data = read_data(test_input_file)
data = read_data(input_file)

# part 1
match_func = lambda a, b: np.all(a == b)  # perfect match
assert [find_reflection(v, match_func) for v in test_data] == [5, 400]
assert all_reflections(test_data, match_func) == 405

print(all_reflections(data, match_func))

# part 2
match_func = lambda a, b:  np.sum(a == b) == a.size - 1  # perfect match except 1?
assert [find_reflection(v, match_func) for v in test_data] == [300, 100]
assert all_reflections(test_data, match_func) == 400

print(all_reflections(data, match_func))
