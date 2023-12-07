import os
import re

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')

nr_nice = 0


def is_nice(word):
    # It does not contain the strings ab, cd, pq, or xy, even if they are part of one of the other requirements.
    if 'ab' in word or 'cd' in word or 'pq' in word or 'xy' in word:
        return False

    # It contains at least three vowels (aeiou only), like aei, xazegov, or aeiouaeiouaeiou.
    if sum([word.count(vowel) for vowel in 'aeiou']) < 3:
        return False

    # It contains at least one letter that appears twice in a row, like xx, abcdde (dd), or aabbccdd (aa, bb, cc, or dd).
    if not re.search(r'(.)\1', word):
        return False

    return True


assert is_nice('ugknbfddgicrmopn')
assert is_nice('aaa')
assert not is_nice('jchzalrnumimnmhp')
assert not is_nice('haegwjzuvuyypxyu')
assert not is_nice('dvszwmarrgswjxmb')

with open(input_file, 'r') as f:
    for line in f:
        if is_nice(line.strip()):
            nr_nice += 1

print(nr_nice)
