
import os

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_files = [os.path.join(script_dir, f'test.input{i}') for i in range(1)]


def read_data(file_name: str) -> tuple[list[int], list[int]]:
    registers = []
    program = []
    with open(file_name, 'r') as f:
        for line in f:
            if line.startswith('Register'):
                registers.append(int(line.strip().split()[-1]))
            if not line.strip():
                continue
            if line.startswith('Program'):
                program = list(map(int, line.strip().split()[-1].split(',')))
    return registers, program


def run(R: list[int], program: list[int]) -> str:
    IP = 0  # Instruction Pointer
    output = []
    while IP < len(program) - 1:
        opcode = program[IP]
        operand = program[IP + 1]
        combo = None
        if opcode in (0, 2, 5, 6, 7):
            combo = operand if operand < 4 else R[operand - 4]

        match opcode:
            case 0:  # adv
                R[0] >>= combo
            case 1:  # bxl
                R[1] ^= operand
            case 2:  # bst
                R[1] = combo & 0b111
            case 3:  # jnz
                if R[0]:
                    IP = operand
                    continue
            case 4:  # bxc
                R[1] = R[1] ^ R[2]
            case 5:  # out
                output.append(combo & 0b111)
            case 6:  # bdv
                R[1] = R[0] >> combo
            case 7:  # cdv
                R[2] = R[0] >> combo
            case _:
                raise NotImplementedError(f'Opcode {opcode} not implemented')
        IP += 2

    return output, R


_, r1 = run([0, 0, 9], [2, 6])
assert r1[1] == 1

o2, _ = run([10, 0, 0], [5, 0, 5, 1, 5, 4])
assert o2 == [0, 1, 2]


o3, r3 = run([2024, 0, 0], [0, 1, 5, 4, 3, 0])
assert o3 == [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0]
assert r3[0] == 0

_, r4 = run([0, 29, 0], [1, 7])
r4[1] = 26

_, r5 = run([0, 2024, 43690], [4, 0])
assert r5[1] == 44354


o6, _ = run(*read_data(test_input_files[0]))
assert o6 == [4, 6, 3, 5, 6, 3, 5, 2, 1, 0]

o, _ = run(*read_data(input_file))
print(','.join(map(str, o)))
