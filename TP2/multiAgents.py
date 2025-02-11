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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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
        newFood = currentGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        newFoodPositions = newFood.asList()
        newGhostPositions = [ghost.getPosition() for ghost in newGhostStates]
        distanceToFood = []
        distanceToGhost = []
        score = 0

        if newPos in newGhostPositions:
            if newScaredTimes[newGhostPositions.index(newPos)]>0:
                return 100
            return -100

        if newPos in newFoodPositions:
            return 100
        
        if action is Directions.STOP:
            return -100

        return  0

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
        
        nbGhost = gameState.getNumAgents() - 1
        
        def Max_value(state, index, depthCount):
            if state.isWin() or state.isLose() or depthCount >= self.depth:
                return self.evaluationFunction(state)
            
            v = float("-inf")

            for action in state.getLegalActions(index):
                successor = state.generateSuccessor(index, action)
                v = max(v, Min_value(successor, index + 1, depthCount))

            return v

        def Min_value(state, index, depthCount):
            if state.isWin() or state.isLose() or depthCount >= self.depth:
                return self.evaluationFunction(state)
            
            v = float("inf")

            for action in state.getLegalActions(index):
                successor = state.generateSuccessor(index, action)

                if index < nbGhost:
                    v = min(v, Min_value(successor, index + 1, depthCount))
                else:
                    v = min(v, Max_value(successor, 0, depthCount + 1))

            return v


        v = float("-inf")
        successor_value = float("-inf")
        best_action = ""

        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            successor_value = max(successor_value, Min_value(successor, 1, 0))
        
            if successor_value > v:
                v = successor_value
                best_action = action 

        return best_action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        nbGhost = gameState.getNumAgents() - 1
        
        def Max_value(state, alpha, beta, index, depthCount):
            if state.isWin() or state.isLose() or depthCount >= self.depth:
                return self.evaluationFunction(state)
            
            v = float("-inf")

            for action in state.getLegalActions(index):
                successor = state.generateSuccessor(index, action)
                v = max(v, Min_value(successor, alpha, beta, index + 1, depthCount))
                if v > beta:
                    return v
                alpha = max(alpha, v)

            return v

        def Min_value(state, alpha, beta, index, depthCount):
            if state.isWin() or state.isLose() or depthCount >= self.depth:
                return self.evaluationFunction(state)
            
            v = float("inf")

            for action in state.getLegalActions(index):
                successor = state.generateSuccessor(index, action)

                if index < nbGhost:
                    v = min(v, Min_value(successor,alpha, beta, index + 1, depthCount))
                else:
                    v = min(v, Max_value(successor, alpha, beta, 0, depthCount + 1))

                if v < alpha:
                    return v
                beta = min(beta, v)

            return v

        v = float("-inf")
        successor_value = float("-inf")
        best_action = ""
        alpha = float("-inf")
        beta = float("inf")

        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            successor_value = max(successor_value, Min_value(successor, alpha, beta, 1, 0))
        
            if successor_value > v:
                v = successor_value
                best_action = action

            if v > beta:
                return v
            
            alpha = max(alpha, v) 

        return best_action

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
        nbGhost = gameState.getNumAgents() - 1

        def expectimax(state, depth, index):
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)

            if index == 0: 
                v = float("-inf")

                for action in state.getLegalActions(index):
                    successor = state.generateSuccessor(index, action)
                    v = max(v, expectimax(successor, depth, index + 1))

                return v
            else:
                sumProb = 0
                prob = 1 / len(state.getLegalActions(index))
                
                for action in state.getLegalActions(index):
                    successor = state.generateSuccessor(index, action)

                    if index < nbGhost:
                        sumProb += expectimax(successor, depth, index + 1) * prob
                    else:
                        sumProb += expectimax(successor, depth - 1, 0) * prob

                return sumProb

        best_value = float("-inf")
        best_action = ""

        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            action_value = expectimax(successor, self.depth, 1)

            if action_value > best_value:
                best_value = action_value
                best_action = action

        return best_action


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
