import os

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, f'{os.path.basename(__file__).split(".")[0]}.input')

digits = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}


def first_number(s: str, from_left: bool) -> str:
    if s[0 if from_left else -1] in digits.values():
        return s[0 if from_left else -1]
    else:
        nr = None
        for nr_chr in [3, 4, 5]:
            if from_left:
                sub_s = s[:min(nr_chr, len(s))]
            else:
                sub_s = s[-min(nr_chr, len(s)):]
            nr = digits.get(sub_s, nr)
        return nr


def valve_value(s: str) -> int:
    first_l = None
    first_r = None
    for i in range(len(s)):
        if not first_l:
            first_l = first_number(s[i:], from_left=True)
        if not first_r:
            first_r = first_number(s[:len(s) - i], from_left=False)
        if first_l and first_r:
            break

    return int(first_l + first_r)


assert valve_value('1abc2') == 12
assert valve_value('pqr3stu8vwx') == 38
assert valve_value('a1b2c3d4e5f') == 15
assert valve_value('treb7uchet') == 77

assert valve_value('two1nine') == 29
assert valve_value('eightwothree') == 83
assert valve_value('abcone2threexyz') == 13
assert valve_value('xtwone3four') == 24
assert valve_value('4nineeightseven2') == 42
assert valve_value('zoneight234') == 14
assert valve_value('7pqrstsixteen') == 76
assert valve_value('2bbjt') == 22
assert valve_value('phonenjjmdzkbzftworjvcvn1eightwox') == 12

assert valve_value('eighthree') == 83
assert valve_value('sevenine') == 79
assert valve_value('one1onermlsevenseven') == 17

v_sum = 0
with open(input_file, 'r') as f:
    for line in f:
        line = line.strip()
        vs = valve_value(line)
        print(f'{vs} ; {line}')
        v_sum += vs

print(v_sum)
