import os

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> list[int]:
    with open(file_name, 'r') as f:
        return list(map(int, f.readlines()))


def steps(jump_offsets: list[int]) -> int:
    i = 0
    s = 0
    while 0 <= i < len(jump_offsets):
        s += 1
        offset = jump_offsets[i]
        jump_offsets[i] += 1 if offset < 3 else -1
        i += offset
    return s


assert steps(read_data(test_input_file)) == 10

s = steps(read_data(input_file))
print(s)
