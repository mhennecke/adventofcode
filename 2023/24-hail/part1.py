import os
import numpy as np
from itertools import combinations


script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> np.ndarray:
    with open(file_name, 'r') as f:
        data = np.fromiter(f.read().replace('@', ',').replace('\n', ',').split(','), dtype=float).reshape(-1, 6)
    return data


def intersections(hailstones, test_area) -> int:
    t_min, t_max = test_area
    nr_intersections = 0
    for i, j in combinations(range(hailstones.shape[0]), 2):
        nr_intersections += ray_intersection_in_area(hailstones[i, 0:2], hailstones[i, 3:5], hailstones[j, 0:2], hailstones[j, 3:5], test_area)
    return nr_intersections


def ray_intersection_in_area(a1, v1, a2, v2, test_area) -> bool:
    # a1 + v1*s = a2 + v2*t
    t_min, t_max = test_area
    A = np.vstack([v1, -v2]).T
    b = (a2 - a1).T
    if np.linalg.det(A):
        st = np.linalg.inv(A) @ b  # line parameters s and t
        p = a1 + v1 * st[0]
        return all(st >= 0) and all(t_min < p) and all(p < t_max)
    else:
        # no intersection
        return False


test_data = read_data(test_input_file)
assert intersections(test_data, (7, 27)) == 2


data = read_data(input_file)
print(intersections(data, (200000000000000, 400000000000000)))
