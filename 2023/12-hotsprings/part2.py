import os
from functools import cache

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> list[tuple[str, list[int]]]:
    data = []
    with open(file_name, 'r') as f:
        for line in f:
            line = line.strip()
            condition, groups = line.split(' ')
            # add padding at the end to simplify
            multiple = 5
            data.append(('?'.join([condition] * multiple) + '.', tuple([int(g) for g in groups.split(',')] * multiple)))
    return data


@cache
def arrangements(condition: str, contiguous_groups: tuple[int], consecutive_hashes: int = 0) -> int:
    if not condition:
        # no left-overs allowed at the end
        return not contiguous_groups and consecutive_hashes == 0
    else:
        # abort early
        if contiguous_groups and contiguous_groups[0] < consecutive_hashes:
            return 0

    possible_arrangements = 0
    c0 = condition[0]
    if c0 == '#' or c0 == '?':
        possible_arrangements += arrangements(condition[1:], contiguous_groups, consecutive_hashes + 1)
    if (c0 == '.' or c0 == '?') and (contiguous_groups and contiguous_groups[0] == consecutive_hashes or consecutive_hashes == 0):
        possible_arrangements += arrangements(condition[1:], contiguous_groups[1:] if consecutive_hashes else contiguous_groups)
    return possible_arrangements


def sum_arrangements(records: list[tuple[str, list[int]]]) -> int:
    return sum([arrangements(*r) for r in records])


test_data = read_data(test_input_file)
assert [arrangements(*r) for r in test_data] == [1, 16384, 1, 16, 2500, 506250]
assert sum_arrangements(test_data) == 525152


data = read_data(input_file)
print(sum_arrangements(data))
