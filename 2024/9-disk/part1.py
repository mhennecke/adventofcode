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
    last_i = len(data) - 1
    last_d = int(data[last_i])
    block_i = 0
    for i, d in enumerate(data):
        if i > last_i:
            # all data processed
            break
        if i == last_i:
            # last data element
            checksum += file_checksum(block_i, last_d, i // 2)
            break
        if i % 2 == 0:
            # do nothing, data already there
            checksum += file_checksum(block_i, int(d), i // 2)
            block_i += int(d)
        else:
            # fill space
            space = int(d)
            while space > 0:
                if space >= last_d:
                    # fits completely
                    space -= last_d
                    assert last_i % 2 == 0´
                    checksum += file_checksum(block_i, last_d, last_i // 2)
                    last_i -= 2
                    block_i += int(last_d)
                    last_d = int(data[last_i])
                else:
                    # fits partially
                    checksum += file_checksum(block_i, space, last_i // 2)
                    last_d -= space
                    block_i += space
                    space = 0
    return checksum


assert compressed_checksum(read_data(test_input_file)) == 1928

d = compressed_checksum(read_data(input_file))
print(d)
