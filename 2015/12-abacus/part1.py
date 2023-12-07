import os
import json

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')


def find_total_sum(j):
    if isinstance(j, int):
        return j
    elif isinstance(j, dict):
        return sum(map(find_total_sum, j.values()))
    elif isinstance(j, list):
        return sum(map(find_total_sum, j))
    elif isinstance(j, str):
        return 0
    else:
        raise ValueError


with open(input_file, 'r') as f:
    data = json.load(f)


print(find_total_sum(data))
