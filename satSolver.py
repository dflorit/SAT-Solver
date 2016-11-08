import random
from nltk.tokenize import word_tokenize
class Solver:
	
	def __init__(self):
		p = Parser()
		self.f = p.parseText() #this is my formula object
		self.decisions = []
		self.solver()
		#self.f.print_clauses()
	
	def randomDecision(self, unassigned):
		lit = random.choice(unassigned)
		val = random.choice([True, False])
		print "random decision: lit, val: ", lit, val
		return lit, val
	
	def removeLastLevel(self):
		temp = self.decisions.pop()
	
	#modified propagationStep
	def propagationStep(self, lit, val):
		print "propagation step"
		print lit
		clauseMembership = self.f.getLiteralMembership(lit)
		print "clauseMembership: ", clauseMembership
		if clauseMembership != None: #need to double check why this is needed
			for c in clauseMembership:
				if val == True:
					c.add_ones()
				else:
					c.add_zeros()
			
				if c.isConflict():
					print "Need to backtrack"
				elif c.isSatisfied():
					self.f.removeClause(c)
				elif c.isUnitClause():
					lits = c.get_literalList()
					
					for l in lits:
						if self.f.getLiteralValue(l) == None:
							unassigned = l
					"I'm the one sending it"
					self.propagationStep(unassigned, True)
					self.propagationStep(-1*unassigned, False)
				
		
		''' old version:
		
		for c in self.f.getClauses(): 
			if lit in c:				#checks if the literal is in each class 
				if val == 1:
					c.add_ones()
				else:
					c.add_zeros()
		'''
					
	#this is the actual solver, the algorithm will be here
	def solver(self):
		
		while True:
			unassigned = self.f.get_unassignedList()
			if len(unassigned) == 0:
				break
			
			lit, val = self.randomDecision(unassigned)
			self.f.removeFromUnassigned(lit)
			
			self.f.setLiteralValue(lit, val)
			self.f.setLiteralValue(-1*lit, val)
			
			self.propagationStep(lit, val)
			self.propagationStep(lit*-1, 0)
			
class Parser:

	def __init__(self):
			input = "sampleInput.cnf"
			self.f = Formula() #creating a formula
			self.text = open(input) # creating file object
			self.n_clauses = 0
			self.max_variables = 0
	
	def parseText(self):
		line = self.text.readline() #first line of the text
		
		#eliminating comments. Waiting for the line that starts with 'p'
		while line[0] != 'p':
			line = self.text.readline()
		
		data = word_tokenize(line) #this line starts with p, then it contains nbvar(max_variables) and nbclauses(n_clauses)
		self.n_clauses = data[3] #exact number of clauses
		self.max_variables = data[2] # largest index of a variable appearing in the file
		
		i = 0 #clause index
		for newLine in self.text:
			newClause = [int(x) for x in word_tokenize(newLine) if x != '0']
			self.f.addClause(newClause)
			c = self.f.getClauseAtIndex(i)
			
			for lit in newClause:
				print "HI ", lit
				self.f.addToUnassigned(abs(lit)) #adding to set of unassigned variables
				self.f.setLiteralMembership(lit, c)
				
			
			i += 1 # increment clause index
		return self.f

class Formula:

	def __init__(self):
		#self.num_of_literals = 0 # do I get the
		self.unassigned = []
		self.clauses = []
		self.literalMembership = {}
	
	def getClauses(self):
		return self.clauses
	
	def getClauseAtIndex(self, i):
		return self.clauses[i]	
			
	def get_unassignedList(self):
		return self.unassigned
	
	def print_clauses(self):
		for c in self.clauses:
			c.print_clause()
		
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
			self.clauses.remove(c)
	
	def printLiteralMembership(self, lit):
		print "lit: ", lit
	
	def getLiteralMembership(self, lit):
		return self.literalMembership[lit][1]
	
	def getLiteralValue(self, lit):
		return self.literalMembership[lit][0]
		
	def setLiteralMembership(self, lit, clause):
		print "lit membership ", lit
		if lit not in self.literalMembership:
			self.literalMembership[lit] = (None, [clause])
		else:
			if clause not in self.literalMembership[lit][1]:
				self.literalMembership[lit] = (self.literalMembership[lit][0], self.literalMembership[lit][1].append(clause))
	
	def setLiteralValue(self, lit, val):
		self.literalMembership[lit] = (val, self.literalMembership[lit][1])
		
	def simplifyFormula(self):
		for c in self.clauses:
			if c.isSatisfied():
				print "removing this clause"
				self.removeClause(c)
	
class Clause:
	
	def __init__(self, lits):
		self.literalList = lits
		self.num_of_literals = len(lits)
		self.num_of_zeros = 0
		self.num_of_ones = 0
	
	def print_clause(self):
		print "The literals in this clause are: ", self.literalList
		print "the number of literals is: ", self.num_of_literals
		print "the number of zeros at this point is: ", self.num_of_zeros
		print "the number of ones at this point is: ", self.num_of_ones
		print "++++++++++++++++++++++++++++++++++++++++++"
		
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
		if self.num_of_zeros == self.num_of_literals:
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

'''
class Literal:
	def __init__(self, name, ):
		self.name = name
		self.sign = sign
		self.val = None
		self.clauseMembership = []
	
	#getters:
	def getVal(self):
		return self.val
	
	def getName(self):
		return self.name
	
	def getSign(self):
		return self.sign
	
	def getMembership(self):
		return self.clauseMembership
	
	#set the value (True/False)
	def setVal(self, b):
		self.val = b
	
	#add clause to the membership list (clauses that include this literal)
	def addMembership(self, c):
		self.clauseMembership.append(c)
'''	
	
		
#class Constrain:
	 #def __init__(self):
	 #
	 #def remove(self):
	 #
	 #def simplify(self):
	 #
	 #def undo(self):
	 #
	 #def calculateReason(self):
	 
	 
s = Solver()