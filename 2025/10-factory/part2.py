import os
import numpy as np

from scipy.optimize import linprog


script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_files = [os.path.join(script_dir, f'test.input{i}') for i in range(1)]


def read_data(file_name: str) -> list[tuple[str, str, str]]:
    def read_line(line: str) -> tuple[str, list[str], str]:
        fields = line.split(' ')
        return fields[0], fields[1:-1], fields[-1]

    with open(file_name, 'r') as f:
        return [read_line(line) for line in f.read().splitlines()]


def fewest_button_presses(machines: list[tuple[str, str, str]]) -> int:
    fewest = 0
    for _, buttons, joltage in machines:
        c = [1] * len(buttons)
        b = list(map(int, joltage[1:-1].split(',')))
        A = np.zeros((len(b), len(buttons)), dtype=int)
        for i, button in enumerate(buttons):
            idx = list(map(int, button[1:-1].split(',')))
            A[idx, i] = 1

        result = linprog(c, A_eq=A, b_eq=b, bounds=[(0, None)] * len(c), method='highs', integrality=[1] * len(c))

        fewest += int(result.fun)
    return fewest


assert fewest_button_presses(read_data(test_input_files[0])) == 33

data = read_data(input_file)
print(fewest_button_presses(data))
