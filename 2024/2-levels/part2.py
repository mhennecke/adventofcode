import os
import itertools

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> list[list[int]]:
    with open(file_name, 'r') as f:
        return list(map(lambda line: list(map(int, line.split())), f.readlines()))


def is_safe_report(report: list[int], dampen: bool = True) -> bool:
    all_pos = None
    for i, (y1, y2) in enumerate(itertools.pairwise(report)):
        d = y2 - y1
        if d == 0 or abs(d) < 1 or abs(d) > 3:
            return dampen and is_dampend_report_safe(report)
        is_pos = True if d > 0 else False
        if all_pos is None:
            all_pos = is_pos
        else:
            if all_pos != is_pos:
                return dampen and is_dampend_report_safe(report)

    return True


def is_dampend_report_safe(report: list[int]) -> bool:
    return any(map(lambda i: is_safe_report(report[:i] + report[i+1:], False), range(len(report))))


def safe_reports(reports: list[list[int]]) -> int:
    return sum(map(is_safe_report, reports))


test_data = read_data(test_input_file)
assert is_safe_report(test_data[0])
assert not is_safe_report(test_data[1])
assert not is_safe_report(test_data[2])
assert is_safe_report(test_data[3])
assert is_safe_report(test_data[4])
assert is_safe_report(test_data[5])


d = safe_reports(read_data(input_file))
print(d)