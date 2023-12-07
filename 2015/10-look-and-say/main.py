import re


def mutate(m: str) -> str:
    regex = r"(.)\1*"

    new = ''
    matches = re.finditer(regex, m, re.MULTILINE)
    for match in matches:
        sub = match.group(0)
        new += f'{len(sub)}{sub[0]}'
    return new


assert mutate('1') == '11'
assert mutate('11') == '21'
assert mutate('21') == '1211'
assert mutate('1211') == '111221'
assert mutate('111221') == '312211'

test_str = '1113222113'

res = test_str
for i in range(50):
    res = mutate(res)

print(len(res))
