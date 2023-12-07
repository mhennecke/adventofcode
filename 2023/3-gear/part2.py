import os
import re
import operator
from functools import reduce

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


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


def numbers(s: re.Match, nrs: list[re.Match]) -> list[int]:
    assert len(s[0]) == 1
    m = []
    for nr in nrs:
        if nr.span()[0] <= (s.span()[0] + 1) and s.span()[0] <= nr.span()[1]:
            m.append(int(nr[0]))
    return m


def gear_ratios(schematic: list[str]) -> list[int]:
    ratios = []
    for i in range(1, len(schematic) - 1):
        m_pre = list(re.finditer(r'\d+', schematic[i - 1]))
        m_post = list(re.finditer(r'\d+', schematic[i + 1]))
        for gear in re.finditer(r'\*', schematic[i]):
            left = schematic[i][:gear.span()[0]]
            right = schematic[i][gear.span()[1]:]
            m_left = re.search(r'\d+$', left)
            nr_left = [int(m_left[0])] if m_left else []
            m_right = re.search(r'^\d+', right)
            nr_right = [int(m_right[0])] if m_right else []

            nrs_pre = numbers(gear, m_pre)
            nrs_post = numbers(gear, m_post)
            nrs = nrs_pre + nr_left + nr_right + nrs_post
            if len(nrs) == 2:
                ratios.append(reduce(operator.mul, nrs, 1))

    return ratios


test_schematic = read_data(test_input_file)
assert sum(gear_ratios(test_schematic)) == 467835

parts = read_data(input_file)
print(sum(gear_ratios(parts)))
