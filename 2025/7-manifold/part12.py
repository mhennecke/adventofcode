import os

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_files = [os.path.join(script_dir, f'test.input{i}') for i in range(1)]


def read_data(file_name: str) -> list[list[str]]:
    with open(file_name, 'r') as f:
        return f.read().splitlines()


def tachyons(manifold: list[list[str]]) -> tuple[int, int]:
    beams = {manifold[0].index('S'): 1}
    splits = 0
    for row in manifold[2::2]:
        new_beams = {}
        for beam, count in beams.items():
            if row[beam] == '^':
                new_beams[beam - 1] = new_beams.get(beam - 1, 0) + count
                new_beams[beam + 1] = new_beams.get(beam + 1, 0) + count
                splits += 1
            else:
                new_beams[beam] = new_beams.get(beam, 0) + count
        beams = new_beams
    return splits, sum(beams.values())


assert tachyons(read_data(test_input_files[0])) == (21, 40)

data = read_data(input_file)
print(tachyons(data))
