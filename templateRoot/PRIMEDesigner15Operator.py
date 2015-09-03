class Operator:
  
	def __init__(self, name, precond, state_transf):
		self.name = name
		self.precond = precond
		self.state_transf = state_transf

	def is_applicable(self, state):
		return self.precond(state)

	def apply(self, state):
		return self.state_transf(state)
		
class AsyncOperator(Operator):
	pass