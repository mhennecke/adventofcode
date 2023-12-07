import os
import parse
import numpy as np


script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> (list[str], np.array):
    format_string = '{:w}: capacity {:d}, durability {:d}, flavor {:d}, texture {:d}, calories {:d}'

    ingredients = []
    data = []
    with open(file_name, 'r') as f:
        for line in f:
            d = parse.parse(format_string, line.strip())
            ingredients.append(d[0])
            data.append([*d[1:]])
    return np.asarray(data)


def score(ingredients: np.array, teaspoons: np.array, properties: slice = slice(4)) -> int:
    assert teaspoons.sum() == 100
    mix = teaspoons.T * ingredients[:, properties]
    return np.clip(mix.sum(axis=0), 0, None).prod()


test_data = read_data(test_input_file)
assert score(test_data, np.array([[44, 56]])) == 62842880

data = read_data(input_file)
max_score = 0
for i in range(101):
    for j in range(101 - i):
        for k in range(101 - i - j):
            for m in range(101 - i - j - k):
                if i + j + k + m == 100:
                    s = score(data, np.array([[i, j, k, m]]))
                    if s > max_score:
                        max_score = s
print(max_score)
