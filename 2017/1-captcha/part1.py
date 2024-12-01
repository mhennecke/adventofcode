import os

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')


def read_data(file_name: str) -> str:
    with open(file_name, 'r') as f:
        data = f.readline().strip()
    return data


def captcha(s: str) -> int:
    res = 0
    for (i, c) in enumerate(s):
        if s[(i + 1) % len(s)] == c:
            res += int(c)
    return res


assert captcha('1122') == 3
assert captcha('1111') == 4
assert captcha('1234') == 0
assert captcha('91212129') == 9

c = captcha(read_data(input_file))
print(c)