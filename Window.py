from Training import Training
from Game import Game
from State import State

from math import floor
import pygame
pygame.init()

WIDTH_OFFSET = 100
HEIGHT_OFFSET = 150
FONT_SIZE = 14
OFFSET_LEFT_TEXT = 20
FREE_SPACE_ON_RIGHT = 30


class Window:
    def __init__(self, training: Training):

        self.training = training
        self.stepbystep = training.stepbystep
        self.nerd = training.nerd

        self.speed = training.speed
        if self.speed < 1:
            print("\033[91m\033[1mEXCEPTION RAISED: Speed must be at least 1.\
 Setting speed to 10.\033[0m")
            self.speed = 10

        if training.size >= 35:
            self.CELL_SIZE = max(int(
                30 - floor((training.size - 35) / 5 + 1) * 5), 10)
        else:
            self.CELL_SIZE = 30
        print(self.CELL_SIZE)
        SIZE = (training.size + 2) * self.CELL_SIZE + 270, \
               (training.size + 2) * self.CELL_SIZE

        self.SCREEN = pygame.display.set_mode(SIZE)
        self.CLOCK = pygame.time.Clock()
        pygame.display.set_caption("Learn2Slither")

    def draw(self, game: Game):
        for x in range(0, (self.training.size + 2) * self.CELL_SIZE,
                       self.CELL_SIZE):
            for y in range(0, (self.training.size + 2) * self.CELL_SIZE,
                           self.CELL_SIZE):

                cell = game.board[y // self.CELL_SIZE][x // self.CELL_SIZE]
                if cell == '0':  # Empty
                    pygame.draw.rect(self.SCREEN, "grey",
                                     (x + WIDTH_OFFSET, y, self.CELL_SIZE,
                                      self.CELL_SIZE))
                elif cell == 'H':  # Head
                    pygame.draw.rect(self.SCREEN, "yellow",
                                     (x + WIDTH_OFFSET, y, self.CELL_SIZE,
                                      self.CELL_SIZE))
                elif cell == 'S':  # Body segment
                    pygame.draw.rect(self.SCREEN, "blue",
                                     (x + WIDTH_OFFSET, y, self.CELL_SIZE,
                                      self.CELL_SIZE))
                elif cell == 'R':  # Red apple
                    pygame.draw.rect(self.SCREEN, "red",
                                     (x + WIDTH_OFFSET, y, self.CELL_SIZE,
                                      self.CELL_SIZE))
                elif cell == 'G':  # Green apple
                    pygame.draw.rect(self.SCREEN, "green",
                                     (x + WIDTH_OFFSET, y, self.CELL_SIZE,
                                      self.CELL_SIZE))
                else:  # Wall
                    pygame.draw.rect(self.SCREEN, "black",
                                     (x + WIDTH_OFFSET, y, self.CELL_SIZE,
                                      self.CELL_SIZE))

                pygame.draw.rect(self.SCREEN, "black",
                                 (x + WIDTH_OFFSET, y, self.CELL_SIZE,
                                  self.CELL_SIZE), 1)

    def drawText(self, game, duration, lastDirection):
        firstLine = "Score: " + str(game.snake.size)
        secondLine = "Duration: " + str(duration)
        thirdLine = "Last Direction:"
        fourthLine = lastDirection
        content = [firstLine, secondLine, thirdLine, fourthLine]

        screenHeight = self.SCREEN.get_height() - HEIGHT_OFFSET
        font = pygame.font.SysFont("Arial", FONT_SIZE)

        for i, line in enumerate(content):
            textSurface = font.render(line, True, "white")
            textRect = textSurface.get_rect()
            if i != 3:
                textRect.topleft = (OFFSET_LEFT_TEXT,
                                    screenHeight / 2 * i + self.CELL_SIZE)
            else:
                textRect.topleft = (OFFSET_LEFT_TEXT,
                                    screenHeight / 2 * (i-1) + self.CELL_SIZE
                                    + 20)
            self.SCREEN.blit(textSurface, textRect)

    def drawNerdText(self, game, state):
        currentState = state.getState()
        if currentState in self.training.LEARNING.qTable:
            qValues = self.training.LEARNING.qTable[currentState]
        else:  # Should never happen, putting this just in case
            qValues = [0, 0, 0, 0]

        firstLine = "Coordinates: " + str(game.snake.getHead())
        secondLine = ("Danger: ", str(currentState[0]))
        thirdLine = ("Red Apple: ", str(currentState[1]))
        fourthLine = ("Green Apple: ", str(currentState[2]))
        content = [firstLine, secondLine, thirdLine, fourthLine]

        screenHeight = self.SCREEN.get_height()
        screenWidth = self.SCREEN.get_width() - 50
        fontSize = min(15, max(10, (screenHeight - self.CELL_SIZE * 2) / 15))

        font = pygame.font.SysFont("Arial", fontSize)

        for i, line in enumerate(content):
            if i == 0:
                textSurface = font.render(line, True, "white")
                textRect = textSurface.get_rect()
                textRect.topleft = (screenWidth - WIDTH_OFFSET, self.CELL_SIZE)
                self.SCREEN.blit(textSurface, textRect)
            else:
                splitState = line[1].split(',')

                firstPart = font.render(line[0], True, "white")
                secondPart = font.render(str(splitState[:2]), True, "white")
                thirdPart = font.render(str(splitState[2:]), True, "white")

                firstPartRect = firstPart.get_rect()
                secondPartRect = secondPart.get_rect()
                thirdPartRect = thirdPart.get_rect()

                firstPartRect.topleft = (screenWidth - WIDTH_OFFSET,
                                         screenHeight / 5 * i)
                secondPartRect.topleft = (screenWidth - WIDTH_OFFSET,
                                          screenHeight / 5 * i + fontSize)
                thirdPartRect.topleft = (screenWidth - WIDTH_OFFSET,
                                         screenHeight / 5 * i + fontSize * 2)

                self.SCREEN.blit(firstPart, firstPartRect)
                self.SCREEN.blit(secondPart, secondPartRect)
                self.SCREEN.blit(thirdPart, thirdPartRect)

        for i, qValue in enumerate(qValues):
            direction = ["UP", "DOWN", "LEFT", "RIGHT"][i]
            qValueText = font.render(direction + ": " + str(qValue), True,
                                     "green" if qValue == max(qValues)
                                     else "white")
            qValueRect = qValueText.get_rect()
            qValueRect.topleft = (screenWidth - WIDTH_OFFSET,
                                  screenHeight / 5 * 4 + i * fontSize)
            self.SCREEN.blit(qValueText, qValueRect)

    def run(self):

        while True:

            game = Game(self.training.size)
            state = State(game)
            currentDuration = 0
            lastDirection = "Hasn't moved yet"

            while game.gameOver is False:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    pygame.quit()
                    exit()

                self.SCREEN.fill("black")
                self.draw(game)
                self.drawText(game, currentDuration, lastDirection)
                if self.nerd:
                    self.drawNerdText(game, state)
                lastDirection = self.training.run(game, state, False)
                currentDuration += 1
                pygame.display.flip()

                self.CLOCK.tick(self.speed)

                if self.stepbystep:
                    while True:
                        event = pygame.event.wait()

                        if event.type == pygame.KEYDOWN\
                                and event.key == pygame.K_SPACE:
                            break

                        if (event.type == pygame.KEYDOWN
                                and event.key == pygame.K_ESCAPE)\
                                or event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
