class rpnCalculator:
	'rpnCalculator'

	def __init__(self):
		self.stack = []
	
	def push(self, v):
		self.stack.append(v)
	
	def pop(self):
		try:
			v = self.stack.pop();
		except:
			v = None
		else:
			return v

	def add(self):
		if len(self.stack) >= 2:
			self.stack.append(self.stack.pop()+self.stack.pop())
	
	def sub(self):
		if len(self.stack) >= 2:
			self.stack.append(self.stack.pop()-self.stack.pop())

	def print(self):
		print(self.stack)
