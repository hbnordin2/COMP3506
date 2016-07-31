import sys, re

# Define all the regular expressions
LABEL = r"([a-zA-Z0-9]*)"
REGISTER = r"[Rr]([0-9]{1,2})"
ARROW = r"\s*<-\s*"
MEMORY = r"mem\[" + REGISTER + r"\]"
LABEL_PATTERN = re.compile(LABEL + r":$")
REGISTER_SET_PATTERN = re.compile(REGISTER + ARROW +  r"([0-9]*)$")
ARITHMETIC_PATTERN = re.compile(REGISTER + ARROW + REGISTER + r"\s*([\/\+\-\*])\s*" + REGISTER + r"$")
CONDITIONAL_PATTERN = re.compile(REGISTER + r"\s*([<=>])\s*" + REGISTER + r"\s*\?\s*" + LABEL + r"$")
MEMORY_SET_PATTERN = re.compile(MEMORY + ARROW + REGISTER + r"$")
MEMORY_GET_PATTERN = re.compile(REGISTER + ARROW + MEMORY + r"$")

class RAMModel:
    def __init__(self, filename):
        with open(filename) as f:
            # read file to string array called lines and remove leading/trailing whitespace
            lines = [l.split("//")[0].strip() for l in f.read().splitlines()]
        # get the initial memory from the first line
        self._memory = [int(x) & 0xffffffff for x in lines[0].split()]
        # remove the first line which is no longer needed
        self._code = lines[1:]

        # this will store any branches to return to
        self._branches = {}
        for line_num in range(len(self._code)):
            c = self._code[line_num]
            match = LABEL_PATTERN.match(c)
            if match:
                self._branches[match.group(1)] = line_num

        self._program_counter = 0
        self._registers = [0] * 32
        self._running_time = 0

    def display_vals(self):
        print("Register Values: " + ' '.join(str(n) for n in self._registers))
        print("Memory Values: " + ' '.join(str(n) for n in self._memory))
        print("Running Time: " + str(self._running_time))

    def interpret_instruction(self):
        line = self._code[self._program_counter]
        register_set_match = REGISTER_SET_PATTERN.match(line)
        arithmetic_match = ARITHMETIC_PATTERN.match(line)
        conditional_match = CONDITIONAL_PATTERN.match(line)
        memory_set_match = MEMORY_SET_PATTERN.match(line)
        memory_get_match = MEMORY_GET_PATTERN.match(line)
        if register_set_match:
            self.set_register(register_set_match.group(1), register_set_match.group(2))
        elif arithmetic_match:
            self.arithmetic(arithmetic_match.group(1), arithmetic_match.group(2), arithmetic_match.group(3), arithmetic_match.group(4))
        elif conditional_match:
            self.conditional(conditional_match.group(1), conditional_match.group(2), conditional_match.group(3), conditional_match.group(4))
        elif memory_set_match:
            self.mem_set(memory_set_match.group(1), memory_set_match.group(2))
        elif memory_get_match:
            self.mem_get(memory_get_match.group(2), memory_get_match.group(1))
        else:
            self._program_counter += 1


    def set_register(self, reg_num, value):
        reg_num = int(reg_num)
        value = int(value) & 0xffffffff
        if 0 <= reg_num < 32:
            self._registers[reg_num] = value
        self._program_counter += 1
        self._running_time += 1

    def arithmetic(self, reg_store, reg_lhs, operation, reg_rhs):
        reg_store = int(reg_store)
        reg_lhs = int(reg_lhs)
        reg_rhs = int(reg_rhs)
        if 0 <= reg_store < 32 and 0 <= reg_lhs < 32 and 0 <= reg_rhs < 32:
            lhs = self._registers[reg_lhs]
            rhs = self._registers[reg_rhs]
            if operation == '/' and rhs == 0:
                print("Division by zero on line " + self._program_counter + ": " + self._code[self._program_counter])
            else:
                # evaluate result of expression
                self._registers[reg_store] = int(eval(str(lhs) + operation + str(rhs))) & 0xffffffff
        self._program_counter += 1
        self._running_time += 1
    
    def conditional(self, reg_lhs, comparison, reg_rhs, label):
        reg_lhs = int(reg_lhs)
        reg_rhs = int(reg_rhs)
        if (0 <= reg_lhs < 32) and (0 <= reg_rhs < 32) and (label in self._branches):
            if comparison == "=":
                comparison = "=="
            lhs = self._registers[reg_lhs]
            rhs = self._registers[reg_rhs]
            result = eval(str(lhs) + comparison + str(rhs))
            if result:
                self._program_counter = self._branches[label]
            else:
                self._program_counter += 1
        self._running_time += 1

    def mem_set(self, reg_address, reg_value):
        reg_address = int(reg_address)
        reg_value = int(reg_value)
        if 0 <= reg_address < 32 and 0 <= reg_value < 32:
            address = self._registers[reg_address]
            value = self._registers[reg_value]
            if (address >= len(self._memory)):
                difference = address - (len(self._memory) - 1)
                self._memory += [0] * difference
            self._memory[address] = value
        self._program_counter += 1
        self._running_time += 1

    def mem_get(self, reg_address, reg_store):
        reg_address = int(reg_address)
        reg_store = int(reg_store)
        if 0 <= reg_address < 32 and 0 <= reg_store < 32:
            address = self._registers[reg_address]
            if (address >= len(self._memory)):
                difference = address - (len(self._memory) - 1)
                self._memory += [0] * difference
            self._registers[reg_store] = self._memory[address]
        self._program_counter += 1
        self._running_time += 1

    def run(self):
        while self._program_counter < len(self._code):
            self.interpret_instruction()
        self.display_vals()

model = RAMModel(sys.argv[1])
model.run()