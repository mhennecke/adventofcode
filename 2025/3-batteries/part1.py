import os

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_files = [os.path.join(script_dir, f'test.input{i}') for i in range(1)]


def read_data(file_name: str) -> list[str]:
    with open(file_name, 'r') as f:
        return f.read().splitlines()


def joltage(bank: str, nr_digits: int = 2) -> int:
    # max in bank[:-digit] 
    # jolt += max
    # bank = bank after max
    # repeat nr_digits times
    jolt = ''
    for digit in range(nr_digits, 0, -1):
        max_n = max(bank[:-digit + 1] if digit > 1 else bank)
        jolt += max_n
        bank = bank[bank.index(max_n) + 1:]
    return int(jolt)


def max_joltage(data: list[str]) -> int:
    return sum(map(joltage, data))


assert max_joltage(read_data(test_input_files[0])) == 357

data = read_data(input_file)
print(max_joltage(data))
