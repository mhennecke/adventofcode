import os
import re

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


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

    return (replacements, input)


def distinct_replacements(replacements: list[tuple[str, str]], molecule: str) -> set[str]:
    new_molecules = set()
    for replacement in replacements:
        for m in re.finditer(replacement[0], molecule):
            new_molecule = molecule[:m.span()[0]] + replacement[1] + molecule[m.span()[1]:]
            new_molecules.add(new_molecule)
    return new_molecules


test_replacements, test_input = read_data(test_input_file)
assert len(distinct_replacements(test_replacements, test_input)) == 4

replacements, input = read_data(input_file)
print(len(distinct_replacements(replacements, input)))
