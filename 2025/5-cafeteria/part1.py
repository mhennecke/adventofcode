import os

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_files = [os.path.join(script_dir, f'test.input{i}') for i in range(1)]


def read_data(file_name: str) -> tuple[list[tuple[int, int]], list[int]]:
    with open(file_name, 'r') as f:
        lines = f.read().splitlines()
        ranges = []
        ids = []
        for line in lines:
            if line == '':
                continue
            t = tuple(map(int, line.split('-')))
            if len(t) == 2:
                ranges.append(t)
            elif len(t) == 1:
                ids.append(t[0])
        return ranges, ids


def fresh_ingredients(ranges: list[tuple[int, int]], ingredients: list[int]) -> int:
    nr_fresh = 0
    for ingredient in ingredients:
        for r in ranges:
            if r[0] <= ingredient <= r[1]:
                nr_fresh += 1
                break
    return nr_fresh


assert fresh_ingredients(*read_data(test_input_files[0])) == 3

data = read_data(input_file)
print(fresh_ingredients(*data))
