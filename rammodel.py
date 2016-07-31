# Defined rules so far:
# 1. Register Value Set
#     R1 <- 2
#     R31 <- 2132

import sys


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def is_register(s):
    if s.startswith("R"):
        reg_number = s.split("R")[1]
    elif s.startswith("r"):
        reg_number = s.split("r")[1]
    else:
        return False
    return is_int(reg_number)


with open(sys.argv[1]) as f:
    # read file to string array called lines
    lines = [l.split("//")[0] for l in f.read().splitlines()]

# get the initial memory from the first line
memory = [int(x) & 0xffffffff for x in lines[0].strip().split()]
# remove the first line which is no longer needed
code = lines[1:]

# this will store any branches to return to
branches = {}

for line_num in range(len(code)):
    c = code[line_num]
    # if it ends in a colon, then it is a branch point
    if c.endswith(":"):
        branches[c.split(":")[0].strip()] = line_num

program_counter = 0
registers = [0] * 32
running_time = 0

while program_counter < len(code):
    line = code[program_counter]
    arrow_split = line.split("<-")
    if len(arrow_split) == 2:
        lhs = arrow_split[0].strip()
        rhs = arrow_split[1].strip()
        # if the left hand side starts is a register, and the right hand side 
        # is a number, then this is an instruction for rule one.
        if is_register(lhs) and is_int(rhs):
            if lhs.startswith("R"):
                register_number = int(lhs.split("R")[1])
            elif lhs.startswith("r"):
                register_number = int(lhs.split("r")[1])
            value = int(rhs)
            # double check that the register is in the valid range
            if 0 < register_number < 32:
                registers[register_number] = value
                running_time += 1
    program_counter += 1

print("Register Values: " + ' '.join(str(n) for n in registers))
print("Memory Values: " + ' '.join(str(n) for n in memory))
print("Running Time: " + str(running_time))
