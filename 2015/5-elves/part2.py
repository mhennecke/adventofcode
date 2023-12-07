import os
import re

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')

nr_nice = 0


def is_nice(word):

    # It contains a pair of any two letters that appears at least twice in the string without overlapping,
    # like xyxy (xy) or aabcdefgaa (aa), but not like aaa (aa, but it overlaps).
    if not re.search(r'(..).*\1', word):
        return False

    # It contains at least one letter which repeats with exactly one letter between them,
    # like xyx, abcdefeghi (efe), or even aaa.
    if not re.search(r'(.).\1', word):
        return False

    return True


assert is_nice('qjhvhtzxzqqjkmpb')
assert is_nice('xxyxx')
assert not is_nice('uurcxstgmygtbstg')
assert not is_nice('ieodomkazucvgmuy')

with open(input_file, 'r') as f:
    for line in f:
        if is_nice(line.strip()):
            nr_nice += 1

print(nr_nice)
