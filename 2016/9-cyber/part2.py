import os
import re

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> str:
    return open(file_name, 'r').readline()


def decrompessed_length(data: str) -> int:
    m: re.Match = re.search(r'\(([x0-9]*)\)', data)
    if m:
        l, t = map(int, m.group(1).split('x'))
        return m.start() + t * decrompessed_length(data[m.end():m.end() + l]) + decrompessed_length(data[m.end() + l:])
    else:
        return len(data)
        

assert decrompessed_length('ADVENT') == 6
assert decrompessed_length('A(1x5)BC') == 7
assert decrompessed_length('(3x3)XYZ') == 9
assert decrompessed_length('A(2x2)BCD(2x2)EFG') == 11
assert decrompessed_length('(6x1)(1x3)A') == 3
assert decrompessed_length('X(8x2)(3x3)ABCY') == 20
assert decrompessed_length('(27x12)(20x12)(13x14)(7x10)(1x12)A') == 241920
assert decrompessed_length('(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN') == 445

print(decrompessed_length(read_data(input_file)))
