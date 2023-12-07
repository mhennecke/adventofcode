import os
import parse
import operator


script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')


def read_data(file_name: str) -> list[dict]:
    data = []
    with open(file_name, 'r') as f:
        for line in f:
            line = line.strip()
            p = {}
            props = line.split(': ', 1)[1]
            for prop in props.split(', '):
                p_name, p_value = parse.parse('{:w}: {:d}', prop)
                p[p_name] = p_value
            data.append(p)
    return data


def match_aunt(tape: dict[int], remembered: dict[int], ops: dict[__builtins__]) -> bool:
    return all(map(lambda item: item[0] in tape and ops[item[0]](item[1], tape[item[0]]), remembered.items()))


aunt_sue = {
    'children': 3,
    'cats': 7,
    'samoyeds': 2,
    'pomeranians': 3,
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 5,
    'trees': 3,
    'cars': 2,
    'perfumes': 1,
}
ops = dict(zip(aunt_sue.keys(), [operator.eq] * len(aunt_sue)))
ops['cats'] = operator.gt
ops['trees'] = operator.gt
ops['pomeranians'] = operator.lt
ops['goldfish'] = operator.lt

data = read_data(input_file)
for i, d in enumerate(data):
    if match_aunt(aunt_sue, d, ops):
        print(i + 1)
        #break
