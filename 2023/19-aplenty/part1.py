import os
from typing import Callable


script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> tuple[dict[str, Callable[[int, int, int, int], str]], list[list[int]]]:
    parts = []
    workflows = {}
    with open(file_name, 'r') as f:
        workflows_, parts_ = f.read().split('\n\n')
        workflows_ = workflows_.splitlines()
        parts_ = parts_.splitlines()

        for w in workflows_:
            w_name = w[:w.find('{')]
            w_steps = w[w.find('{') + 1:-1]

            l_func = 'lambda x, m, a, s: '
            for w_step in w_steps.split(','):
                if ':' in w_step:
                    condition, w_target = w_step.split(':')
                    l_func += f'"{w_target}" if {condition} else '
                else:
                    # assume: always last
                    l_func += f'"{w_step}"'
            workflows[w_name] = eval(l_func)

        for p in parts_:
            parts.append([int(p_[2:]) for p_ in p[1:-1].split(',')])

    return workflows, parts


def sum_ratings_accepted_parts(workflows: dict[str, Callable[[int, int, int, int], str]], parts: list[list[int]]) -> int:
    sum_ratings = 0
    for p in parts:
        state = 'in'
        while state != 'A' and state != 'R':
            state = workflows[state](*p)
        if state == 'A':
            sum_ratings += sum(p)
    return sum_ratings


test_data = read_data(test_input_file)
assert sum_ratings_accepted_parts(*test_data) == 19114


data = read_data(input_file)
print(sum_ratings_accepted_parts(*data))
