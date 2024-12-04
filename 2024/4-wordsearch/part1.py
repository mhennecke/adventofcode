import os

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> list[str]:
    with open(file_name, 'r') as f:
        return f.read().splitlines()


def nr_words(words: list[str], search_word: str = 'XMAS') -> int:
    nr_words = 0
    directions = [(0, 1), (1, 0), (1, 1), (1, -1), (-1, 0), (0, -1), (-1, -1), (-1, 1)]
    for y in range(len(words)):
        for x in range(len(words[y])):
            if words[y][x] == search_word[0]:
                for dx, dy in directions:
                    try:
                        indices = map(lambda i: (y + i * dy, x + i * dx), range(1, len(search_word)))
                        if any(map(lambda i: i[0] < 0 or i[1] < 0, indices)):
                            raise IndexError
                        word = map(lambda i: words[y + i * dy][x + i * dx], range(1, len(search_word)))
                        nr_words += ''.join(word) == search_word[1:]
                    except IndexError:
                        pass
    return nr_words


test_data = read_data(test_input_file)
assert nr_words(test_data) == 18


d = nr_words(read_data(input_file))
print(d)
