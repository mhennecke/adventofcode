import os
import re

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, f'{os.path.basename(__file__).split(".")[0]}.input')
test_input_file = os.path.join(script_dir, f'{os.path.basename(__file__).split(".")[0]}.test.input')


def read_data(file_name: str) -> list[str]:
    lines = []
    with open(file_name, 'r') as f:
        for line in f:
            line = line.strip()
            # add padding to simplify analysis
            if not lines:
                lines.append('.' * (len(line) + 2))
            assert len(line) + 2 == len(lines[0])
            lines.append(f'.{line}.')

    # pad end
    lines.append('.' * len(lines[0]))

    return lines


def part_numbers(schematic: list[str]) -> list[int]:
    numbers = []
    for i in range(1, len(schematic) - 1):
        assert len(schematic[i]) == len(schematic[0])
        re_sym = re.compile(r'^\.*[^\d\.]+\.*$')
        for nr in re.finditer(r'\d+', schematic[i]):
            if re_sym.match(schematic[i][nr.span()[0] - 1]) or \
              re_sym.match(schematic[i][nr.span()[1]]) or \
              re_sym.match(schematic[i - 1][nr.span()[0] - 1:nr.span()[1] + 1]) or \
              re_sym.match(schematic[i + 1][nr.span()[0] - 1:nr.span()[1] + 1]):
                numbers.append(int(nr[0]))

    return numbers


test_schematic = read_data(test_input_file)
assert sum(part_numbers(test_schematic)) == 4361

parts = read_data(input_file)
print(sum(part_numbers(parts)))
