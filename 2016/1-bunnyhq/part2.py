import os
from functools import reduce

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input2')


def read_data(file_name: str) -> list[str]:
    data = []
    with open(file_name, 'r') as f:
        data = f.readline().split(', ')
    return data


def hq_distance(moves: list[str]) -> int:
    pos: complex = 0
    visited = {pos}
    dir: complex = 1j
    for m in moves:
        dir *= 1j if m[0]=='L' else -1j
        for _ in range(int(m[1:])):
            pos += dir
            if pos in visited:
                return int(abs(pos.real) + abs(pos.imag))
            visited.add(pos)
    return None


assert hq_distance(['R8', 'R4', 'R4', 'R8']) == 4


data = read_data(input_file)
print(hq_distance(data))
