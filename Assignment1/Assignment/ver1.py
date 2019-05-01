#!/usr/bin/env python3
import sys
from maze import Maze, Room
from fringe import Fringe
from state import State

def solveMazeGeneral(maze, algorithm):
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
	else:
		print("algorithm not found/implemented, exit")
		return;
		
	room = maze.getRoom(*maze.getStart())
	state = State(room, None)

	if algorithm == "UCS" or algorithm == "GREEDY" or algorithm == "ASTAR":
		state.setPrio(prioFunc(state, room))

	fr.push(state)		
	path = []
	visited = set()

	while not fr.isEmpty():
	
		while True:
			state = fr.pop()
			room = state.getRoom()
			if room not in visited: break

		path.append(room.getCoords())
		visited.add(room)
	
		if room.isGoal():
			print("solved")
			fr.printStats()
			state.printPath()
			maze.printMazeWithPath(state)
			return path

		# loop through every possible move
		for d in room.getConnections():
			# get new room after move and cost to get there
			newRoom, cost = room.makeMove(d, state.getCost())
			# if it is an unvisited room
			if newRoom not in visited:
				newState = State(newRoom, state, cost)

				if algorithm == "UCS" or algorithm == "GREEDY" or algorithm == "ASTAR":
					newState.setPrio(prioFunc(state, room))
				
				fr.push(newState)

				
	print("not solved")
	fr.printStats()

	return path

