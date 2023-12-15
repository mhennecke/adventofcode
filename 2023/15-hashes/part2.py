import os

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> list[tuple[str, list[int]]]:
    data = []
    with open(file_name, 'r') as f:
        data = f.read().splitlines()[0].split(',')
    return data


def seq_hash(sequence: str, seed: int = 0) -> int:
    h = seed
    for c in sequence:
        h = (h + ord(c)) * 17 % 256
    return h


def hashmap(sequences: list[str]) -> int:
    boxes = {i: {} for i in range(265)}
    for seq in sequences:
        op = seq[-1]
        label = seq[:-1] if op == '-' else seq[:-2]
        box = seq_hash(label)

        if op == '-':
            if label in boxes[box]:
                del boxes[box][label]
        else:
            focal_length = int(op)
            boxes[box][label] = focal_length

    return sum(
        [sum([(i + 1) * (slot + 1) * lens for slot, lens in enumerate(box.values())])
            for i, box in boxes.items()])


assert seq_hash('HASH') == 52
test_data = read_data(test_input_file)
assert hashmap(test_data) == 145


data = read_data(input_file)
print(hashmap(data))
