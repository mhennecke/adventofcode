import os
import functools

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> list[str]:
    with open(file_name, 'r') as f:
        return f.read().split()


@functools.cache
def change(s: str, i: int) -> int:
    if i == 0:
        return 1
    elif s == '0':
        nr = change('1', i - 1)
        return nr
    elif len(s) % 2 == 0:
        midp = len(s) // 2
        sl = s[:midp]
        sr = s[midp:].lstrip('0') or '0'
        return change(sl, i - 1) + change(sr, i - 1)
    else:
        return change(str(int(s) * 2024), i - 1)


def nr_stones(stones: list[str], iterations: int) -> int:
    nr = 0
    for s in stones:
        nr += change(s, iterations)
    return nr


assert nr_stones(read_data(test_input_file), 25) == 55312

d = nr_stones(read_data(input_file), 25)
print(d)
d = nr_stones(read_data(input_file), 75)
print(d)
