import os
from functools import reduce

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> list[str]:
    data = []
    with open(file_name, 'r') as f:
        data = f.read().splitlines()
    return data


def code(lines: list[str]) -> str:
    codes = {-1+1j: '1',  1j: '2',  1+1j: '3',  -1: '4', 0: '5',  1: '6',  -1-1j: '7',  -1j: '8', 1-1j: '9'}
    dirs = {'R': 1, 'U': 1j, 'L': -1, 'D': -1j}
    pos: complex = 0
    digits = ''

    for line in lines:
        for c in line:
            if not abs(pos + dirs[c]) > 1.5:
                pos += dirs[c]
        digits += codes[pos]
    return digits


assert code(read_data(test_input_file)) == '1985'

print(code(read_data(input_file)))
