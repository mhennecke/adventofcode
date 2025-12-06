import os
import operator
from functools import reduce

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_files = [os.path.join(script_dir, f'test.input{i}') for i in range(1)]


def read_data(file_name: str) -> list[list[str]]:
    with open(file_name, 'r') as f:
        worksheet = map(str.split, f.read().splitlines())
        worksheet_transp = list(map(list, zip(*worksheet)))
        return worksheet_transp


def read_data2(file_name: str) -> list[list[str]]:
    with open(file_name, 'r') as f:
        worksheet_transp = list(map(list, zip(*f.read().splitlines())))
        worksheet_transp.append([' '])
        worksheet = []
        problem = []
        op = None
        for line in worksheet_transp:
            if problem == []:
                op = line[-1]
            if any(map(lambda x: x != ' ', line)):
                problem.append(str.join('', line[:-1]).strip())
            else:
                problem.append(op)
                worksheet.append(problem)
                problem = []

        return worksheet


def grand_total(worksheet: list[list[str]]) -> int:
    operators = {
        '*': operator.mul,
        '+': operator.add
    }
    return sum(reduce(operators[p[-1]], map(int, p[:-1])) for p in worksheet)


assert grand_total(read_data(test_input_files[0])) == 4277556
assert grand_total(read_data2(test_input_files[0])) == 3263827

data = read_data(input_file)
print(grand_total(data))

data = read_data2(input_file)
print(grand_total(data))
