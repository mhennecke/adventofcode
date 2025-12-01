import os

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_files = [os.path.join(script_dir, f'test.input{i}') for i in range(1)]


def read_data(file_name: str) -> list[int]:
    with open(file_name, 'r') as f:
        return list(map(lambda s: -1 * int(s[1:]) if s[0] == 'L' else int(s[1:]), f.read().splitlines()))


def password(data: list[int], dial_start: int = 50, clicks: int = 100) -> int:
    dial = dial_start
    nr_zeros = 0
    for i in range(len(data)):
        steps = data[i]
        dial_new = dial + steps
        nr_zeros += abs(dial_new // clicks - dial // clicks)
        if steps < 0:
            # starting from 0?
            nr_zeros -= dial % clicks == 0
            # ending on zero?
            nr_zeros += dial_new % clicks == 0
        dial = dial_new

    return nr_zeros


assert password([50]) == 1
assert password([-50, -5]) == 1
assert password([-50]) == 1
assert password([51]) == 1
assert password([150]) == 2
assert password([151]) == 2
assert password(read_data(test_input_files[0])) == 6


data = read_data(input_file)
print(password(data))
