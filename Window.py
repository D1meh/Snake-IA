from Training import Training
from Game import Game
from State import State

# Remove pygame's welcome message
import os
import pygame

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
pygame.init()

WIDTH_OFFSET = 200


class Window:
    def __init__(self, training: Training):

        self.training = training
        self.stepbystep = training.stepbystep
        self.nerd = training.nerd

        self.FPS = 10
        SIZE = (training.size + 11) * 50, \
               (training.size + 2) * 50

        self.SCREEN = pygame.display.set_mode(SIZE)
        self.CLOCK = pygame.time.Clock()
        pygame.display.set_caption("Learn2Slither")

    def draw(self, game: Game):
        for x in range(0, (self.training.size + 2) * 50, 50):
            for y in range(0, (self.training.size + 2) * 50, 50):

                cell = game.board[y // 50][x // 50]
                if cell == '0':  # Empty
                    pygame.draw.rect(self.SCREEN, "grey",
                                     (x + WIDTH_OFFSET, y, 50, 50))
                elif cell == 'H':  # Head
                    pygame.draw.rect(self.SCREEN, "yellow",
                                     (x + WIDTH_OFFSET, y, 50, 50))
                elif cell == 'S':  # Body segment
                    pygame.draw.rect(self.SCREEN, "blue",
                                     (x + WIDTH_OFFSET, y, 50, 50))
                elif cell == 'R':  # Red apple
                    pygame.draw.rect(self.SCREEN, "red",
                                     (x + WIDTH_OFFSET, y, 50, 50))
                elif cell == 'G':  # Green apple
                    pygame.draw.rect(self.SCREEN, "green",
                                     (x + WIDTH_OFFSET, y, 50, 50))
                else:  # Wall
                    pygame.draw.rect(self.SCREEN, "black",
                                     (x + WIDTH_OFFSET, y, 50, 50))

                pygame.draw.rect(self.SCREEN, "black",
                                 (x + WIDTH_OFFSET, y, 50, 50), 1)

    def drawText(self, game, duration, lastDirection):
        firstLine = "Score: " + str(game.snake.size)
        secondLine = "Duration: " + str(duration)
        thirdLine = "Last Direction:"
        fourthLine = lastDirection
        content = [firstLine, secondLine, thirdLine, fourthLine]

        screenHeight = self.SCREEN.get_height() - 250
        font = pygame.font.SysFont("Arial", 35)

        for i, line in enumerate(content):
            textSurface = font.render(line, True, "white")
            textRect = textSurface.get_rect()
            if i != 3:
                textRect.topleft = (40, screenHeight / 2 * i + 100)
            else:
                textRect.topleft = (40, screenHeight / 2 * (i-1) + 130)
            self.SCREEN.blit(textSurface, textRect)

    def drawNerdText(self, game, state):
        currentState = state.getState()
        if currentState in self.training.LEARNING.qTable:
            qValues = self.training.LEARNING.qTable[currentState]
        else:
            qValues = [0, 0, 0, 0]

        firstLine = "Coordinates: " + str(game.snake.getHead())
        secondLine = ("Danger: ", str(currentState[0]))
        thirdLine = ("Red Apple: ", str(currentState[1]))
        fourthLine = ("Green Apple: ", str(currentState[2]))
        content = [firstLine, secondLine, thirdLine, fourthLine]

        screenHeight = self.SCREEN.get_height() - 100
        screenWidth = self.SCREEN.get_width()
        font = pygame.font.SysFont("Arial", 30)

        for i, line in enumerate(content):
            if i == 0:
                textSurface = font.render(line, True, "white")
                textRect = textSurface.get_rect()
                textRect.topleft = (screenWidth - 250, 50)
                self.SCREEN.blit(textSurface, textRect)
            else:
                splitState = line[1].split(',')

                firstPart = font.render(line[0], True, "white")
                secondPart = font.render(str(splitState[:2]), True, "white")
                thirdPart = font.render(str(splitState[2:]), True, "white")

                firstPartRect = firstPart.get_rect()
                secondPartRect = secondPart.get_rect()
                thirdPartRect = thirdPart.get_rect()

                firstPartRect.topleft = (screenWidth - 250,
                                         screenHeight / 5 * i)
                secondPartRect.topleft = (screenWidth - 250,
                                          screenHeight / 5 * i + 30)
                thirdPartRect.topleft = (screenWidth - 250,
                                         screenHeight / 5 * i + 60)

                self.SCREEN.blit(firstPart, firstPartRect)
                self.SCREEN.blit(secondPart, secondPartRect)
                self.SCREEN.blit(thirdPart, thirdPartRect)

        for i, qValue in enumerate(qValues):
            direction = ["UP", "DOWN", "LEFT", "RIGHT"][i]
            qValueText = font.render(direction + ": " + str(qValue), True,
                                     "green" if qValue == max(qValues)
                                     else "white")
            qValueRect = qValueText.get_rect()
            qValueRect.topleft = (screenWidth - 250,
                                  screenHeight - 100 + i * 30)
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
                lastDirection = self.training.run(game, state)
                currentDuration += 1
                pygame.display.flip()

                self.CLOCK.tick(self.FPS)

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
