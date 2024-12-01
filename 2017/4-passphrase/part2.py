import os

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')


def read_data(file_name: str) -> list[list[str]]:
    with open(file_name, 'r') as f:
        return list(map(str.split, f.readlines()))


def is_valid_passphrase(phrases: list[str]) -> bool:
    phrases_sorted = map(lambda p: ''.join(sorted(p)), phrases)
    return len(phrases) == len(set(phrases_sorted))


assert is_valid_passphrase("abcde fghij".split())
assert not is_valid_passphrase("abcde xyz ecdab".split())
assert is_valid_passphrase("a ab abc abd abf abj".split())
assert is_valid_passphrase("iiii oiii ooii oooi oooo".split())
assert not is_valid_passphrase("oiii ioii iioi iiio".split())

s = sum(map(is_valid_passphrase, read_data(input_file)))
print(s)
