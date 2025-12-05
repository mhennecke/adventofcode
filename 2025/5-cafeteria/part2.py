import os

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_files = [os.path.join(script_dir, f'test.input{i}') for i in range(1)]


def read_data(file_name: str) -> list[tuple[int, int]]:
    with open(file_name, 'r') as f:
        lines = f.read().splitlines()
        ranges = []
        for line in lines:
            if line == '':
                break
            ranges.append(tuple(map(int, line.split('-'))))
        return ranges


def potential_fresh_ingredients(ranges: list[tuple[int, int]]) -> int:
    nr_fresh = 0
    sorted_ranges = sorted([(interval[0], 'l') for interval in ranges] + [(interval[1], 'u') for interval in ranges])

    ranges_stack = []
    lower_bound = 0
    for b in sorted_ranges:
        if b[1] == 'l':
            if ranges_stack == []:
                lower_bound = b[0]
            ranges_stack.append(b)
        else:
            ranges_stack.pop()
            if ranges_stack == []:
                nr_fresh += b[0] - lower_bound + 1
    return nr_fresh


assert potential_fresh_ingredients(read_data(test_input_files[0])) == 14

data = read_data(input_file)
print(potential_fresh_ingredients(data))
