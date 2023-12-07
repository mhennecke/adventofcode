import os


script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> list[int]:
    data = []
    with open(file_name, 'r') as f:
        for line in f:
            data.append(int(line.strip()))
    return data


def container_combinations(liters: int, containers: list[int], containers_available: list[int], liters_target: int) -> list[list[int]]:
    if liters == liters_target:
        combinations = [containers]
    elif liters > liters_target:
        combinations = None
    else:
        combinations = []
        for i, c in enumerate(containers_available):
            remaining_containers = containers_available[i+1:]
            comb = container_combinations(liters + c, containers + [c], remaining_containers, liters_target)
            if comb:
                combinations += comb

    return combinations


def min_container_combinations(containers_available: list[int], liters_target: int) -> int:
    combinations = container_combinations(0, [], containers_available, liters_target)
    min_nr_containers = min(map(len, combinations))
    return len([c for c in combinations if len(c) == min_nr_containers])


test_data = read_data(test_input_file)
assert min_container_combinations(test_data, 25) == 3

data = read_data(input_file)
print(min_container_combinations(data, 150))
