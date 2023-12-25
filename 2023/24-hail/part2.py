import os
import numpy as np
from sympy import symbols, solve

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> np.ndarray:
    with open(file_name, 'r') as f:
        data = np.fromiter(f.read().replace('@', ',').replace('\n', ',').split(','), dtype=float).reshape(-1, 6)
    return data


def stone(hailstones) -> int:
    p1, v1 = np.split(hailstones[0, :], 2)
    p2, v2 = np.split(hailstones[1, :], 2)
    p3, v3 = np.split(hailstones[2, :], 2)

    syms = symbols('p_x0,py_0,p_z0,v_x0,v_y0,v_z0,t1,t2,t3')
    p0, v0 = np.split(np.array(syms[0:6]), 2)
    t1, t2, t3 = syms[6:]

    eq = np.block([
        p0 - p1 + t1 * (v0 - v1),
        p0 - p2 + t2 * (v0 - v2),
        p0 - p3 + t3 * (v0 - v3)
    ])

    s0 = solve(eq, *syms)[0]
    return sum(map(int, s0[0:3]))


test_data = read_data(test_input_file)
assert stone(test_data) == 47


data = read_data(input_file)
print(stone(data))
