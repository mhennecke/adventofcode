import os

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')


def read_data(file_name: str) -> list[list[str]]:
    with open(file_name, 'r') as f:
        return list(map(str.split, f.readlines()))


def is_valid_passphrase(phrases: list[str]) -> bool:
    return len(phrases) == len(set(phrases))


assert is_valid_passphrase("aa bb cc dd ee".split())
assert not is_valid_passphrase("aa bb cc dd aa".split())
assert is_valid_passphrase("aa bb cc dd aaa".split())

s = sum(map(is_valid_passphrase, read_data(input_file)))
print(s)
