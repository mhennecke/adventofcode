import os

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> tuple[list[tuple[int, int]], list[list[int]]]:
    rules = []
    updates = []
    with open(file_name, 'r') as f:
        for line in f:
            if '|' in line:
                rules.append(tuple(map(int, line.split('|'))))
            elif ',' in line:
                updates.append(list(map(int, line.split(','))))
    return rules, updates


def is_valid_update(rules: list[tuple[int, int]], update: list[int]) -> bool:
    for i in range(len(update) - 1):
        u = update[i]
        u_next = update[i + 1]
        if not (u, u_next) in rules:
            return False
    return True


def fix_update(rules: list[tuple[int, int]], update: list[int]) -> list[int]:
    for i in range(len(update) - 1):
        u = update[i]
        u_next = update[i + 1]
        if not (u, u_next) in rules:
            assert (u_next, u) in rules
            update[i + 1] = u
            update[i] = u_next
    if is_valid_update(rules, update):
        return update
    return fix_update(rules, update)


def middle_page(update: list[int]) -> int:
    return update[len(update) // 2]


def sum_middle_pages_of_fixed_updates(rules: list[tuple[int, int]], updates: list[list[int]]) -> int:
    invalid_updates = filter(lambda u: not is_valid_update(rules, u), updates)
    fixed_updates = list(map(lambda u: fix_update(rules, u), invalid_updates))
    return sum(map(middle_page, fixed_updates))


assert sum_middle_pages_of_fixed_updates(*read_data(test_input_file)) == 123


d = sum_middle_pages_of_fixed_updates(*read_data(input_file))
print(d)
