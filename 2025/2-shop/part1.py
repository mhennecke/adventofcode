import os

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_files = [os.path.join(script_dir, f'test.input{i}') for i in range(1)]


def read_data(file_name: str) -> list[list[str]]:
    with open(file_name, 'r') as f:
        return list(map(lambda s: s.split('-'), f.readline().split(',')))


def invalid_ids(id_range: list[str]) -> list[int]:
    id_start_s = id_range[0]
    id_start = int(id_start_s)
    id_end_s = id_range[1]
    id_end = int(id_end_s)

    invalids = []
    id = id_start
    id_s = id_start_s
    while id <= id_end:
        if len(id_s) % 2 != 0:
            # odd -> can't be invalid
            id_s = '1' + (len(id_s) - 1) * '0' + '1'
            id = int(id_s)
            if id > id_end:
                break

        left_s = id_s[:len(id_s)//2]
        right_s = id_s[len(id_s)//2:]
        if left_s == right_s:
            invalids.append(id)
            increment = 1
        else:
            increment = left_s < right_s

        new_left_s = str(int(left_s) + increment)
        id_s = 2 * new_left_s
        id = int(id_s)

    return invalids


def sum_invalid_ids(data: list[list[str]]) -> int:
    invalids = list(map(lambda r: sum(invalid_ids(r)), data))
    print(list(zip(data, invalids)))
    return sum(invalids)


assert sum_invalid_ids(read_data(test_input_files[0])) == 1227775554

data = read_data(input_file)
print(sum_invalid_ids(data))
