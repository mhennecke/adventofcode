import os
import parse
import itertools

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
input_2nd_file = os.path.join(script_dir, 'input2')
test_input_file = os.path.join(script_dir, 'test.input')

# Alice would lose 2 happiness units by sitting next to Bob.
# Alice would lose 62 happiness units by sitting next to Carol.
# Alice would gain 65 happiness units by sitting next to David.


def read_data(file_name: str) -> dict:
    format_string = '{:w} would {:w} {:d} happiness units by sitting next to {:w}.'

    data = {}
    with open(file_name, 'r') as f:
        for line in f:
            p_a, d, w, p_b = parse.parse(format_string, line.strip())
            data[(p_a, p_b)] = w if d == 'gain' else -w
    return data


def happiness(table: list[str], happiness_data: list[tuple]) -> int:
    h = 0
    for i, p in enumerate(table):
        h += happiness_data[(p, table[(i - 1) % len(table)])]
        h += happiness_data[(p, table[(i + 1) % len(table)])]

    return h


def max_happiness(data) -> (list[str], int):
    people = {}
    for d in data.keys():
        people[d[0]] = 0
        people[d[1]] = 0
    people = list(people.keys())

    max_happiness = 0
    max_h_order = None
    for perm in itertools.permutations(people[1:]):
        seating_order = [people[0]] + list(perm)
        h = happiness(seating_order, data)
        if h > max_happiness:
            max_happiness = h
            max_h_order = seating_order

    return (max_happiness, max_h_order)


assert happiness(
    ['David', 'Alice', 'Bob', 'Carol'],
    read_data(test_input_file)
    ) == 330


print(max_happiness(read_data(input_file)))
print(max_happiness(read_data(input_2nd_file)))
