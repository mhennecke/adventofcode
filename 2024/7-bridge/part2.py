import os

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> list[tuple[int, list[int]]]:
    equations = []
    with open(file_name, 'r') as f:
        for line in f:
            s, v = line.strip().split(': ')
            equations.append((int(s), list(map(int, v.split(' ')))))
    return equations


def is_possible(equation: tuple[int, list[int]], running_value: int = None) -> bool:
    s, values = equation

    if s < (running_value or 0):
        return False

    if len(values) == 0:
        return s == running_value

    v = values[0]
    return is_possible((s, values[1:]), (running_value or 1) * v) or \
        is_possible((s, values[1:]), (running_value or 0) + v) or \
        is_possible((s, values[1:]), int(str((running_value or '')) + str(v)))


def calibrations(equations: list[tuple[int, list[int]]]) -> int:
    return sum([e[0] for e in filter(is_possible, equations)])


assert calibrations(read_data(test_input_file)) == 11387

d = calibrations(read_data(input_file))
print(d)
