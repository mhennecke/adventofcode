import os

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> list[tuple[str, list[int]]]:
    data = []
    with open(file_name, 'r') as f:
        data = f.read().splitlines()
    return data


def total_load(platform: list[list[str]]) -> int:
    load = 0
    for c in range(len(platform[0])):
        nr_rocks = 0
        block = 0
        for r in range(len(platform)):
            state = platform[r][c]
            if state == '#':
                block = r + 1
                nr_rocks = 0
            elif state == 'O':
                load += len(platform) - block - nr_rocks
                nr_rocks += 1
    return load


test_data = read_data(test_input_file)
assert total_load(test_data) == 136


data = read_data(input_file)
print(total_load(data))
