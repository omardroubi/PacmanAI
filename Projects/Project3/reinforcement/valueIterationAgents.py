# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util
import sys
import time

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"


        for i1 in range(0,self.iterations):
            
            newValCounter = util.Counter()   #we need a temporary new Value counter because we will use old values of changed ones in the process
            for s in self.mdp.getStates():
                maxV = float('-inf')
                for a in self.mdp.getPossibleActions(s):
                    summ = 0.0
                    for transPb in self.mdp.getTransitionStatesAndProbs(s,a):
                        nextState,p = transPb
                        summ += p*(self.mdp.getReward(s,a,nextState) + self.discount*self.getValue(nextState))
                    if summ > maxV:
                        maxV = summ
                    newValCounter[s] = maxV

            self.values = newValCounter     #now we can update self.values after iterating through all states
                        
                    
                
        
        

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        Qval = 0.0
        for transPb in self.mdp.getTransitionStatesAndProbs(state,action):
            nextState,p = transPb
            Qval += p*(self.mdp.getReward(state,action,nextState) + self.discount*self.getValue(nextState))
        return Qval
    
        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"

        maxQv = float('-inf')
        maxAc = None
        for a in self.mdp.getPossibleActions(state):
            temp = self.computeQValueFromValues(state, a)
            if temp > maxQv:
                maxQv = temp
                maxAc = a

        return maxAc
        
        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"

        listOfStates = self.mdp.getStates()
        numbOfStates = len(listOfStates)

        for i1 in range(0,self.iterations):
            s = listOfStates[i1%numbOfStates]
            if (self.mdp.isTerminal(s)==False):
                maxV = float('-inf')
                listOfActions = self.mdp.getPossibleActions(s)
                nAc = len(listOfActions)
                if nAc != 0:
                    for a in listOfActions:
                        summ = 0.0
                        for transPb in self.mdp.getTransitionStatesAndProbs(s,a):
                            nextState,p = transPb
                            summ += p*(self.mdp.getReward(s,a,nextState) + self.discount*self.getValue(nextState))
                        if summ > maxV:
                            maxV = summ
                    self.values[s] = maxV
        

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta

        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"

        predecessors = {}
        for s in self.mdp.getStates():
            predecessors[s] = set()

        pQ = util.PriorityQueue()

        for s in self.mdp.getStates():
            if self.mdp.isTerminal(s)==False:
                
                for a in self.mdp.getPossibleActions(s):
                    for successor, prob in self.mdp.getTransitionStatesAndProbs(s, a):
                        if prob > 0:
                            predecessors[successor].add(s)



                
                maxQV = -float(sys.maxint)
                for a in self.mdp.getPossibleActions(s):
                    if self.getQValue(s, a)>maxQV:
                        maxQV = self.getQValue(s, a)
                    
                diff = abs(self.values[s] - maxQV)
                pQ.push(s, -diff)

        start = time.time()
        for i in range(0,self.iterations):
            if pQ.isEmpty():
                break

            s = pQ.pop()

            
            maxQV = -float(sys.maxint)
            for a in self.mdp.getPossibleActions(s):
                if self.getQValue(s, a)>maxQV:
                    maxQV = self.getQValue(s, a)
            self.values[s] = maxQV

        for p in predecessors[s]:
            maxQV = -float(sys.maxint)
            for a in self.mdp.getPossibleActions(p):
                if self.getQValue(p, a)>maxQV:
                    maxQV = self.getQValue(p, a)
                
            diff = abs(self.values[p] - maxQV)

            if diff > self.theta:
                pQ.update(p, -diff)                












                


        

