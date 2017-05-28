# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util
import sys
from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]


        
        "*** YOUR CODE HERE ***"

        ## Minimum food distance and the adds them to the list in order to use them later
        minDF = float(sys.maxint)
        for i, row in enumerate(newFood):
            for j, column in enumerate (newFood[i]):
                if (newFood[i][j] == True):
                    if (manhattanDistance((i, j), newPos) < minDF):
                        minDF = manhattanDistance((i, j), newPos)

        ## Minimum ghosts distance
        minDG = float(sys.maxint)
        for ghost in newGhostStates:
            if (manhattanDistance(ghost.getPosition(), newPos) < minDG):
                minDG = manhattanDistance(ghost.getPosition(), newPos)

        ## Minimum capsules distance
        newCapsules = successorGameState.getCapsules()
        minDC = float(sys.maxint)
        for capsules in newCapsules:
            if (manhattanDistance(capsules, newPos) < minDC):
                minDC = manhattanDistance(capsules, newPos)

        getScore = minDG + successorGameState.getScore() + minDC  #score for now

        if successorGameState.getPacmanPosition() in newCapsules: #prioritize capsules
            getScore += 130

        currFoodLeft = currentGameState.getNumFood()
        newFoodLeft = successorGameState.getNumFood()
        
        if (newFoodLeft < currFoodLeft):    #prioritize eating food
            getScore = getScore + 90

        ## This makes pacman keep on moving
        if action == Directions.STOP:
            getScore = getScore - 4
            
        getScore = getScore - (4 * minDF)

        if successorGameState.isWin() == True:
            return sys.maxint

        return getScore




def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"


        # we need the minimax value for each successor of the pacman(max) state
        # and choose the action with the highest value 

        legalA = gameState.getLegalActions(0)

        #for each possible action we will extract the successor
        #and for each successor we will call the value function
        #and we will choose the action that leads to the successor with the highest value
        maxval=-sys.maxint
        maxaction = None
        for a in legalA:
            sucVal = self.value(gameState.generateSuccessor(0, a), 1, 0)
            if sucVal > maxval:
                maxval = sucVal
                maxaction = a
        
        
        return maxaction
    
        util.raiseNotDefined()

    def value(self, gamestate, agentnum, currentDep):
        if gamestate.isWin():
            return self.evaluationFunction(gamestate)
        elif gamestate.isLose():
            return self.evaluationFunction(gamestate)
        elif currentDep == self.depth:
            return self.evaluationFunction(gamestate)
        elif agentnum==0:
            return self.maxvalue(gamestate, currentDep)
        else:
            return self.minvalue(gamestate, agentnum, currentDep)

    def maxvalue(self, gamestate, currentDep):
        v = -sys.maxint

        legalA = gamestate.getLegalActions(0)
        for a in legalA:
            v = max(v,self.value(gamestate.generateSuccessor(0, a), 1, currentDep))
        return v
        
    def minvalue(self, gamestate, agentnum, currentDep):
        v = sys.maxint

        if agentnum + 1 == gamestate.getNumAgents():
            currentDep = currentDep + 1
            nextagent = 0
        else:
            nextagent = agentnum + 1
            
        legalA = gamestate.getLegalActions(agentnum)
        for a in legalA:
            v = min(v,self.value(gamestate.generateSuccessor(agentnum, a),  nextagent, currentDep))

        return v
        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"


        #This code is different than the above, now we need the action so the value function
        #will return a tuple of score and action so that we get the action with the score here
        #the value, minvalue, and maxvalue functions are very similar but this time we added alpha and beta

        alpha = -sys.maxint
        beta = +sys.maxint
        
        return self.avalue(gameState, 0, 0, alpha, beta)[1]
    
        util.raiseNotDefined()


    def avalue(self, gamestate, agentnum, currentDep, alpha, beta):
        if gamestate.isWin():
            return self.evaluationFunction(gamestate), None
        elif gamestate.isLose():
            return self.evaluationFunction(gamestate), None
        elif currentDep == self.depth:
            return self.evaluationFunction(gamestate), None
        elif agentnum==0:
            return self.amaxvalue(gamestate, currentDep,alpha, beta)
        else:
            return self.aminvalue(gamestate, agentnum, currentDep,alpha, beta)

    def amaxvalue(self, gamestate, currentDep, alpha, beta):
        v = (-sys.maxint, None)

        legalA = gamestate.getLegalActions(0)
        for a in legalA:
            temp = self.avalue(gamestate.generateSuccessor(0, a), 1, currentDep,alpha, beta)
            if temp[0] > v[0]:
                v = (temp[0], a)
            if v[0] > beta:
                return v
            alpha = max(alpha,v[0])
        return v
        
    def aminvalue(self, gamestate, agentnum, currentDep, alpha, beta):
        v = (sys.maxint, None)

        if agentnum + 1 == gamestate.getNumAgents():
            currentDep = currentDep + 1
            nextagent = 0
        else:
            nextagent = agentnum + 1
            
        legalA = gamestate.getLegalActions(agentnum)
        for a in legalA:
            temp = self.avalue(gamestate.generateSuccessor(agentnum, a),  nextagent, currentDep,alpha, beta)
            if temp[0] < v[0]:
                v = (temp[0], a)
            if v[0]< alpha:
                return v
            beta = min(beta,v[0])
        return v
        
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"

        #This code is similar to the minimax search however the only changes are now we have
        # the expvalue function instead of the minvalue


        # we need the minimax value for each successor of the pacman(max) state
        # and choose the action with the highest value 

        legalA = gameState.getLegalActions(0)

        #for each possible action we will extract the successor
        #and for each successor we will call the value function
        #and we will choose the action that leads to the successor with the highest value
        maxval=-sys.maxint
        maxaction = None
        for a in legalA:
            sucVal = self.Evalue(gameState.generateSuccessor(0, a), 1, 0)
            if sucVal > maxval:
                maxval = sucVal
                maxaction = a
        
        
        return maxaction
    
        util.raiseNotDefined()

    def Evalue(self, gamestate, agentnum, currentDep):
        if gamestate.isWin():
            return self.evaluationFunction(gamestate)
        elif gamestate.isLose():
            return self.evaluationFunction(gamestate)
        elif currentDep == self.depth:
            return self.evaluationFunction(gamestate)
        elif agentnum==0:
            return self.Emaxvalue(gamestate, currentDep)
        else:
            return self.expvalue(gamestate, agentnum, currentDep)

    def Emaxvalue(self, gamestate, currentDep):
        v = -sys.maxint

        legalA = gamestate.getLegalActions(0)
        for a in legalA:
            v = max(v,self.Evalue(gamestate.generateSuccessor(0, a), 1, currentDep))
        return v
        
    def expvalue(self, gamestate, agentnum, currentDep):
        v = 0.0

        if agentnum + 1 == gamestate.getNumAgents():
            currentDep = currentDep + 1
            nextagent = 0
        else:
            nextagent = agentnum + 1
            
        legalA = gamestate.getLegalActions(agentnum)
        count = float(len(legalA))    #this will get the number of successors we have
        p = 1.0 / count               # because we are using a uniform prob 
        for a in legalA:
            v += p*self.Evalue(gamestate.generateSuccessor(agentnum, a),  nextagent, currentDep)

        return v

        
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    

    ## Minimum food distance and the adds them to the list in order to use them later
    minDF = float(sys.maxint)
    for i, row in enumerate(newFood):
        for j, column in enumerate (newFood[i]):
            if (newFood[i][j] == True):
                if (manhattanDistance((i, j), newPos) < minDF):
                    minDF = manhattanDistance((i, j), newPos)

    ## Minimum ghosts distance
    minDG = float(sys.maxint)
    for ghost in newGhostStates:
        if (manhattanDistance(ghost.getPosition(), newPos) < minDG):
            minDG = manhattanDistance(ghost.getPosition(), newPos)

    ## Minimum capsules distance
    newCapsules = currentGameState.getCapsules()
    minDC = float(sys.maxint)
    for capsules in newCapsules:
        if (manhattanDistance(capsules, newPos) < minDC):
            minDC = manhattanDistance(capsules, newPos)

    getScore = currentGameState.getScore()  - 5*minDF - 100* currentGameState.getNumFood()  #utility function

    if currentGameState.getPacmanPosition() in newCapsules:   #add priority to capsules
        getScore += 130

    x,y = currentGameState.getPacmanPosition()


    boolG = True
    if all(t > 1 for t in newScaredTimes):    # check if all ghosts are scared
        boolG = False



    if currentGameState.getNumFood()==0:  # we win
        return sys.maxint

    elif minDG<=1 and boolG:        #if all the ghosts are scared we dont need to care about them
        return -sys.maxint

    elif newFood[x][y]== True:      #prioritize getting the food
        return sys.maxint

    else:
        return getScore


    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

