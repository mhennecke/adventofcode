import os
import re
from functools import reduce

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test2.input')


def read_data(file_name: str) -> str:
    with open(file_name, 'r') as f:
        return f.read().strip().replace('\n', '')


def mul_corrupted(memory: str) -> bool:
    memory = re.sub(r"don't\(\)(.*?)(do\(\)|$)", "", memory)
    matches = re.findall(r"mul\((\d+),(\d+)\)", memory)
    return reduce(lambda x, m: x + int(m[0]) * int(m[1]), matches, 0)


test_data = read_data(test_input_file)
assert mul_corrupted(test_data) == 48


d = mul_corrupted(read_data(input_file))
print(d)
