from Game import Game
from State import State
from .utils import fadeout, BACKGROUND, FONT, BUTTON, GREEN_APPLE, RED_APPLE, \
    mouseClickedOnButton, getSnakeFacingDirection, DRAGON_HEAD, DRAGON_WING, \
    DRAGON_WING_ANGLE, DRAGON_BODY, DRAGON_BODY_ANGLE, DRAGON_TAIL

import pygame

TRANSPARENCY = 150
WIDTH_OFFSET = 300
HEIGHT_OFFSET = 50
HEIGHT_OFFSET_TEXT = 675
OFFSET_FOR_NERD = 30

BUTTONS_COORDS = {
    0: (215, 490, 830, 910),
    1: (715, 990, 830, 910)
}


class Display:
    def __init__(self, screen, clock, size, stepbystep, nerd, training):
        self.size = size
        self.stepbystep = stepbystep
        self.nerd = nerd
        self.training = training

        self.SCREEN = screen
        self.CLOCK = clock
        self.fps = 20

    def initGame(self):
        self.game = Game(self.size)

    def drawDragonHead(self, x, y):
        if self.game.snake.size == 1:
            if self.lastDirection == 'U':
                angle = 0
            elif self.lastDirection == 'D':
                angle = 180
            elif self.lastDirection == 'L':
                angle = 90
            else:  # Right
                angle = 270

        else:
            nextCell = self.game.snake.pos[1]
            if nextCell[0] == x and nextCell[1] == y - 1:  # Down
                angle = 180
            elif nextCell[0] == x and nextCell[1] == y + 1:  # Up
                angle = 0
            elif nextCell[0] == x - 1 and nextCell[1] == y:  # Left
                angle = 270
            else:  # Right
                angle = 90
        return pygame.transform.rotate(
            pygame.transform.scale(DRAGON_HEAD,
                                   [self.CELLSIZE, self.CELLSIZE]), angle)

    def drawDragonBody(self, x, y):
        bodyParts = {
            0: DRAGON_WING,
            1: DRAGON_WING_ANGLE,
            2: DRAGON_BODY,
            3: DRAGON_BODY_ANGLE
        }

        bodyNumber = self.game.snake.pos.index((x, y))
        previousCell = self.game.snake.pos[bodyNumber - 1]
        nextCell = self.game.snake.pos[bodyNumber + 1]\
            if bodyNumber + 1 < self.game.snake.size else None
        bodyPart = 0 if bodyNumber == 1 else 2
        horizontalFlip = False
        verticalFlip = False

        if previousCell[0] == x and previousCell[1] == y - 1:  # Previous is up
            angle = 0
        elif previousCell[0] == x and previousCell[1] == y + 1:  # Down
            angle = 180
        elif previousCell[0] == x - 1 and previousCell[1] == y:  # Left
            angle = 90
        else:  # Right
            angle = 270

        if nextCell is None:
            return pygame.transform.rotate(
                pygame.transform.scale(DRAGON_TAIL,
                                       [self.CELLSIZE, self.CELLSIZE]), angle)

        if nextCell[0] == x and nextCell[1] == y - 1:  # Next is up
            if angle != 180:
                bodyPart += 1 if bodyPart % 2 == 0 else 0
                verticalFlip = True if angle == 90 else False
                angle = 270
        elif nextCell[0] == x and nextCell[1] == y + 1:  # Down
            if angle != 0:
                bodyPart += 1 if bodyPart % 2 == 0 else 0
                horizontalFlip = True if angle == 270 else False
        elif nextCell[0] == x - 1 and nextCell[1] == y:  # Left
            if angle != 270:
                bodyPart += 1 if bodyPart % 2 == 0 else 0
                verticalFlip = True if angle == 180 else False
                angle = 0
        else:  # Right
            if angle != 90:
                bodyPart += 1 if bodyPart % 2 == 0 else 0
                horizontalFlip = True if angle != 180 else False

        if bodyPart % 2 == 0:
            return pygame.transform.rotate(
                pygame.transform.scale(bodyParts[bodyPart],
                                        [self.CELLSIZE, self.CELLSIZE]), angle)
        else:
            return pygame.transform.rotate(
                    pygame.transform.flip(
                        pygame.transform.scale(bodyParts[bodyPart],
                                        [self.CELLSIZE, self.CELLSIZE]),
                    horizontalFlip, verticalFlip),
                angle)

    def drawMap(self):
        self.CELLSIZE = int(500 / self.size)
        redApple = pygame.transform.scale(RED_APPLE, [self.CELLSIZE, self.CELLSIZE])
        greenApple = pygame.transform.scale(GREEN_APPLE, [self.CELLSIZE, self.CELLSIZE])

        for x in range(0, (self.size + 2) * self.CELLSIZE, self.CELLSIZE):
            for y in range(0, (self.size + 2) * self.CELLSIZE, self.CELLSIZE):
                transparentCell = pygame.Surface(
                    (self.CELLSIZE, self.CELLSIZE), pygame.SRCALPHA)

                cell = self.game.board[y // self.CELLSIZE][x // self.CELLSIZE]
                if cell == 'W':
                    values = (0, 0, 0, TRANSPARENCY)
                else:
                    values = (150, 150, 150, TRANSPARENCY)

                pygame.draw.rect(transparentCell, values,
                                 (0, 0, self.CELLSIZE, self.CELLSIZE))
                self.SCREEN.blit(transparentCell,
                                 (x + WIDTH_OFFSET, y + HEIGHT_OFFSET))
                if cell == 'R':
                    self.SCREEN.blit(redApple, (x + WIDTH_OFFSET,
                                                 y + HEIGHT_OFFSET))
                elif cell == 'G':
                    self.SCREEN.blit(greenApple, (x + WIDTH_OFFSET,
                                                   y + HEIGHT_OFFSET))
                elif cell == 'H' and self.game.snake.size > 0:
                    head = self.drawDragonHead(x // self.CELLSIZE, y // self.CELLSIZE)
                    self.SCREEN.blit(head, (x + WIDTH_OFFSET,
                                             y + HEIGHT_OFFSET))
                elif cell == 'S':
                    body = self.drawDragonBody(x // self.CELLSIZE, y // self.CELLSIZE)
                    self.SCREEN.blit(body, (x + WIDTH_OFFSET,
                                             y + HEIGHT_OFFSET))
                pygame.draw.rect(self.SCREEN, (0, 0, 0),
                                 (x + WIDTH_OFFSET, y + HEIGHT_OFFSET,
                                     self.CELLSIZE, self.CELLSIZE), 1)

    def drawText(self, currentDuration):
        text = ["Duration: " + str(currentDuration),
                "Size: " + str(self.game.snake.size)]

        font = pygame.font.Font(FONT, 20)
        for i, line in enumerate(text):
            textSurface = font.render(line, True, (255, 255, 255))
            textRect = textSurface.get_rect()
            textRect.topleft = (WIDTH_OFFSET + self.CELLSIZE + 300 * i,
                                HEIGHT_OFFSET_TEXT)
            self.SCREEN.blit(textSurface, textRect)

    def drawNerdText(self):
        currentState = self.state.getState()
        if currentState in self.training.LEARNING.qTable:
            qValues = self.training.LEARNING.qTable[currentState]
        else:  # Should never happen, putting this just in case
            qValues = [0, 0, 0, 0]

        firstLine = "Coordinates: " + str(self.game.snake.getHead())
        secondLine = ("Danger: ", str(currentState[0]))
        thirdLine = ("Red Apple: ", str(currentState[1]))
        fourthLine = ("Green Apple: ", str(currentState[2]))
        content = [firstLine, secondLine, thirdLine, fourthLine]

        font = pygame.font.Font(FONT, 20)
        smallFont = pygame.font.Font(FONT, 10)
        for i, line in enumerate(content):
            if i == 0:
                textSurface = font.render(line, True, "white")
                textRect = textSurface.get_rect()
                textRect.topleft = (WIDTH_OFFSET + self.CELLSIZE,
                                    HEIGHT_OFFSET_TEXT + OFFSET_FOR_NERD)
                self.SCREEN.blit(textSurface, textRect)
            else:
                firstPart = font.render(line[0], True, "white")
                secondPart = font.render(line[1], True, "white")

                firstPartRect = firstPart.get_rect()
                firstPartRect.topleft = (
                    WIDTH_OFFSET + self.CELLSIZE,
                    HEIGHT_OFFSET_TEXT + OFFSET_FOR_NERD * (i + 1)
                )

                secondPartRect = secondPart.get_rect()
                secondPartRect.topleft = (
                    WIDTH_OFFSET + self.CELLSIZE + 250,
                    HEIGHT_OFFSET_TEXT + OFFSET_FOR_NERD * (i+1)
                )

                self.SCREEN.blit(firstPart, firstPartRect)
                self.SCREEN.blit(secondPart, secondPartRect)

        for i, qValue in enumerate(qValues):
            direction = ["UP", "DOWN", "LEFT", "RIGHT"][i]
            qValueText = smallFont.render(
                direction + ": " + str(qValue)[:19], True,
                "green" if qValue == max(qValues)
                else "white")
            qValueRect = qValueText.get_rect()
            qValueRect.topleft = (50 if i < 2 else 950,
                                  300 if i % 2 == 0 else 350)
            self.SCREEN.blit(qValueText, qValueRect)

    def drawButtons(self):
        buttonsText = ["Run again", "Quit"]
        font = pygame.font.Font(FONT, 20)
        mouse = pygame.mouse.get_pos()

        for idx, text in enumerate(buttonsText):
            x1, x2, y1, y2 = BUTTONS_COORDS[idx]
            isHovering = x1 <= mouse[0] <= x2 and\
                y1 <= mouse[1] <= y2
            buttonColor = (200, 200, 255) if isHovering else "#9A845B"

            buttonText = font.render(text, True, buttonColor)
            buttonTextRect = buttonText.get_rect()
            buttonTextRect.topleft = (
                300 + (4 - len(text)) * 7 + 520 * idx, 862
            )
            self.SCREEN.blit(BUTTON, (200 + 500 * idx, 800))
            self.SCREEN.blit(buttonText, buttonTextRect)

    def drawSpeedButton(self):
        font = pygame.font.Font(FONT, 20)

        buttonText = font.render("-         +", True, "#9A845B")
        buttonTextRect = buttonText.get_rect()
        buttonTextRect.topleft = (495, 862)

        speedText = font.render("Speed " + str(self.fps), True, "#9A845B")
        speedTextRect = speedText.get_rect()
        speedTextRect.topleft = (525, 862)

        self.SCREEN.blit(BUTTON, (450, 800))
        self.SCREEN.blit(buttonText, buttonTextRect)
        self.SCREEN.blit(speedText, speedTextRect)

    # Public

    def displayAI(self):
        minusSpeed = (490, 510, 850, 880)
        plusSpeed = (695, 715, 850, 880)

        while True:
            self.initGame()
            self.state = State(self.game)
            currentDuration = 0

            while self.game.gameOver is False:
                mouse = pygame.mouse.get_pos()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        fadeout(self.SCREEN)
                        pygame.quit()
                        exit()

                    if event.type == pygame.MOUSEBUTTONDOWN\
                            and not self.stepbystep:

                        if minusSpeed[0] <= mouse[0] <= minusSpeed[1] and\
                                minusSpeed[2] <= mouse[1] <= minusSpeed[3] and\
                                self.fps > 2:
                            self.fps -= 2

                        if plusSpeed[0] <= mouse[0] <= plusSpeed[1] and\
                                plusSpeed[2] <= mouse[1] <= plusSpeed[3] and\
                                self.fps < 100:
                            self.fps += 2

                self.SCREEN.fill((0, 0, 0))
                self.SCREEN.blit(BACKGROUND, (0, 0))
                self.drawMap()
                self.drawText(currentDuration)

                if self.nerd:
                    self.drawNerdText()
                if not self.stepbystep:
                    self.drawSpeedButton()

                self.lastDirection = self.training.run(self.game, self.state, False)
                currentDuration += 1

                pygame.display.flip()
                self.CLOCK.tick(self.fps)

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

            # Game over
            while True:
                self.SCREEN.fill((0, 0, 0))
                self.SCREEN.blit(BACKGROUND, (0, 0))
                self.drawMap()
                self.drawText(currentDuration)
                if self.nerd:
                    self.drawNerdText()
                self.drawButtons()

                mouse = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        fadeout(self.SCREEN)
                        pygame.quit()
                        exit()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        buttonClicked = mouseClickedOnButton(mouse,
                                                             BUTTONS_COORDS)
                        if buttonClicked == 0:
                            return self.displayAI()
                        elif buttonClicked == 1:
                            return

                pygame.display.flip()
                self.CLOCK.tick(10)

    def displayForPlayer(self):
        while True:
            self.initGame()
            direction = getSnakeFacingDirection(self.game.snake.pos)
            dontUpdateForXFrames = 20
            framesSinceLastUpdate = 0
            currentDuration = 0

            while self.game.gameOver is False:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        fadeout(self.SCREEN)
                        pygame.quit()
                        exit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            direction = 'U'
                        elif event.key == pygame.K_DOWN:
                            direction = 'D'
                        elif event.key == pygame.K_LEFT:
                            direction = 'L'
                        elif event.key == pygame.K_RIGHT:
                            direction = 'R'

                self.SCREEN.fill((0, 0, 0))
                self.SCREEN.blit(BACKGROUND, (0, 0))
                self.drawMap()
                self.drawText(currentDuration)

                if framesSinceLastUpdate == dontUpdateForXFrames:
                    framesSinceLastUpdate = 0
                    lastCell = self.game.update(direction)
                    if lastCell == 'G':
                        dontUpdateForXFrames -= 1 if dontUpdateForXFrames > 1\
                            else 0
                    currentDuration += 1
                    self.lastDirection = direction

                pygame.display.flip()
                self.CLOCK.tick(30)
                framesSinceLastUpdate += 1

            # Game over
            while True:
                self.SCREEN.fill((0, 0, 0))
                self.SCREEN.blit(BACKGROUND, (0, 0))
                self.drawMap()
                self.drawText(currentDuration)
                self.drawButtons()

                mouse = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        fadeout(self.SCREEN)
                        pygame.quit()
                        exit()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        buttonClicked = mouseClickedOnButton(mouse,
                                                             BUTTONS_COORDS)
                        if buttonClicked == 0:
                            return self.displayForPlayer()
                        elif buttonClicked == 1:
                            return

                pygame.display.flip()
                self.CLOCK.tick(10)
