import os

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> list[int]:
    with open(file_name, 'r') as f:
        return list(map(int, f.readline().split()))


def cycle_length(jump_offsets: list[int]) -> int:
    seen = {}
    c = 0
    while tuple(jump_offsets) not in seen.keys():
        seen[tuple(jump_offsets)] = c
        c += 1
        m = max(jump_offsets)
        i = jump_offsets.index(m)
        jump_offsets[i] = 0
        for j in range(m):
            jump_offsets[(i + j + 1) % len(jump_offsets)] += 1
    return c - seen[tuple(jump_offsets)]


assert cycle_length(read_data(test_input_file)) == 4

s = cycle_length(read_data(input_file))
print(s)
