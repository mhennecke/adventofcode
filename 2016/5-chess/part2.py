import os
from hashlib import md5

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> str:
    return open(file_name, 'r').readline().strip()


def password(door_id: str) -> int:
    p = ['_'] * 8
    p_i = 0
    i = 0
    while p_i < 8:
        h = md5((door_id + str(i)).encode()).hexdigest()
        if h[:5] == '00000':
            pos = int(h[5], base=16)
            if pos < 8 and p[pos] == '_':
                p[pos] = h[6]
                p_i += 1
        i += 1
    return str.join('', p)

assert password(read_data(test_input_file)) == '05ace8e3'

print(password(read_data(input_file)))
