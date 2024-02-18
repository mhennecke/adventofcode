import os
from functools import reduce

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')


def read_data(file_name: str) -> list[str]:
    data = []
    with open(file_name, 'r') as f:
        data = f.readline().split(', ')
    return data


def hq_distance(moves: list[str]) -> int:
    pos: complex = 0
    dir: complex = 1j
    for m in moves:
        dir *= 1j if m[0]=='L' else -1j
        pos += dir * int(m[1:])
    return int(abs(pos.real) + abs(pos.imag))


assert hq_distance(['R2', 'L3']) == 5
assert hq_distance(['R2', 'R2', 'R2']) == 2
assert hq_distance(['R5', 'L5', 'R5', 'R3']) == 12

data = read_data(input_file)
print(hq_distance(data))
