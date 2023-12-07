import os


script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')


def get_string_size(s: str) -> (int, int):
    # The length of the string as it is
    actual_length = len(s)

    # The length of the string it would be if it was encoded
    encoded_length = len(s.replace('\\', '\\\\').replace('"', '\\"')) + 2

    return (actual_length, encoded_length)


assert get_string_size(r'""') == (2, 6)
assert get_string_size(r'"abc"') == (5, 9)
assert get_string_size(r'"aaa\"aaa"') == (10, 16)
assert get_string_size(r'"\x27"') == (6, 11)

res = 0
with open(input_file, 'r') as f:
    for line in f:
        line = line.strip()
        (nr_chars, nr_mem) = get_string_size(line)
        res += nr_mem - nr_chars

print(res)
