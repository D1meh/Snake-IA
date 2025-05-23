from .utils import BACKGROUND, FONT, mouseClickedOnButton, \
                    BUTTON, fadeout, grayscale
from .Display import Display
from Training import Training

from types import SimpleNamespace
import threading
import pygame

WIDTH_OFFSET = 300
STARTING_HEIGHT = 300
VALUE_WIDTH_OFFSET = 700

BUTTONS_COORDS = {
    0: (215, 490, 730, 810),
    1: (715, 990, 730, 810)
}

INPUT_COORDS = {
    0: (680, 880, 285, 335),
    1: (680, 880, 360, 410)
}

CHECKBOXES_COORDS = {
    0: (680, 730, 430, 480),
    1: (680, 730, 505, 555),
    2: (680, 730, 580, 630)
}

START_BUTTON_COORDS = {
    0: (465, 740, 730, 810)
}


class Train:

    def __init__(self, screen, clock):
        self.SCREEN = screen
        self.CLOCK = clock

    # Public

    def run(self):
        # Init variables
        values = [1000, 10]  # Sessions, size
        valuesAreSelected = [False, False]  # Same
        boolValues = [False, False, False]  # Dontlearn, Stepbystep, Nerd

        # Load font
        self.titleFont = pygame.font.Font(FONT, 50)
        self.argsFont = pygame.font.Font(FONT, 20)

        while True:

            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    fadeout(self.SCREEN)
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    valuesAreSelected = [False, False]

                    buttonClicked = mouseClickedOnButton(mouse, BUTTONS_COORDS)
                    if buttonClicked == 0:
                        self.__train(values, boolValues)
                    elif buttonClicked == 1:
                        return

                    inputClicked = mouseClickedOnButton(mouse, INPUT_COORDS)
                    if inputClicked is not None:
                        valuesAreSelected[inputClicked] = True

                    checkboxClicked = mouseClickedOnButton(mouse,
                                                           CHECKBOXES_COORDS)
                    if checkboxClicked is not None:
                        boolValues[checkboxClicked] = \
                            not boolValues[checkboxClicked]

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

                    if any(valuesAreSelected):
                        if event.key == pygame.K_BACKSPACE:
                            values[inputClicked] = int(
                                values[inputClicked] / 10)

                        elif event.key >= pygame.K_KP_1\
                                and event.key <= pygame.K_KP_0:

                            if (inputClicked == 0
                                and values[0] * 10 < 1_000_000_000) \
                                or (inputClicked == 1
                                    and values[1] * 10 <= 100):

                                values[inputClicked] = \
                                    values[inputClicked] * 10 + (
                                        (event.key - pygame.K_KP_1 + 1) % 10
                                        )

                                if inputClicked == 1\
                                        and values[inputClicked] > 100:
                                    values[1] = 100

            # Reset display
            self.SCREEN.fill("black")
            self.SCREEN.blit(BACKGROUND, (0, 0))

            # Title
            title = self.titleFont.render("Start new training", True, "gold")
            titleRect = title.get_rect()
            titleRect.topleft = (175, 100)
            self.SCREEN.blit(title, titleRect)

            # Args: sessions and size
            firstTypeOfArgs = ["Sessions", "Grid size"]
            for idx, text in enumerate(firstTypeOfArgs):
                # Arg text
                buttonText = self.argsFont.render(text, True, "orange")
                buttonTextRect = buttonText.get_rect()
                buttonTextRect.topleft = (WIDTH_OFFSET,
                                          STARTING_HEIGHT + 75 * idx)
                self.SCREEN.blit(buttonText, buttonTextRect)

                # Input
                transparentInput = pygame.Surface((210, 50), pygame.SRCALPHA)
                pygame.draw.rect(transparentInput, (100, 100, 100, 150),
                                                   (0, 0, 210, 50))
                self.SCREEN.blit(transparentInput,
                                 (VALUE_WIDTH_OFFSET - 20,
                                  STARTING_HEIGHT - 15 + 75 * idx))
                pygame.draw.rect(self.SCREEN, "black",
                                 (VALUE_WIDTH_OFFSET - 20,
                                  STARTING_HEIGHT - 15 + 75 * idx,
                                  210, 50), 1)

                # Value
                valueColor = "orange" if valuesAreSelected[idx] is True\
                    else "white"
                valueText = self.argsFont.render(str(values[idx]),
                                                 True, valueColor)
                valueTextRect = valueText.get_rect()
                valueTextRect.topleft = (VALUE_WIDTH_OFFSET,
                                         STARTING_HEIGHT + 75 * idx)
                self.SCREEN.blit(valueText, valueTextRect)

            # Args: dontlearn, stepbystep and nerd
            secondTypeOfArgs = ["Don't learn mode",
                                "Step by step mode",
                                "Nerd mode"]

            for idx, text in enumerate(secondTypeOfArgs):
                # Arg text
                buttonText = self.argsFont.render(text, True, "orange")
                buttonTextRect = buttonText.get_rect()
                buttonTextRect.topleft = (WIDTH_OFFSET,
                                          STARTING_HEIGHT + 150 + 75 * idx)
                self.SCREEN.blit(buttonText, buttonTextRect)

                # Check box
                pygame.draw.rect(self.SCREEN, "black",
                                 (VALUE_WIDTH_OFFSET - 20,
                                  STARTING_HEIGHT + 130 + 75 * idx, 50, 50), 3)
                if boolValues[idx] is True:
                    X = self.titleFont.render("X", True, "black")
                    Xrect = X.get_rect()
                    Xrect.topleft = (VALUE_WIDTH_OFFSET - 17,
                                     STARTING_HEIGHT + 132 + 75 * idx)
                    self.SCREEN.blit(X, Xrect)

            # Start and quit buttons
            buttonsText = ["Start", "Quit"]
            for idx, text in enumerate(buttonsText):
                x1, x2, y1, y2 = BUTTONS_COORDS[idx]
                isHovering = x1 <= mouse[0] <= x2 and\
                    y1 <= mouse[1] <= y2
                buttonColor = (200, 200, 255) if isHovering else "#9A845B"

                buttonText = self.argsFont.render(text, True, buttonColor)
                buttonTextRect = buttonText.get_rect()
                buttonTextRect.topleft = (300 + 520 * idx,
                                          762)
                self.SCREEN.blit(BUTTON, (200 + 500 * idx,
                                          700))
                self.SCREEN.blit(buttonText, buttonTextRect)

            pygame.display.flip()
            self.CLOCK.tick(10)

    # Private

    def __drawLoadingBar(self, totalSessions):
        percent = int(self.trainingCount / totalSessions * 100)

        # Reset display
        self.SCREEN.fill("black")
        self.SCREEN.blit(BACKGROUND, (0, 0))

        # Title
        title = self.titleFont.render(
            "Training in progress" if not self.doneTraining
            else "Training completed!", True, "gold")
        titleRect = title.get_rect()
        titleRect.topleft = (130, 100)
        self.SCREEN.blit(title, titleRect)

        # Loading bar
        pygame.draw.rect(self.SCREEN, "gold", (400, 300, 400, 50), 1)
        pygame.draw.rect(self.SCREEN, "gold", (400, 300, 4 * percent, 50))

        # Progress
        percentProgress = self.argsFont.render(
            f"{int(percent)}% ({self.trainingCount}/{totalSessions})",
            True, "orange")
        percentProgressRect = percentProgress.get_rect()
        percentProgressRect.topleft = (450, 400)
        self.SCREEN.blit(percentProgress, percentProgressRect)

        # Start button
        coord = (465, 740, 730, 810)
        mouse = pygame.mouse.get_pos()
        x1, x2, y1, y2 = coord
        isHovering = x1 <= mouse[0] <= x2 and\
            y1 <= mouse[1] <= y2 and self.doneTraining
        button = grayscale(BUTTON.copy())

        buttonColor = (200, 200, 255) if isHovering else "#9A845B"
        buttonText = self.argsFont.render("Start", True, buttonColor)
        buttonTextRect = buttonText.get_rect()
        buttonTextRect.topleft = (550, 862)
        self.SCREEN.blit(BUTTON if self.doneTraining else button, (450, 800))
        self.SCREEN.blit(buttonText, buttonTextRect)

        pygame.display.flip()
        self.CLOCK.tick(30)

    def __showStats(self):
        firstTenth = int(len(self.sizes) / 10)
        
        maxDuration = max(self.durations)
        maxSize = max(self.sizes)
        averageSize = sum(self.sizes) / len(self.sizes)
        averageSizeOnBeginning = sum(self.sizes[:firstTenth]) / firstTenth

        values = {
            "Max duration:": maxDuration,
            "Max size:": maxSize,
            "Average size": averageSize,
            "Average size on first 10%": averageSizeOnBeginning
        }

        idx = 0
        for valueName, value in values.values():
            text = self.argsFont.render(valueName, True, "white")
            valueText = self.argsFont.render(str(value), True, "orange")

            textRect = text.get_rect()
            textRect.topleft = (400 if idx < 2 else 800,
                                600 if idx % 2 == 0 else 650)

            valueTextRect = valueText.get_rect()
            valueTextRect.topleft = (450 if idx < 2 else 850,
                                     600 if idx % 2 == 0 else 650)
            
            self.SCREEN.blit(text, textRect)
            self.SCREEN.blit(valueText, valueTextRect)


    def __train(self, values, boolValues):
        self.trainingCount = 0

        def updateProgress(sessions):
            self.trainingCount = sessions

        def initTrain():

            args = SimpleNamespace()
            args.sessions = values[0]
            args.size = values[1]
            args.save = None
            args.choosetosave = False
            args.load = None
            args.dontlearn = boolValues[0]
            args.visual = False
            args.speed = 10
            args.plot = False # maybe implement it?
            args.ui = True
            args.stepbystep = boolValues[1]
            args.nerd = boolValues[2]

            self.training = Training(args, False)
            self.training.resetQTable()
            self.sizes, self.durations = self.training.train(
                showLogs=False, progress=updateProgress)
            self.doneTraining = True

        self.doneTraining = False
        t = threading.Thread(target=initTrain)
        t.start()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    fadeout(self.SCREEN)
                    pygame.quit()
                    exit()

            self.__drawLoadingBar(values[0])
            if self.doneTraining:
                t.join()
                break

        while True:
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or\
                    (event.type == pygame.KEYDOWN and
                     event.key == pygame.K_ESCAPE):
                    fadeout(self.SCREEN)
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    buttonClicked = mouseClickedOnButton(mouse,
                                                         START_BUTTON_COORDS)
                    if buttonClicked == 0:
                        return Display(self.SCREEN, self.CLOCK,
                                       values[1], boolValues[1],
                                       boolValues[2], self.training
                                       ).displayAI()

            self.__showStats()
            self.__drawLoadingBar(values[0])
