from Game import Game
from State import State
from QLearning import QLearning
from Results import plotResults, saveResults, loadResults

import time


class Training:
    LEARNING = QLearning()

    def __init__(self, params):
        self.sessions = params.sessions
        self.size = params.size
        self.save = params.save
        self.choosetosave = params.choosetosave
        self.load = params.load
        self.dontlearn = params.dontlearn
        self.visual = params.visual
        self.speed = params.speed
        self.plot = params.plot
        self.ui = params.ui
        self.stepbystep = params.stepbystep
        self.nerd = params.nerd

        if self.size < 5:
            print("\033[91m\033[1mEXCEPTION RAISED: Size must be at least 5.\
 Setting grid size to 5.\033[0m")
            self.size = 5

    # Private

    def __getReward(self, currentCell):
        if currentCell == 'R':
            return -100
        elif currentCell == 'G':
            return 1000
        elif currentCell == 'W' or currentCell == 'S':
            return -100000
        else:
            return -1

    # Public

    def run(self, g: Game, s: State, canExplore=True):

        currentState = s.getState()
        action = self.LEARNING.chooseAction(currentState, canExplore)
        direction = ['U', 'D', 'L', 'R'][action]
        currentCell = g.update(direction)

        if self.dontlearn is False:
            if g.snake.size == 0:
                nextState = [[False, False, False, False],
                             [False, False, False, False],
                             [False, False, False, False]]
            else:
                nextState = s.getState()

            reward = self.__getReward(currentCell)
            self.LEARNING.updateQValue(currentState, action,
                                       reward, nextState)

        return direction

    def train(self):
        durations, sizes = [], []

        if self.load:
            self.LEARNING.qTable = loadResults(self.load)

        if self.sessions < 1:
            print("\033[93m\033[1mRequested an invalid number of training\
 sessions. Skipped training.\033[0m")
            return

        startTime = time.time()
        for sessionNumber in range(self.sessions):
            if sessionNumber % (self.sessions / 10) == 0\
                    or time.time() - startTime > 10:
                print("\033[93mTraining progress: ",
                      int(sessionNumber / self.sessions * 100),
                      "% (", sessionNumber, "/", self.sessions,
                      ")\033[0m", sep='')

            if time.time() - startTime > 10:
                startTime = time.time()

            g = Game(self.size)
            s = State(g)
            currentDuration = 0

            while g.gameOver is False:
                self.run(g, s)
                currentDuration += 1

            sizes.append(g.snake.size)
            durations.append(currentDuration)

        # Results
        print("\033[92m\033[1mTraining is completed!\033[0m")

        print("Highest length: ", max(sizes),
              ", with the duration on this run being ",
              durations[sizes.index(max(sizes))], ", achieved on run #",
              sizes.index(max(sizes)), sep='')

        print("Highest duration: ", max(durations),
              ", with the size on this run being ",
              sizes[durations.index(max(durations))], ", achieved on run #",
              durations.index(max(durations)), sep='')

        print("Exploration:", self.LEARNING.choseExploration,
              ", Exploitation:", self.LEARNING.choseExploitation)

        if self.plot:
            plotResults(durations, sizes)

        if self.save:
            saveResults(self.LEARNING.qTable, self.save)
        elif self.choosetosave:
            if input("Do you want to save the results? (y/n): ") == 'y':
                outfile = input("Enter the file name: ")
                saveResults(self.LEARNING.qTable, outfile)
