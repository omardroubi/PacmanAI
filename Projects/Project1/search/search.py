# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

## Anis Assi & Omar El Droubi
## University of California, Berkeley
## PROJECT 1

import util

# SEARCH PROBLEM Class

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]


## Node Class: Used for searching the nodes and saving the correct path while expanding them in dfs and bfs
## Each node stores the state and its path
class Node:
    def __init__(self, state, pathList):
        self.state = state   #stores the state
        self.pathList = pathList # stores the path

## Depth First Search Algorithm! Keeps on expanding each node while saving its path until it finds the goal node
def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    fringe = util.Stack()       ## The fringe to store the nodes
    state0 = problem.getStartState()  ## Start State
    
    closed = [] ## stores the nodes that were searched previously in order not to search them again

    n0 = Node(state0, [])
    fringe.push(n0)  

    #The Loop
    while True:

        # Returns NONE when the graph was searched completely and the goal state wasn't found
        if fringe.isEmpty():
            return None   #check
        n = fringe.pop()

        ## Returns the pathlist when the goal state is found
        if problem.isGoalState(n.state):
            return n.pathList

        # The loop: Adds the successors to the list and checks if it was searched previously
        if  n.state not in closed:
            closed.append(n.state)
            for successor in problem.getSuccessors(n.state):
                n1 = Node(successor[0],list(n.pathList))
                n1.pathList.append(successor[1])
                fringe.push(n1)
        
    util.raiseNotDefined()

## Breadth First Search Algorithm! Similar to Depth First Search except that it searches by levels
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    fringe =util.Queue()
    state0= problem.getStartState()
    
    closed = [] ## stores the nodes that were searched previously in order not to search them again

    n0 = Node(state0, [])
    fringe.push(n0)  


    while True:   
        if fringe.isEmpty():
            return None   
        n = fringe.pop()
        
        if problem.isGoalState(n.state):
            return n.pathList
        
        # expands the node if it wasn't searched previously
        if  n.state not in closed:
            closed.append(n.state)
            for successor in problem.getSuccessors(n.state):
                n1 = Node(successor[0],list(n.pathList))
                n1.pathList.append(successor[1])
                fringe.push(n1)

    util.raiseNotDefined()


## Node Priority Class: Used for searching the nodes and saving the correct path !!And also to save each node's priority!! while expanding them in dfs and bfs
## Each nodep stores the state, the path, and the priority
class Nodep:
    def __init__(self, state, pathList, priority):
        self.state = state
        self.pathList = pathList
        self.priority = priority

## UCS Algorithm! Searches depending on the cheaper cost
def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    fringe =util.PriorityQueue()    
    state0= problem.getStartState()
    
    closed = []

    n0 = Nodep(state0, [],0)
    fringe.push(n0, 0)  


    while True:   
        if fringe.isEmpty():
            return None   #check
        n = fringe.pop()
        
        if problem.isGoalState(n.state):
            return n.pathList
        
        # expands the node if it wasn't searched previously
        if  n.state not in closed:
            closed.append(n.state)
            for successor in problem.getSuccessors(n.state):
                n1 = Nodep(successor[0],list(n.pathList),successor[2] + n.priority)
                n1.pathList.append(successor[1])
                fringe.push(n1, successor[2] + n.priority)

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

## A* Search: Sums the heuristic with the cost and chooses to expand the node that is has lowest sum
def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    fringe =util.PriorityQueue()    
    state0= problem.getStartState()
    
    closed = [] ## stores the nodes that were searched previously in order not to search them again

    n0 = Nodep(state0, [],heuristic(state0,problem))
    fringe.push(n0, heuristic(state0,problem))  

    while True:   
        if fringe.isEmpty():
            return None   #check
        n = fringe.pop()

        ## Returns the path when the goal state is found
        if problem.isGoalState(n.state):
            return n.pathList

        # expands the node if it wasn't searched previously
        if  n.state not in closed:
            closed.append(n.state)
            for successor in problem.getSuccessors(n.state):
                n1 = Nodep(successor[0],list(n.pathList),successor[2] + n.priority - heuristic(n.state,problem) + heuristic(successor[0],problem) )
                n1.pathList.append(successor[1])
                fringe.push(n1, successor[2] + n.priority - heuristic(n.state,problem) + heuristic(successor[0],problem) )
    
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
