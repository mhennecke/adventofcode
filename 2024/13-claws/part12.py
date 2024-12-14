import os
from parse import parse
import numpy as np

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> list[tuple[tuple[int, int], tuple[int, int], tuple[int, int]]]:
    machines = []
    with open(file_name, 'r') as f:
        while True:
            a_line = f.readline().strip()
            if not a_line:
                break
            ax, ay = parse('Button A: X+{:d}, Y+{:d}', a_line)
            bx, by = parse('Button B: X+{:d}, Y+{:d}', f.readline().strip())
            px, py = parse('Prize: X={:d}, Y={:d}', f.readline().strip())
            machines.append(((ax, ay), (bx, by), (px, py)))
            # skip empty line
            f.readline()
    return machines


def min_tokens(machine: list[tuple[tuple[int, int], tuple[int, int], tuple[int, int]]], p_correction: int, tokens_a: int = 3, tokens_b: int = 1) -> int:
    # ignores actual minimization problem of min(t_mn) over m, n but works here
    # assumes the only integer solution to the linear equation is optimal in terms of spent tokens
    (ax, ay), (bx, by), (px, py) = machine
    px += p_correction
    py += p_correction
    # Solving the system of equations x * A = c
    A = np.array([[ax, bx], [ay, by]])
    c = np.array([px, py])

    x = np.linalg.inv(A) @ c # linalg.solve(A, c) would work as well
    if np.allclose(x, x.round(), rtol=1e-15):
        return (x @ np.array([tokens_a, tokens_b])).round().astype(int)
    return 0


def sum_min_tokens(machines: list[list[tuple[tuple[int, int], tuple[int, int], tuple[int, int]]]], p_correction: int = 0) -> int:
    return sum(map(lambda m: min_tokens(m, p_correction), machines))


assert sum_min_tokens(read_data(test_input_file)) == 480

d = sum_min_tokens(read_data(input_file))
print(d)

d = sum_min_tokens(read_data(input_file), 10000000000000)
print(d)
