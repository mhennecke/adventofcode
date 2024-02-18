import os
from itertools import islice, groupby
from operator import itemgetter

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> list[tuple]:
    data = []
    with open(file_name, 'r') as f:
        for line in f:
            data.append((line[:-12], int(line[-11:-8]), line[-7:-2]))
    return data


def decrypt_shift(ciphertext: str, shift: int) -> str:
    return str.join('', map(lambda c: chr((ord(c) - ord('a') + shift) % 26 + ord('a')) if c != '-' else ' ', ciphertext))


def sector_id_northpole_objects(rooms: list[tuple]) -> int:
    for name, id, checksum in rooms:
        occurences = [(k, len(list(g))) for k, g in groupby(sorted(name.replace('-', '')))]
        top5_chars = str.join('', [c for c, _ in islice(sorted(occurences, key=itemgetter(1), reverse=True), 5)])

        if checksum == top5_chars:
            cleartext = decrypt_shift(name, id)
            if cleartext == 'northpole object storage':
                return id
    return None

assert decrypt_shift('qzmt-zixmtkozy-ivhz', 343) == 'very encrypted name'

print(sector_id_northpole_objects(read_data(input_file)))
