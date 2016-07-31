"""
A class representing the RAM model
"""
class Ram:
    def __init__(self):
        self.register = [None] * 32
        self.memory = [None] * 100

    """
    Adds the value in register x and y and stores the result in register dest
    """
    def add_register(self, x, y, dest):
        self.register[dest] = self.register[x] + self.register[y]

    """
    Multiplies the values in register x and y and stores the result in register dest
    """
    def multiply_register(self, x, y, dest):
        self.register[dest] = self.register[x] * self.register[y]

    """
    Subtracts the values in register x and y and stores the result in register dest
    """
    def subtract_register(self, x, y, dest):
        self.register[dest] = self.register[x] - self.register[y]

    """
    Divides the values in register x and y and stores the result in register dest
    """
    def divide_register(self, x, y, dest):
        self.register[dest] = self.register[x]//self.register[y]

    """
    Initializes a register x to value
    """
    def initialize_register(self, x, value):
        self.register[x] = value

    """
    Stores 1 into register dest if register x > register y and 0 otherwise
    """
    def register_greater(self, x, y, dest):
        if(self.register[x]>self.register[y]):
            self.register[dest] = 1
        else:
            self.register[dest] = 0

    """
    Stores 1 into register dest if register x < register y and 0 otherwise
    """
    def register_lesser(self, x, y, dest):
        if(self.register[x]<self.register[y]):
            self.register[dest] = 1
        else:
            self.register[dest] = 0

    """
    Stores 1 into register dest if register x == register y and 0 otherwise
    """
    def register_comp(self, x, y, dest):
        if(self.register[x]==self.register[y]):
            self.register[dest] = 1
        else:
            self.register[dest] = 0

    """
    Copies value from register address to memory address
    """
    def write_to_mem(self, register_address, memory_address):
        self.memory[memory_address] = self.register[register_address]

    """
    Copies value from memory address to register address
    """
    def read_from_mem(self, register_address, memory_address):
        self.regiser[register_address] = self.memory[memory_address]
