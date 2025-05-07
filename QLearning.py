from random import randint, choice
from numpy.random import rand

ALPHA = 0.2
GAMMA = 0.8
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
                self.qTable[state] = [0, 0, 0, 0]  # UP DOWN LEFT RIGHT
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
            print("\033[1;31mExploration\033[0m", self.epsilon)
            self.choseExploration += 1
            return randint(0, 3)

        # Exploitation
        self.choseExploitation += 1
        return self.__getBestAction(state)

    def updateQValue(self, state, action, reward, nextState):
        dyingStates = [
            ((True, False, False, False), (False, False, False, False), (False, False, False, False)),
            ((False, True, False, False), (False, False, False, False), (False, False, False, False)),
            ((False, False, True, False), (False, False, False, False), (False, False, False, False)),
            ((False, False, False, True), (False, False, False, False), (False, False, False, False)),

        ]

        qValues = self.__getQValues(state)
        nextQValues = self.__getQValues(nextState)
        if state in dyingStates:
            print("state is", state)
            print("nextState is", nextState)
            print("next qValues", nextQValues)
            print("before", qValues)
        qValues[action] = qValues[action] + ALPHA *\
            (reward + GAMMA * max(nextQValues) - qValues[action])
        if state in dyingStates:
            print("after", qValues)
