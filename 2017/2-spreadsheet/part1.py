import os

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> list[list[int]]:
    with open(file_name, 'r') as f:
        return list(map(lambda line: list(map(int, line.split())), f.readlines()))


def checksum(rows: list[list[int]]) -> int:
    return sum(map(lambda row: abs(max(row) - min(row)), rows))


assert checksum(read_data(test_input_file)) == 18


c = checksum(read_data(input_file))
print(c)
