import functools
import os

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_files = [os.path.join(script_dir, f'test.input{i}') for i in range(1)]


def read_data(file_name: str) -> tuple[list[str], list[str]]:
    with open(file_name, 'r') as f:
        towels = f.readline().strip().split(', ')
        f.readline()
        stripes = f.read().splitlines()
    return towels, stripes


class Onsen:
    def __init__(self, towels: list[str], designs: list[str]):
        self.towels = towels
        self.designs = designs
        self.design_towel_combinations = functools.cache(self.design_towel_combinations)  # instance method caching

    def design_towel_combinations(self, design: str, all_combinations: bool) -> int:
        d = 0
        for t in filter(lambda towel: design.startswith(towel), self.towels):
            d += len(design) == len(t) or self.design_towel_combinations(design[len(t):], all_combinations)
            if d and not all_combinations:
                break  # one valid design is enough
        return d

    def designs_towel_combinations(self, all_combinations: bool = False) -> int:
        return sum(map(lambda design: self.design_towel_combinations(design, all_combinations), self.designs))


assert Onsen(*read_data(test_input_files[0])).designs_towel_combinations() == 6

o = Onsen(*read_data(input_file))
d = o.designs_towel_combinations()
print(d)

d = o.designs_towel_combinations(all_combinations=True)
print(d)
