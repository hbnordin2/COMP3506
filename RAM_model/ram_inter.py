import ram

class Interpreter:
	def __init__(self, file_name):
		self.file = open(file_name, 'r')
		self.statements = []
		self.__add_statements__()
		self.program_counter = 0
		self.ram = ram.Ram()
		self.__interprete__()
		self.run_time = 0

	def get_statements(self):
		return self.statements

	def get_ram(self):
		return self.ram

	def __remove_comments__(self, line):
		line_content = line.split('//')
		statement = line_content[0]
		return statement

	def __add_statements__(self):
		for i in self.file:
			statement = self.__remove_comments__(i)
			self.statements.append(statement)

	def __read_statement__(self, statement):
		if('<-' in statement):
			self.run_time += 1;
			self.__initialize_op__(statement)

	def __initialize_op__(self, statement):
		statement_content = statement.split('<-')
		register_index = self.__parse_register__(statement_content[0])
		self.ram.initialize_register(register_index, statement_content[1])

	def __parse_register__(self, register_name):
		register_val = register_name[1:]
		return int(register_val)

	def __interprete__(self):
		for i in self.statements:
			self.__read_statement__(i)

class Subroutine:
	def __init__(self, subroutine):
		self.__get_label__(subroutine[0])
		self.statements = self.__parse_statements__(subroutine[1:])

	def __get_label__(self, label_statement):
		length = len(label_statement)
		self.label = label_statement[:length-1]

	def __parse_statements__(self, statements):
		statements = []
		for i in statements:
			statement = i.strip()
			statements.append(statement)
		return statements



inter = Interpreter('example.ram')
print(inter.get_statements())
print(inter.get_ram().get_register(0,10))