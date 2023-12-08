import os
import parse

from itertools import cycle


script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> tuple[str, dict]:
    data = {}
    with open(file_name, 'r') as f:
        instructions = f.readline().strip()
        f.readline()
        for line in f:
            node, left, right = parse.parse('{:w} = ({:w}, {:w})', line.strip())
            data[node] = (left, right)
    return instructions, data


def nr_steps(instructions, map_, start='AAA', end='ZZZ') -> int:
    steps = 0
    node = start
    for direction in cycle(instructions):
        if node == end:
            break
        steps += 1
        node = map_[node][0 if direction == 'L' else 1]
    return steps


test_data = read_data(test_input_file)
assert nr_steps(*test_data) == 2

data = read_data(input_file)
print(nr_steps(*data))
