import os
import re

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input2')


def read_data(file_name: str) -> (list[tuple[str, str]], str):
    replacements = []
    saw_empty = False
    with open(file_name, 'r') as f:
        for line in f:
            line = line.strip()
            if saw_empty:
                input = line
                break
            if line == '':
                saw_empty = True
            else:
                replacements.append(tuple(line.split(' => ')))

    return (tuple(replacements), input)


def reduce_molecule(molecule: str, replacements: tuple[tuple[str, str]], pruning_max: int = 1000) -> int:
    reduction_candidates = dict()
    reduction_candidates[molecule] = 0

    while True:
        new_candidates = {}
        for replacement in replacements:
            for candidate_molecule in reduction_candidates:
                # replacement to 'e' only relevant if candidate molecule reduces directly to 'e':
                for m in re.finditer(replacement[1], candidate_molecule):
                    new_molecule = candidate_molecule[:m.span()[0]] + replacement[0] + candidate_molecule[m.span()[1]:]
                    if new_molecule == 'e':
                        return reduction_candidates[candidate_molecule] + 1
                    elif 'e' not in new_molecule:
                        new_candidates[new_molecule] = reduction_candidates[candidate_molecule] + 1

        # prune reductions set
        pruned_candidates = {}
        for i, item in enumerate(sorted(new_candidates.items(), key=lambda item: len(item[0]))):
            if i > pruning_max:
                break
            pruned_candidates[item[0]] = item[1]
        reduction_candidates = pruned_candidates


test_replacements, test_input = read_data(test_input_file)
assert reduce_molecule(test_input, test_replacements) == 6

replacements, input = read_data(input_file)
print(reduce_molecule(input, replacements))
