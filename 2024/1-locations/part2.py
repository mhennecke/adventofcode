import os

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> tuple[tuple[int], tuple[int]]:
    with open(file_name, 'r') as f:
        left, right = zip(*(map(int, line.split()) for line in f))
    return left, right


def similarity_score(left: tuple[int], right: tuple[int]) -> int:
    return sum(map(lambda x: x * right.count(x), left))


assert similarity_score(*read_data(test_input_file)) == 31

d = similarity_score(*read_data(input_file))
print(d)
