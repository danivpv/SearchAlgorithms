#!/usr/bin/env python3
import sys
from maze import Maze, Room
from fringe import Fringe
from state import State

MAX_DFS_DEPTH = 500000

def solveMazeGeneral(maze, algorithm, deepness=MAX_DFS_DEPTH):
	#select the right queue for each algorithm
	if algorithm == "BFS":
		fr = Fringe("FIFO")
	elif algorithm == "DFS":
		fr = Fringe("STACK")
	elif algorithm == "UCS":
		fr = Fringe("PRIO")
		prioFunc = lambda state, room: state.getCost()
	elif algorithm == "GREEDY":
		fr = Fringe("PRIO")
		prioFunc = lambda state, room: room.getHeuristicValue()
	elif algorithm == "ASTAR":
		fr = Fringe("PRIO")
		prioFunc = lambda state, room: state.getCost() + room.getHeuristicValue()
	elif algorithm == "IDS":
		solvedQ = False
		path = []
		for deepLim in range(deepness, MAX_DFS_DEPTH+1, deepness):
			path, solvedQ = solveMazeGeneral(maze, "DFS", deepLim)
			if solvedQ: break
		return path, solvedQ
	else:
		print("algorithm not found/implemented, exit")
		return [], False;
		
	room = maze.getRoom(*maze.getStart())
	state = State(room, None)

	if algorithm == "UCS" or algorithm == "GREEDY" or algorithm == "ASTAR":
		state.setPrio(prioFunc(state, room))

	fr.push(state)		
	path = []
	visited = set()

	while not fr.isEmpty():
	
		while not fr.isEmpty():
			state = fr.pop()
			room = state.getRoom()
			if room not in visited: break
		
		try: path.append(room.getCoords())
		except: break
		visited.add(room)
	
		if room.isGoal():
			print("solved")
			fr.printStats()
			state.printPath()
			maze.printMazeWithPath(state)
			print(state.sequenceItem_i())
			return path, True

		# loop through every possible move
		for d in room.getConnections():
			# get new room after move and cost to get there
			newRoom, cost = room.makeMove(d, state.getCost())
			# if it is an unvisited room
			if newRoom not in visited:
				newState = State(newRoom, state, cost)

				if algorithm == "UCS" or algorithm == "GREEDY" or algorithm == "ASTAR":
					newState.setPrio(prioFunc(newState, newRoom))

				if algorithm == "DFS":
					newState.setDeep(state.getDeep() + 1)
					if deepness >= newState.getDeep():
						fr.push(newState)
				else: fr.push(newState)


	if deepness == MAX_DFS_DEPTH:
		print("not solved")
		fr.printStats()

	return path, False

