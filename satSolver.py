import random

class Solver:
	
	def __init__(self):
		var1 = 1
		self.f = Formula(litNum)
		self.decisions = []
	
	def randomDecision(self, unassigned):
		var = random.choice(unassigned)
		val = random.choice([0,1])
		return var, val
	
	def removeLastLevel(self):
		temp = self.decisions.pop()
	
	def propagationStep(self, lit, val):
		for c in self.f.get_clausses(): 
			if lit in c:				#checks if the literal is in each class 
				if val == 1:
					c.add_ones()
					
				else:
					c.add_zeros()
					
	
	
	#this is the actual solver, the algorithm will be here
	def solver(self):
		
		while True:
			unassigned = self.f.get_unassignedList()
			if len(unassigned) == 0:
				break
			
			lit, val = self.randomDecision(unassigned)
			self.f.removeFromUnassigned(lit)
			
			self.propagationStep(lit)
			
		
class Formula:

	def __init__(self, litNum):
		self.num_of_literals = litNum # do I get the
		self.unassigned = []
		self.clauses = []
	
	def get_clausses(self):
		return self.clauses
	
	def get_unassignedList(self):
		return self.unassigned
	
	def addToUnassigned(self, x):
		if x not in self.unassigned:
			self.unassigned.append(x)
			
	def removeFromUnassigned(self, x):
		if x in self.unassigned:
			self.unassigned.remove(x)
	
	def addClause(self, lits):
		c = Clause(lits)
		self.clauses.append(c) #do I need to order in some way?
	
	def removeClause(self, c):
		if c in self.clauses:
			self.clauses.remove(x)
	
	def simplifyFormula(self):
		for c in self.clauses:
			if c.isSatisfied():
				self.removeClause(c)
						
	def createClauses(self):
		#TODO: parse the benchmark
	
		
class Clause:
	
	def __init__(self, lits):
		self.literalList = lits
		self.num_of_literals = len(lits)
		self.num_of_zeros = 0
		self.num_of_ones = 0
	
	def get_num_of_zeros(self):
		return self.num_of_zeros
	
	def get_num_of_ones(self):
		return self.num_of_ones
	
	def get_literalList(self):
		return self.literalList
		
	def add_zeros(self):
		self.num_of_zeros += 1
	
	def add_ones(self):
		self.num_of_ones += 1
	
	def isConflict(self):
		if self.num_of_zeros == self.num_of_literals
			return True
		else:
			return False
	
	def isSatisfied(self):
		if self.num_of_ones + self.num_of_zeros == self.num_of_literals:
			if not self.isConflict():
				return True
		return False
	
	def isUnitClause(self):
		if (self.num_of_zeros == self.num_of_literals - 1) and not self.isSatisfied():
			return True
		return False
	
	
			