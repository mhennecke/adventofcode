import os


script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')


def get_string_size(s: str) -> (int, int):
    return (len(s), len(s.encode().decode('unicode_escape')) - 2)


assert get_string_size(r'""') == (2, 0)
assert get_string_size(r'"abc"') == (5, 3)
assert get_string_size(r'"aaa\"aaa"') == (10, 7)
assert get_string_size(r'"\x27"') == (6, 1)

res = 0
with open(input_file, 'r') as f:
    for line in f:
        line = line.strip()
        (nr_chars, nr_mem) = get_string_size(line)
        res += nr_chars - nr_mem

print(res)
