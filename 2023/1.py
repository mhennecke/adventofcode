import os
import re

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, f'{os.path.basename(__file__).split(".")[0]}.input')


def valve_value(s: str) -> int:
    s = re.sub(r'[a-z]', '', s)
    return int(s[0] + s[-1])


assert valve_value('1abc2') == 12
assert valve_value('pqr3stu8vwx') == 38
assert valve_value('a1b2c3d4e5f') == 15
assert valve_value('treb7uchet') == 77

s = 0
with open(input_file, 'r') as f:
    for line in f:
        s += valve_value(line.strip())


print(s)
