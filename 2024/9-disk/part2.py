import os

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> list[str]:
    with open(file_name, 'r') as f:
        return f.read().strip()


def file_checksum(start: int, length: int, weight: int) -> int:
    return sum(map(lambda d_i: d_i * weight, range(start, start + length)))


def compressed_checksum(data: str) -> int:
    checksum = 0
    assert len(data) % 2 == 1 # make sure, last element is a data element
    files = []
    spaces = []
    block_i = 0
    for i, d in enumerate(data):
        if i % 2 == 0:
            files.append((block_i, int(d), i // 2))
        else:
            if int(d) > 0:
                spaces.append((block_i, int(d)))
        block_i += int(d)

    for f in reversed(files):
        # find spot in spaces
        for s_i, s in enumerate(spaces):
            if s[0] > f[0]:
                # not a space left from file
                checksum += file_checksum(*f)
                break
            if f[1] <= s[1]:
                # fits
                checksum += file_checksum(s[0], f[1], f[2])
                spaces[s_i] = (s[0] + f[1], s[1] - f[1])
                if spaces[s_i][1] == 0:
                    spaces.pop(s_i)
                break
        else:
            # no space found
            checksum += file_checksum(*f)

    return checksum


assert compressed_checksum(read_data(test_input_file)) == 2858

d = compressed_checksum(read_data(input_file))
print(d)
