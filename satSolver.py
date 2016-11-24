import random
from nltk.tokenize import word_tokenize

class Solver:
	
	def __init__(self):
		p = Parser()
		self.n = Next()
		self.f = p.parseText() #this is my formula object
		
		self.decisions = {}
		self.unassigned = self.f.get_unassignedList()
		
	def solve(self):	
		self.satisfiable, self.decisions = self.backtrackSearch(self.unassigned, self.decisions)
		if self.satisfiable == True:
			print "\n"
			print "\n"
			print "\n"
			print "This formula is satisfiable"
			print "A possible assignment is: "
			print self.decisions
			print "\n"
			print "\n"
			print "\n"
			#print "len of decisions is: ", len(self.decisions)
			return True
		else:
			print "This formula is not satisfibale"
			return False
			
	def nextAssign(self, unassigned):
		lit, val = self.n.getSorted(unassigned)
		return lit, val
	
	def undoPropagation(self, lit, v):
		self.f.resetLiteralValue(lit)
		clauseMembership = self.f.getLiteralMembership(lit)
		if clauseMembership != None:
			for c in clauseMembership:
				if v == True:
					c.sub_ones()
				else:
					c.sub_zeros()
				
	def propagationStep(self, lit, val):
		#print "propagation step: ---------------------------------"
		#print "lit and val passed are: ", lit, val
		clauseMembership = self.f.getLiteralMembership(lit)
		assigned = [(lit, val)]

		if clauseMembership != None:
			for c in clauseMembership:
				if val == True:
					c.add_ones()
				else:
					c.add_zeros()
				
				if c.isConflict():
					#print "Conflict"
					self.undoPropagation(lit, val)
					self.undoPropagation(-1*lit, not val)
					return False , []
					
				elif c.isUnitClause():
					lits = c.get_literalList()
					
					for l in lits:
						if self.f.getLiteralValue(l) == None:
							#print "unit clause"
							
							unit = l
							self.f.setLiteralValue(unit, True)
							self.f.setLiteralValue(-1*unit, False)
				
							p, a = self.propagationStep(unit, True)
							if p == False:
								self.undoPropagation(lit, val)
								self.undoPropagation(-1*lit, not val)
								return False
							#p is True	
							assigned += a
								
							p1, a1 = self.propagationStep(-1*unit, False)
							if p1 == False:
								self.undoPropagation(lit, val)
								self.undoPropagation(-1*lit, not val)
								for v in assigned:
									self.undoPropagation(v[0], v[1])
									self.undoPropagation(-1*v[0], not v[1])
								return False #, assigned
							#(both p and p1 are True)
							assigned += a1
							break
		return True, assigned
	
	def backtrackSearch(self, unassigned, decisions):
		#print "Backtracking step: ---------------------------------"
		#print "unassigned is:"
		#print unassigned
		#print "len of unassigned is ", len(unassigned)
		#print "decisions"
		#print decisions
		
		d = {}
		if len(unassigned) == 0:
			return True, decisions
		
		lit, val = self.nextAssign(unassigned)
		unassigned.remove(lit)
		
		for v in [val, not val]: #maybe modify this to make it more generic
			self.f.setLiteralValue(lit, v)
			self.f.setLiteralValue(-1*lit, not v)
			d[lit] = v
			
			p, a = self.propagationStep(lit, v)
			if p == True:
				for pair in a:
					if pair[0] in unassigned:
						unassigned.remove(pair[0])
				p1, a1 = self.propagationStep(-1*lit, not v)
				if p1 == False:
					for vi in a:
						self.undoPropagation(vi[0], vi[1])
						self.undoPropagation(-1*vi[0], not vi[1])
				else:	
					d.update(a)
					d.update(a1)
					#print "propagation step did not cause conflict for: "
					#print lit, v
					#print d
					#print "LLLLLLL"
					#print "im going to backtrack \n"
					
								
					while len(unassigned) != 0:
						b, d1 = self.backtrackSearch(unassigned, d)
						if b == True:
							d.update(d1)
							#print "d updated ", d
						else:
							self.undoPropagation(lit, v)
							self.undoPropagation(-1*lit, not v)
							return False, decisions
					return True, d
		return False, decisions
				


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
				self.f.addToUnassigned(abs(lit)) #adding to set of unassigned variables
				
				self.f.setLiteralMembership(lit, c)
				
			
			i += 1 # increment clause index
		return self.f

class Next:
	
	def randomDecision(self, unassigned):
		lit = random.choice(unassigned)
		val = random.choice([True, False])
		return lit, val

	def getSorted(self, unassigned):
		lit = sorted(unassigned)[0]
		#print "\n"
		#print "lis is: ", lit
		#print "\n"
		val = random.choice([True, False])
		return lit, val
		
		 
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
		if lit in self.literalMembership:
			print "Yesss"
		else:
			print "NOooo"
	
	def getLiteralMembership(self, lit):
		if lit in self.literalMembership:
			return self.literalMembership[lit][1]
		else:
			return {}
			
	def getLiteralValue(self, lit):
		if lit in self.literalMembership:
			return self.literalMembership[lit][0]
		else:
			return None
				
	def setLiteralMembership(self, lit, clause):
		#print lit
		#print "This should print the clause:"
		#clause.print_clause()
			
		if lit not in self.literalMembership:
			self.literalMembership[lit] = (None, [clause])
			
		else:
			if self.literalMembership[lit][1] == None:
				#print "here1"
				self.literalMembership[lit] = (self.literalMembership[lit][0], [clause])
			elif clause not in self.literalMembership[lit][1]:
				#print "here2"
				self.literalMembership[lit] = (self.literalMembership[lit][0], self.literalMembership[lit][1].append(clause))
	
	def setLiteralValue(self, lit, val):
		if lit in self.literalMembership:
			self.literalMembership[lit] = (val, self.literalMembership[lit][1])
	
	def resetLiteralValue(self, lit):
		if lit in self.literalMembership:
			self.literalMembership[lit] = (None, self.literalMembership[lit][1])
	
		
	def simplifyFormula(self):
		for c in self.clauses:
			if c.isSatisfied():
				#print "removing this clause"
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
	
	def sub_ones(self):
		self.num_of_ones -= 1
		
	def sub_zeros(self):
		self.num_of_zeros -= 1
		
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

s = Solver()
sat = s.solve()