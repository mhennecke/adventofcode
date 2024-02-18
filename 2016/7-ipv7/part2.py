import os
import re

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input2')


def read_data(file_name: str) -> list[str]:
    return open(file_name, 'r').read().splitlines()


def supports_ssl(ip: str) -> bool:
    m1 = re.search(r'\[[a-z]*([a-z])(?!\1)([a-z])\1[a-z]*\]([a-z]+\[[a-z]+\])*[a-z]*(\2\1\2)', ip)
    m2 = re.search(r'([a-z])(?!\1)([a-z])\1[a-z]*(\[[a-z]+\][a-z]+)*\[[a-z]*(\2\1\2)', ip)
    return bool(m1 or m2)


def nr_supports_tls(ips: list[str]) -> int:
    return sum(map(supports_ssl, ips))
    

assert nr_supports_tls(read_data(test_input_file)) == 3

print(nr_supports_tls(read_data(input_file)))
