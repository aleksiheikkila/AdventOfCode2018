"""
Advent of code, 2018
Day 16: Chronal Classification
"""

# Four registers: 0-3
# Every instruction consists of four values: an opcode, two inputs (named A and B), and an output (named C)
# So format like "OPCODE A B C"

# Unfortunately, while the manual gives the name of each opcode, it doesn't seem to indicate the number

from typing import NamedTuple, List

Registers = List[int]

OPERATIONS = ["addr", "addi", "mulr", "muli", "banr", "bani", "borr", "bori",
              "setr", "seti", "gtir", "gtri", "gtrr", "eqir", "eqri", "eqrr"]

# Immutable, NamedTuple should be fine
class Instruction(NamedTuple):
    op: str  # the name of the operation (not the numeric code)
    a: int
    b: int
    c: int

    def process(self, registers: Registers) -> Registers:
        out = registers.copy()  # the register state after the instruction has been processed. To be returned

        # addr (add register) stores into register C the result of adding register A and register B.
        if self.op == "addr":
            out[self.c] = out[self.a] + out[self.b]
        # addi (add immediate) stores into register C the result of adding register A and value B.
        elif self.op == "addi":
            out[self.c] = out[self.a] + self.b

        # mulr (multiply register) stores into register C the result of multiplying register A and register B.
        elif self.op == "mulr":
            out[self.c] = out[self.a] * out[self.b]
        # muli (multiply immediate) stores into register C the result of multiplying register A and value B.
        elif self.op == "muli":
            out[self.c] = out[self.a] * self.b

        # bitwise AND
        #banr (bitwise AND register) stores into register C the result of the bitwise AND of register A and register B.
        elif self.op == "banr":
            out[self.c] = out[self.a] & out[self.b]

        #bani (bitwise AND immediate) stores into register C the result of the bitwise AND of register A and value B.
        elif self.op == "bani":
            out[self.c] = out[self.a] & self.b

        # bitwise OR
        #borr (bitwise OR register) stores into register C the result of the bitwise OR of register A and register B.
        elif self.op == "borr":
            out[self.c] = out[self.a] | out[self.b]
        #bori (bitwise OR immediate) stores into register C the result of the bitwise OR of register A and value B.
        elif self.op == "bori":
            out[self.c] = out[self.a] | self.b

        #Assignment:
        #setr (set register) copies the contents of register A into register C. (Input B is ignored.)
        elif self.op == "setr":
            out[self.c] = out[self.a]

        #seti (set immediate) stores value A into register C. (Input B is ignored.)
        elif self.op == "seti":
            out[self.c] = self.a
        
        #Greater-than testing:
        #gtir (greater-than immediate/register) sets register C to 1 if value A is greater than register B. 
        # Otherwise, register C is set to 0.
        elif self.op == "gtir":
            out[self.c] = 1 if self.a > out[self.b] else 0
        
        #gtri (greater-than register/immediate) sets register C to 1 if register A is greater than value B. 
        # Otherwise, register C is set to 0.
        elif self.op == "gtri":
            out[self.c] = 1 if out[self.a] > self.b else 0
        
        #gtrr (greater-than register/register) sets register C to 1 if register A is greater than register B. 
        # Otherwise, register C is set to 0.
        elif self.op == "gtrr":
            out[self.c] = 1 if out[self.a] > out[self.b] else 0

        #Equality testing:
        #eqir (equal immediate/register) sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0.
        elif self.op == "eqir":
            out[self.c] = 1 if self.a == out[self.b] else 0
        
        #eqri (equal register/immediate) sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0.
        elif self.op == "eqri":
            out[self.c] = 1 if out[self.a] == self.b else 0
        
        #eqrr (equal register/register) sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0.
        elif self.op == "eqrr":
            out[self.c] = 1 if out[self.a] == out[self.b] else 0

        else:  # no idea what op is being requested
            raise ValueError("The operator code string not identified!")

        return out   # this is the register state after the instruction is applied on the previous register state


# PART A:
# Ignoring the opcode numbers, how many samples in your puzzle input behave like three or more opcodes?
# Go thru all of them, apply all operations to them, check how many gives the correct output


# Test case:
reg_before = [3, 2, 1, 1]
valid_ops = []
reg_expected = [3, 2, 2, 1]

for op in OPERATIONS:
    instr = Instruction(op, 2, 1, 2)
    registers_after = instr.process(reg_before)
    if registers_after == reg_expected:
        valid_ops.append(op)

# Unit tests for the test case
assert len(valid_ops) == 3
assert set(valid_ops) == set(["mulr", "addi", "seti"])


# READ IN THE INSTRUCTION DATA:
with open("data/day16_ops.txt") as f:
    lines = f.readlines()

def parse_input(lines: str):
    """
    given lines of input (as list), returns examples
    Examples is a list, with sublist for each complete example
    The sublist contains three sublists, register state before, actual instruction, register state after
    """
    inputs = []
    for line in lines:
        if "Before: " in line:
            reg_before = [int(elem) for elem in eval(line.split(": ")[1].strip())]   # as list
        elif line[0].isdigit():
            instr_input = [int(elem) for elem in line.strip().split()]
        elif "After: " in line:
            reg_expected = [int(elem) for elem in eval(line.split(": ")[1].strip())]  # as list
        elif line == "\n":  # empty.
            inputs.append([reg_before[:], instr_input[:], reg_expected[:]])
            del reg_before, instr_input, reg_expected

    # add the last example (there is not newline for that to trigger addition)
    inputs.append([reg_before[:], instr_input[:], reg_expected[:]])

    return inputs

examples = parse_input(lines)

# Go thru all inputdata elements.
num_samples_with_min_3_opcodes = 0   # we need to solve this

for example in examples:
    reg_before, instr_inputs, reg_expected = example
    valid_ops = []
    # apply every operation
    for op in OPERATIONS:
        instr = Instruction(op, *instr_inputs[1:])
        registers_after = instr.process(reg_before)
        if registers_after == reg_expected:
            valid_ops.append(op)
    
    if len(valid_ops) >= 3:
        num_samples_with_min_3_opcodes += 1

print("PART 1: ", num_samples_with_min_3_opcodes, " samples behaved like three or more opcodes\n")
# 596 --> the right answer!


#########
# PART 2:
# Using the samples you collected, work out the number of each opcode and execute the test program (the second section of your puzzle input).
print("PART 2:")
# for every opcode (int), set of possible ops (strings) that it could match to.
possible_ops = {i: set(OPERATIONS) for i in range(len(OPERATIONS))}

# Possible mappings after examples
for example in examples:
    reg_before, instr_inputs, reg_expected = example
    valid_ops = set()
    # apply every operation
    for op in OPERATIONS:
        instr = Instruction(op, *instr_inputs[1:])
        registers_after = instr.process(reg_before)
        if registers_after == reg_expected:
            valid_ops.add(op)
    
    # set intersection (remove those that are not common between...)
    possible_ops[instr_inputs[0]] = possible_ops[instr_inputs[0]] & valid_ops

# Then iteratively find the matches. Find such possible_ops that have only one possibility. Found!
# Freeze that, remove the just found op from the rest of the possible_ops. Repeat the process

op_to_opcode_map = dict()

while True:
    maxlen = max(len(possible) for possible in possible_ops.values())
    if maxlen < 1:  # all found
        break

    for opcode, pops in possible_ops.items():
        if len(pops) == 1:
            resolved_op = pops.pop()
            op_to_opcode_map[opcode] = resolved_op
            break
    # remove resolved_op from all sets in possible_ops
    for opcode, pops in possible_ops.items():
        pops.discard(resolved_op)

print(op_to_opcode_map)

# What value is contained in register 0 after executing the test program?
# Load the test prog:
with open("data/day16_test_prog.txt") as f:
    test_prog_instructions = [[int(elem) for elem in line.strip().split()]
                                for line in f.readlines()]

registers = [0, 0, 0, 0]
for instr_params in test_prog_instructions:
    registers = Instruction(op_to_opcode_map[instr_params[0]], *instr_params[1:]).process(registers)

print("Register state after processing: ", registers)
# 554 - correct answer