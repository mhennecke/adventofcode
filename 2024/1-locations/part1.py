import os

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> tuple[tuple[int], tuple[int]]:
    with open(file_name, 'r') as f:
        left, right = zip(*(map(int, line.split()) for line in f))
    return left, right


def total_distance(left: tuple[int], right: tuple[int]) -> int:
    return sum(map(lambda x, y: abs(x - y), sorted(left), sorted(right)))


assert total_distance(*read_data(test_input_file)) == 11

d = total_distance(*read_data(input_file))
print(d)
