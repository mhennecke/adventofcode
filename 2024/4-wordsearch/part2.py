import os

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> list[str]:
    with open(file_name, 'r') as f:
        return f.read().splitlines()


def nr_mas(words: list[str]) -> int:
    nr_mas = 0
    directions = [(1, 1), (1, -1)]
    for y in range(1, len(words) - 1):
        for x in range(1, len(words[y]) - 1):
            if words[y][x] == 'A':
                is_xmas = [False] * len(directions)
                for i, dir in enumerate(directions):
                    dx, dy = dir
                    indices = map(lambda i: (x + i * dx, y + i * dy), range(-1, 2))
                    word = ''.join(map(lambda xy_i: words[xy_i[1]][xy_i[0]], indices))
                    is_xmas[i] = word == 'MAS' or word == 'SAM'
                nr_mas += all(is_xmas)

    return nr_mas


test_data = read_data(test_input_file)
assert nr_mas(test_data) == 9


d = nr_mas(read_data(input_file))
print(d)
# 1815