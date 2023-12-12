import os
from itertools import combinations
import re

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> list[tuple[str, list[int]]]:
    data = []
    with open(file_name, 'r') as f:
        for line in f:
            line = line.strip()
            condition, groups = line.split(' ')
            data.append((condition, [int(g) for g in groups.split(',')]))
    return data


def valid_condition(condition: str, contiguous_groups: list[int]) -> bool:
    groups = [len(c) for c in condition.split('.') if c]
    return len(groups) == len(contiguous_groups) and all([g1 == g2 for g1, g2 in zip(groups, contiguous_groups)])


def arrangements(condition: str, contiguous_groups: list[int]) -> int:
    possible_arrangements = []

    all_q = list(re.finditer(r'\?', condition))

    nr_target_h = sum(contiguous_groups)
    nr_h = len([1 for c in condition if c == '#'])
    nr_q = len([1 for c in condition if c == '?'])

    nr_h_to_distribute = nr_target_h - nr_h
    for h_indices in combinations(list(range(nr_q)), nr_h_to_distribute):
        c = list(condition)
        for h_index in h_indices:
            c[all_q[h_index].span()[0]] = '#'
        c = ['.' if c_ == '?' else c_ for c_ in c]
        if valid_condition(''.join(c), contiguous_groups):
            possible_arrangements.append(c)

    return len(possible_arrangements)


def sum_arrangements(records: list[tuple[str, list[int]]]) -> int:
    return sum([arrangements(*r) for r in records])


assert valid_condition('##.#', [2, 1])
assert valid_condition('.##.#.#', [2, 1, 1])
assert not valid_condition('.##.#', [2, 1, 1])
assert not valid_condition('.#.#.#', [2, 1, 1])

test_data = read_data(test_input_file)
assert [arrangements(*r) for r in test_data] == [1, 4, 1, 1, 4, 10]
assert sum_arrangements(test_data) == 21


data = read_data(input_file)
print(sum_arrangements(data))
