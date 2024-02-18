import os
import re

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> list[str]:
    return open(file_name, 'r').read().splitlines()


def supports_tls(ip: str) -> bool:
    parts = re.split(r'[\[\]]', ip)
    abbas = list(map(lambda p: bool(re.search(r'(.)(?!\1)(.)\2\1', p)), parts))
    return any(abbas[::2]) and not any(abbas[1::2])

def nr_supports_tls(ips: list[str]) -> int:
    return sum(map(supports_tls, ips))
    

assert nr_supports_tls(read_data(test_input_file)) == 2

print(nr_supports_tls(read_data(input_file)))
# 38 wrong
