from random import randint, choice
from numpy.random import rand

ALPHA = 0.1
GAMMA = 0.9
EPSILON_FACTOR = 0.997


class QLearning:
    def __init__(self):
        self.qTable = {}
        self.epsilon = 1.0

        # Debug
        self.choseExploration = 0
        self.choseExploitation = 0

    # Private

    def __getQValues(self, state):
        try:
            if state not in self.qTable:
                if state != ("DEAD", "DEAD", "DEAD"):
                    self.qTable[state] = [0, 0, 0, 0]  # UP DOWN LEFT RIGHT
                else:
                    self.qTable[state] = [-1000, -1000, -1000, -1000]
            return self.qTable[state]
        except TypeError:
            return [0, 0, 0, 0]

    def __getBestAction(self, state):
        qValues = self.__getQValues(state)
        maxValue = max(qValues)
        maxIndices = [i for i, value in enumerate(qValues)
                      if value == maxValue]
        return choice(maxIndices)

    # Public

    def chooseAction(self, state):
        # Exploration
        if rand() < self.epsilon:
            self.epsilon *= EPSILON_FACTOR
            self.choseExploration += 1
            return randint(0, 3)

        # Exploitation
        self.choseExploitation += 1
        return self.__getBestAction(state)

    def updateQValue(self, state, action, reward, nextState):
        qValues = self.__getQValues(state)
        nextQValues = self.__getQValues(nextState)
        qValues[action] = qValues[action] + ALPHA *\
            (reward + GAMMA * max(nextQValues) - qValues[action])
