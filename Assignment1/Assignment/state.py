#!/usr/bin/env python3

class State:
	"""Class to save the possible states in"""
	def __init__(self, room, parent, cost=0, prio=0, deepness=0):
		self.parent = parent
		self.room = room
		self.cost = cost
		self.prio = prio
		self.deepness = deepness

	# returns the current room
	def getRoom(self):
		return self.room

	# returns the previous state
	def getParent(self):
		return self.parent

	# returns the cost of the state
	def getCost(self):
		return self.cost

	# returns the deepness of the state
	def getDeep(self):
		return self.deepness

	# sets the cost of the state
	def setCost(self, cost):
		self.cost = cost

	# sets the priority of the state
	def setPrio(self, prio):
		self.prio = prio

	# sets the deepness of the state
	def setDeep(self, deepness):
		self.deepness = deepness

	# helper function to print the path
	def printPathHelper(self):
		s = ""
		if self.parent is not None:
			self.parent.printPathHelper()
			s =  str(self.parent.room.coords) + " -> "
			s += str(self.room.coords)
			s += " cost: "+str(self.cost)
			print(s)

	def comingFrom(self):
		movement = tuple(x-y for x, y in zip(self.parent.room.coords, self.room.coords))
		if movement == (0,0,-1):
			return "U"
		elif movement == (0,0,1):
			return "D"
		elif movement == (-1,0,0):
			return "E"
		elif movement == (1,0,0):
			return "W"
		elif movement == (0,-1,0):
			return "S"
		elif movement == (0,1,0):
			return "N"
		else: 
			return ""

	def sequenceItem_i(self):
		s = ""
		if self.parent is not None:
			s = self.parent.sequenceItem_i()
			s += self.comingFrom()
		return s
		
	# prints the found path
	def printPath(self):
		self.printPathHelper()
		print()

	# function used to compare two states for the priority queue
	def __lt__(self, other):
		return self.prio < other.prio


