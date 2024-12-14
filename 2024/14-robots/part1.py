from functools import reduce
from operator import mul
import os
from parse import parse


script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> list[tuple[complex, complex]]:
    robots = []
    with open(file_name, 'r') as f:
        for line in f:
            p_x, p_y, v_x, v_y = parse('p={:d},{:d} v={:d},{:d}', line.strip())
            robots.append((p_x + p_y * 1j, v_x + v_y * 1j))
    return robots


def safety_factor(robots: list[tuple[complex, complex]], height: int = 103, width: int = 101, simulate: int = 100) -> int:
    m_h = height // 2
    m_w = width // 2
    quadrants = [0] * 4
    for r in robots:
        p, v = r
        t = (p + v * simulate)
        x, y = (int(t.real % width), int(t.imag % height))
        if x == m_w or y == m_h:
            continue
        quadrants[int(x < m_w) + int(y < m_h) * 2] += 1
    return reduce(mul, quadrants, 1)


assert safety_factor(read_data(test_input_file), 7, 11) == 12

d = safety_factor(read_data(input_file))
print(d)
