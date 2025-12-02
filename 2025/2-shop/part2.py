import os

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_files = [os.path.join(script_dir, f'test.input{i}') for i in range(1)]


def read_data(file_name: str) -> list[list[str]]:
    with open(file_name, 'r') as f:
        return list(map(lambda s: s.split('-'), f.readline().split(',')))


def invalid_ids(id_range: list[str]) -> list[int]:
    id_start = id_range[0]
    id_end = id_range[1]

    invalids = set()
    for digits in range(len(id_start), len(id_end) + 1):
        start = max(int(id_start), 10**(digits - 1))
        end = min(int(id_end), 10**digits - 1)
        for segment_len in range(1, digits):
            if digits % segment_len == 0:
                # is factor
                a = range(int(str(start)[:segment_len]), int(str(end)[:segment_len]) + 1)
                ids = map(lambda x: int(str(x) * (digits // segment_len)), a)
                ids_in_range = filter(lambda y: int(id_start) <= y and y <= int(id_end), ids)
                invalids.update(ids_in_range)

    return invalids


def sum_invalid_ids(data: list[list[str]]) -> int:
    invalids = list(map(lambda r: sum(invalid_ids(r)), data))
    return sum(invalids)


assert sum_invalid_ids(read_data(test_input_files[0])) == 4174379265

data = read_data(input_file)
print(sum_invalid_ids(data))
