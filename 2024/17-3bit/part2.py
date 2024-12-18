
import itertools
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


# Program is equivalent to the following:
# # while A > 0:
# #     if A % 2 == 0:
# #         print(((A >> 1 >> A % 8) ^ A ^ 4) % 8)
# #     else:
# #         print(((A << 1 >> A % 8) ^ A ^ 4) % 8)
# #     A >>= 3
#
# Main observations:
# - A is shifted right by 3 bits in each iteration of the loop.
# - The output is calculated based on the parity of A.
# - program output only depends on register A.
#
# Find outputs from the program by working backwards to find the initial value of A
# by trying all possible values of A and checking if the outputs match. Once a match
# is found, A is shifted right by 3 bits to mimic the next iteration of the program loop.


def initial_A(program: list[int]) -> int:
    A = 0
    i_out = 1
    while i_out <= len(program):
        A <<= 3
        for i in itertools.count():
            out, _ = run([A + i, 0, 0], program)
            if program[-i_out:] == out:
                i_out += 1
                A += i
                break
    return A


_, program = read_data(input_file)
A = initial_A(program)
print(A)
