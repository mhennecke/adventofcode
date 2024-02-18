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
    codes = {
        2j: '1',
        -1+1j: '2',
        1j: '3',
        1+1j: '4',
        -2: '5',
        -1: '6',
        0: '7',
        1: '8',
        2: '9',
        -1-1j: 'A',
        -1j: 'B',
        1-1j: 'C',
        -2j: 'D',
    }
    dirs = {'R': 1, 'U': 1j, 'L': -1, 'D': -1j}
    pos: complex = -2
    digits = ''

    for line in lines:
        for c in line:
            if not abs(pos + dirs[c]) > 2:
                pos += dirs[c]
        digits += codes[pos]
    return digits


assert code(read_data(test_input_file)) == '5DB3'

print(code(read_data(input_file)))
