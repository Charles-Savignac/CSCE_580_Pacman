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
        for _ in range(self.iterations):
            valueCopy=self.values.copy()
            for state in self.mdp.getStates():

                if self.mdp.isTerminal(state):
                    continue

                qValue=float('-inf')
                for action in self.mdp.getPossibleActions(state):
                    if self.getQValue(state,action)>qValue:
                        qValue=self.getQValue(state,action)
                        valueCopy[state]=qValue
            self.values=valueCopy

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
        qValue=0
        for nextState, prob in self.mdp.getTransitionStatesAndProbs(state,action):
            qValue+=prob*(self.mdp.getReward(state,action,nextState)+self.discount*self.getValue(nextState))
        
        return qValue

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        maxValue=float('-inf')
        bestAction=None
     
        if self.mdp.isTerminal(state):
            return None
        
        for action in self.mdp.getPossibleActions(state):
            
            if self.getQValue(state,action) > maxValue:
                bestAction=action
                maxValue=self.getQValue(state,action)
        
        return bestAction

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
        states = self.mdp.getStates()
        index = 0

        for _ in range(self.iterations):

            valueCopy=self.values.copy()

            if index >= len(states):
                index = 0

            state = states[index]

            if self.mdp.isTerminal(state):
                index += 1
                continue

            maxQValue = float('-inf')

            for action in self.mdp.getPossibleActions(state):
                qValue = self.getQValue(state, action)
                maxQValue = max(maxQValue, qValue)

            valueCopy[state] = maxQValue
            self.values = valueCopy
            index += 1

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
        states = self.mdp.getStates()
        predecessors = {}
        queue = util.PriorityQueue()

        for state in states:
            if state not in predecessors:
                predecessors[state] = set()

            for action in self.mdp.getPossibleActions(state):
                for next_state, prob in self.mdp.getTransitionStatesAndProbs(state, action):
                    if prob > 0:
                        if next_state not in predecessors:
                            predecessors[next_state] = set()

                        predecessors[next_state].add(state)

        for state in states:
            if not self.mdp.isTerminal(state):
                maxQValue = float('-inf')

                for action in self.mdp.getPossibleActions(state):
                    qValue = self.getQValue(state, action)
                    maxQValue = max(maxQValue, qValue)
                
                diff = abs(self.values[state] - maxQValue)
                queue.push(state, -diff)

        for _ in range(self.iterations):
            if queue.isEmpty():
                break

            state = queue.pop()

            if not self.mdp.isTerminal(state):
                maxQValue = float('-inf')
                
                for action in self.mdp.getPossibleActions(state):
                    qValue = self.getQValue(state, action)
                    maxQValue = max(maxQValue, qValue)

                self.values[state] = maxQValue

            for pred in predecessors[state]:
                maxQValue = float('-inf')
                
                for action in self.mdp.getPossibleActions(pred):
                    qValue = self.getQValue(pred, action)
                    maxQValue = max(maxQValue, qValue)
                
                diff = abs(self.values[pred] - maxQValue)
                
                if diff > self.theta:
                        queue.update(pred, -diff)