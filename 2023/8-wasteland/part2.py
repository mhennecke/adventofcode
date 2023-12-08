import os
import parse
import math
from itertools import cycle
from functools import reduce


script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input2')


def read_data(file_name: str) -> tuple[str, dict]:
    data = {}
    with open(file_name, 'r') as f:
        instructions = f.readline().strip()
        f.readline()
        for line in f:
            node, left, right = parse.parse('{:w} = ({:w}, {:w})', line.strip())
            data[node] = (left, right)
    return instructions, data


def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


def nr_steps(instructions, map_) -> int:
    nodes = [node for node in map_.keys() if node[2] == 'A']
    cycle_lenghts = [cycle_length(instructions, map_, node) for node in nodes]
    return reduce(lcm, cycle_lenghts, 1)


def cycle_length(instructions, map_, start='AAA') -> int:
    steps = 0
    node = start
    for direction in cycle(instructions):
        if steps and node[2] == 'Z':
            return steps
        if node[2] == 'Z' or steps:
            steps += 1
        node = map_[node][0 if direction == 'L' else 1]
    return steps


test_data = read_data(test_input_file)
assert nr_steps(*test_data) == 6

data = read_data(input_file)
print(nr_steps(*data))
