"""
Advent of code, 2018
Day 19: Go With The Flow
Part Two was... different.
"""

from day16_chronal_classification import Instruction
from typing import List

Registers = List[int]


RAW = """#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5"""


def parse_input(input_str: str):
    lines = input_str.splitlines()

    instructs = []

    for line in lines:
        if line.startswith("#ip"):
            ip = int(line.split()[1])
        else:
            op, a, b, c = line.strip().split()
            instructs.append(Instruction(str(op), int(a), int(b), int(c)))

    return ip, instructs


def run_prog_until_halt(registers: Registers, instructions: List[Instruction], ip: int, verbose=False) -> Registers:
    while True:
        instruction_idx = registers[ip]

        if verbose: print(instruction_idx, registers)

        # stop criterion
        if instruction_idx >= len(instructions) or instruction_idx < 0:  # outside the program
            break

        instruction = instructions[instruction_idx]
        registers = instruction.process(registers)
        registers[ip] += 1

    return registers


def run_prog_one_step(registers: Registers, instructions: List[Instruction], ip: int, verbose=False) -> Registers:
    instruction_idx = registers[ip]

    if verbose: print("Before:\t", instruction_idx, registers)

    # stop criterion
    if instruction_idx >= len(instructions) or instruction_idx < 0:  # outside the program
        return "Finished!"

    instruction = instructions[instruction_idx]
    registers = instruction.process(registers)
    registers[ip] += 1

    if verbose: print("After:\t", instruction_idx, registers)

    return registers


# With test input
ip, instrs = parse_input(RAW)
registers = [0, 0, 0, 0, 0, 0]

registers = run_prog_until_halt(registers, instrs, ip)
assert registers[0] == 7


# Then with actual input
# PART ONE:
# What value is left in register 0 when the background process halts?

with open("data/day19.txt") as f:
    inp = f.read()

ip, instrs = parse_input(inp)
registers = [0, 0, 0, 0, 0, 0]

registers = run_prog_until_halt(registers, instrs, ip)
print("Part One: value left in register 0 when the background process halts: ", registers[0])
# 960 is the right answer


################
# Part Two
#A new background process immediately spins up in its place. 
#It appears identical, but on closer inspection, you notice that this time, register 0 started with the value 1.

# What value is left in register 0 when this new background process halts?
registers = [1, 0, 0, 0, 0, 0]


#registers = run_prog_until_halt(registers, instrs, ip, verbose=True)
#print("Part Two: value left in register 0 when the background process halts: ", registers[0])

# Takes ages... need to reason the solution
# Figure out what the "assembly code" does and how the program will run

"""
# instruction pointer is bound to the last register (id 5)

start register values before starts looping: 

At the beginning we do:
0 [1, 0, 0, 0, 0, 0]
17 [1, 0, 0, 0, 0, 17]
18 [1, 0, 0, 0, 2, 18]
19 [1, 0, 0, 0, 4, 19]
20 [1, 0, 0, 0, 76, 20]
21 [1, 0, 0, 0, 836, 21]
22 [1, 0, 0, 2, 836, 22]
23 [1, 0, 0, 44, 836, 23]
24 [1, 0, 0, 57, 836, 24]
25 [1, 0, 0, 57, 893, 25]
27 [1, 0, 0, 57, 893, 27]
28 [1, 0, 0, 27, 893, 28]
29 [1, 0, 0, 756, 893, 29]
30 [1, 0, 0, 785, 893, 30]
31 [1, 0, 0, 23550, 893, 31]
32 [1, 0, 0, 329700, 893, 32]
33 [1, 0, 0, 10550400, 893, 33]
34 [1, 0, 0, 10550400, 10551293, 34]
35 [0, 0, 0, 10550400, 10551293, 35]
1 [0, 0, 0, 10550400, 10551293, 1]
2 [0, 0, 1, 10550400, 10551293, 2]
3 [0, 1, 1, 10550400, 10551293, 3]
4 [0, 1, 1, 1, 10551293, 4]
5 [0, 1, 1, 0, 10551293, 5]
6 [0, 1, 1, 0, 10551293, 6]
8 [0, 1, 1, 0, 10551293, 8]
9 [0, 2, 1, 0, 10551293, 9]
10 [0, 2, 1, 0, 10551293, 10]
11 [0, 2, 1, 0, 10551293, 11]
"""

# This setups the thing. Then we start the following loop
"""
3 [0, 2, 1, 0, 10551293, 3]
4 [0, 2, 1, 2, 10551293, 4]
5 [0, 2, 1, 0, 10551293, 5]
6 [0, 2, 1, 0, 10551293, 6]
8 [0, 2, 1, 0, 10551293, 8]
9 [0, 3, 1, 0, 10551293, 9]
10 [0, 3, 1, 0, 10551293, 10]
11 [0, 3, 1, 0, 10551293, 11]
3 [0, 3, 1, 0, 10551293, 3]
4 [0, 3, 1, 3, 10551293, 4]
5 [0, 3, 1, 0, 10551293, 5]
6 [0, 3, 1, 0, 10551293, 6]
8 [0, 3, 1, 0, 10551293, 8]
9 [0, 4, 1, 0, 10551293, 9]
10 [0, 4, 1, 0, 10551293, 10]
11 [0, 4, 1, 0, 10551293, 11]
3 [0, 4, 1, 0, 10551293, 3]


# Hence loop op ids 3,4,5,6,8,9,10,11 (ids start from zero)

3   mulr 2 1 3      r[3] = r[2] * [r1]
4   eqrr 3 4 3      r[3] = 1 if r[3] == r[4] else r[3] = 0
5   addr 3 5 5      r[5] += r[3]
6   addi 5 1 5      r[5] += 1
8   addi 1 1 1      r[1] += 1
9   gtrr 1 4 3      r[3] = 1 if r[1] > r[4] else r[3] = 0
10  addr 5 3 5      r[5] += r[3]
11  seti 2 6 5      r[5] = 2                    # keeps cycling
...
3   mulr 2 1 3


These remain unchanged over these cycles (are not touched at all):
r[0] = 0
r[2] = 1
r[4] = 10551293

What changes between cycles?
r[1] += 1
When will this lead to breaking out of the cycle?

# Reduced:
3   mulr 2 1 3      r[3] = r[2]*r[1] 
4   eqrr 3 4 3      r[3] = 1 if r[3] == 10551293 else r[3] = 0

    
5   addr 3 5 5      r[5] += r[3]
6   addi 5 1 5      r[5] += 1
8   addi 1 1 1      r[1] += 1
9   gtrr 1 4 3      r[3] = 1 if r[1] > 10551293 else r[3] = 0
10  addr 5 3 5      r[5] += r[3]
11  seti 2 6 5      r[5] = 2

--> Something else happens when r[1] gets to 10551293. What is it?

1st iter:
            [0, 2, 1, 0, 10551293, 3]

2nd iter
Before:  3  [1, 1, 2, 0, 10551293, 3]

3rd iter
Before:  3  [1, 2, 3, 0, 10551293, 3]

4th iter
Before:  3 [1, 1, 4, 0, 10551293, 3]

We increment the r[2] by one


What happens when r[1] get to 10551293?

4 [1, 10551293, 3, 31653879, 10551293, 4]
5 [1, 10551293, 3, 0, 10551293, 5]
6 [1, 10551293, 3, 0, 10551293, 6]
8 [1, 10551293, 3, 0, 10551293, 8]
9 [1, 10551294, 3, 0, 10551293, 9]
10 [1, 10551294, 3, 1, 10551293, 10]
12 [1, 10551294, 3, 1, 10551293, 12]
13 [1, 10551294, 4, 1, 10551293, 13]
14 [1, 10551294, 4, 0, 10551293, 14]
15 [1, 10551294, 4, 0, 10551293, 15]
2 [1, 10551294, 4, 0, 10551293, 2]
3 [1, 1, 4, 0, 10551293, 3]

4   eqrr 3 4 3      r[3] = 1 if r[3] == r[4] else r[3] = 0          out:    [1, 10551293, 3, 0, 10551293, 5]
5   addr 3 5 5      r[5] += r[3]                                            [1, 10551293, 3, 0, 10551293, 6]
6   addi 5 1 5      r[5] += 1                                               [1, 10551293, 3, 0, 10551293, 8]
8   addi 1 1 1      r[1] += 1                                               [1, 10551294, 3, 0, 10551293, 9]
9   gtrr 1 4 3      r[3] = 1 if r[1] > r[4] else r[3] = 0                   [1, 10551294, 3, 1, 10551293, 10]
10  addr 5 3 5      r[5] += r[3]                                            [1, 10551294, 3, 1, 10551293, 12]
12  addi 2 1 2      r[2] += 1                                               [1, 10551294, 4, 1, 10551293, 13]
13  gtrr 2 4 3      r[3] = 1 if r[2] > r[4] else 0                          [1, 10551294, 4, 0, 10551293, 14]
    ## Things change when r[2] is greater that 10551293
14  addr 3 5 5      r[5] += r[3]                                            [1, 10551294, 4, 0, 10551293, 15]
15  seti 1 2 5      r[5] = 1                                                [1, 10551294, 4, 0, 10551293, 2]
2   seti 1 8 1      r[1] = 1                                                [1, 1, 4, 0, 10551293, 3]

Iterations increase the r[2] by one (instr 12)

When will this stop?

On the round when r[1] == 10551293 we go after instr 10 to 12
12  addi 2 1 2      r[2] += 1
13  gtrr 2 4 3      r[3] = 1 if r[2] > r[4] else 0
    ## Things change when r[2] is greater that 10551293
14  addr 3 5 5      r[5] += r[3]
15  seti 1 2 5      r[5] = 1
2   seti 1 8 1      r[1] = 1
(then continue the first loop)


Then it is important to note that the operation 3,4,5 will go to operation 7 whenever
r[2]*r[1] == 10551293. Then we increment r[0] by r[2].

3   mulr 2 1 3      r[3] = r[2]*r[1]    ( r[1] loops over the range of the number, r[2] get just incremented by one)
4   eqrr 3 4 3      r[3] = 1 if r[3] == 10551293 else r[3] = 0
    ## check this case when r[2] is increased...
    ## when r[2] and r[1] are factors of 10551293
        r[3] = 1 --> 
        --> next op 5: addr 3 5 5      r[5] += r[3]--> r[5] = 7
        --> op 7: addr 2 0 0    r[0] += r[2]


=> OKAY, THE ANSWER IS THE SUM OF ALL FACTORS OF r[4] = 10551293
After these the program will hit operation r[5] = r[5]*r[5] which will throw op pointer out of bounds and terminate the prog
"""


def get_factors(n:int) -> List[int]:
    factors = []
    for i in range(1, n+1):
        if n % i == 0: factors.append(i)

    return factors

print("Part Two")
print("The answer should be:", sum(get_factors(10551293)))
# Correct answer: 10750428