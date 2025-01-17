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
import random, util, math

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
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        foodList = newFood.asList()

        closestFood = -1.0
        for food in foodList:
            closestFood = min(closestFood, manhattanDistance(newPos, food))

        for ghostPos in childGameState.getGhostPositions():
            if manhattanDistance(newPos, ghostPos) < 2:
                return -100
        closestGhost = manhattanDistance(newPos, newGhostStates[0].configuration.pos)

        return childGameState.getScore() + closestGhost / (closestFood * 10)
        # return childGameState.getScore() + 1.0/closestFood


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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
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

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        return max(gameState.getLegalActions(0),
                   key=lambda action: self.minValue(gameState.getNextState(0, action), 1, 1))

    def maxValue(self, gameState, agentIndex, depth):
        legalActions = gameState.getLegalActions(agentIndex)
        isTerminal = not legalActions or depth == self.depth

        if isTerminal:
            return self.evaluationFunction(gameState)  # utility

        v = -math.inf
        for action in legalActions:
            v = max(v, self.minValue(gameState.getNextState(0, action), 0 + 1, depth + 1))

        return v

    def minValue(self, gameState, agentIndex, depth):
        legalActions = gameState.getLegalActions(agentIndex)
        isTerminal = not legalActions

        if isTerminal:
            return self.evaluationFunction(gameState)  # utility

        v = math.inf
        for action in legalActions:
            if agentIndex == gameState.getNumAgents() - 1:
                v = min(v, self.maxValue(gameState.getNextState(agentIndex, action), 0, depth))
            else:
                v = min(v, self.minValue(gameState.getNextState(agentIndex, action), agentIndex + 1, depth))
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
        return self.maxValue(gameState, 0, 0, -math.inf, math.inf)

    def maxValue(self, gameState, agentIndex, depth, alpha, beta):
        legalActions = gameState.getLegalActions(agentIndex)
        isTerminal = not legalActions or depth == self.depth
        bestAction = 0

        if isTerminal:
            return self.evaluationFunction(gameState)  # utility

        v = -math.inf

        for action in legalActions:
            nextV = self.minValue(gameState.getNextState(0, action), 1, depth + 1, alpha, beta)

            if nextV > v and depth == 0:
                bestAction = action

            v = max(v, nextV)

            if v > beta:
                return v
            else:
                alpha = max(alpha, v)

        if depth == 0:
            return bestAction

        return v

    def minValue(self, gameState, agentIndex, depth, alpha, beta):
        legalActions = gameState.getLegalActions(agentIndex)
        isTerminal = not legalActions

        if isTerminal:
            return self.evaluationFunction(gameState)  # utility

        v = math.inf
        for action in legalActions:
            if agentIndex == gameState.getNumAgents() - 1:
                nextV = self.maxValue(gameState.getNextState(agentIndex, action), 0, depth, alpha, beta)
            else:
                nextV = self.minValue(gameState.getNextState(agentIndex, action), agentIndex + 1, depth, alpha, beta)

            v = min(v, nextV)

            if v < alpha:
                return v
            else:
                beta = min(beta, v)

        return v


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
        return max(gameState.getLegalActions(),
                   key=lambda action: self.expValue(gameState.getNextState(0, action), 1, 1))

    def maxValue(self, gameState, agentIndex, depth):
        legalActions = gameState.getLegalActions(agentIndex)
        isTerminal = not legalActions or depth == self.depth

        if isTerminal:
            return self.evaluationFunction(gameState)  # utility

        v = -math.inf
        for action in legalActions:
            v = max(v, self.expValue(gameState.getNextState(0, action), 0 + 1, depth + 1))

        return v

    def expValue(self, gameState, agentIndex, depth):
        legalActions = gameState.getLegalActions(agentIndex)
        isTerminal = not legalActions

        if isTerminal:
            return self.evaluationFunction(gameState)  # utility

        probability = 1.0 / len(legalActions)

        expected = 0
        for action in legalActions:
            if agentIndex == gameState.getNumAgents() - 1:
                expected += self.maxValue(gameState.getNextState(agentIndex, action), 0, depth) * probability
            else:
                expected += self.expValue(gameState.getNextState(agentIndex, action), agentIndex + 1, depth) \
                            * probability
        return expected



def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    evaluation = 0

    newPos = currentGameState.getPacmanPosition()
    foodList = currentGameState.getFood().asList()
    newGhostPos = currentGameState.getGhostPositions()
    capsuleList = currentGameState.getCapsules()

    closestFood = -1
    for food in foodList:
        closestFood = min(closestFood, manhattanDistance(newPos, food))

    closestGhost = 0
    for ghost in newGhostPos:
        closestGhost = manhattanDistance(newPos, ghost)

        if closestGhost < 2:
            return -1

    evaluation = currentGameState.getScore() + 1 / (len(foodList)+1) * 100 + 1 / closestFood * 10 + closestGhost

    if not capsuleList:
        closestCapsule = -1
        for capsule in capsuleList:
            closestCapsule = min(closestCapsule, manhattanDistance(newPos, capsule))

        evaluation += 1.0 / closestCapsule * 20 + len(capsuleList) * 40

    return evaluation



# Abbreviation
better = betterEvaluationFunction
