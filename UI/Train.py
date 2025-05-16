from .utils import BACKGROUND, FONT, BUTTON_SIZE, mouseClickedOnButton, BUTTON
from Training import Training

from types import SimpleNamespace
import pygame
import os

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

class Train:

    def __init__(self, screen, clock):
        self.SCREEN = screen
        self.CLOCK = clock
        
        self.trainingCount = 0

    def run(self):
        # Init variables
        values = [1000, 10] # Sessions, size
        valuesAreSelected = [False, False] # Same
        boolValues = [False, False, False] # Dontlearn, Stepbystep, Nerd

        # Load font
        titleFont = pygame.font.Font(FONT, 50)
        argsFont = pygame.font.Font(FONT, 20)
        xFont = pygame.font.Font(os.path.join(
            os.path.dirname(__file__), "statics/Flagfies.ttf"), 40)

        while True:

            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    valuesAreSelected = [False, False]

                    buttonClicked = mouseClickedOnButton(mouse, BUTTONS_COORDS)
                    if buttonClicked == 0:
                        pass
                    elif buttonClicked == 1:
                        return
                    
                    inputClicked = mouseClickedOnButton(mouse, INPUT_COORDS)
                    if inputClicked is not None:
                        valuesAreSelected[inputClicked] = True

                    checkboxClicked = mouseClickedOnButton(mouse, CHECKBOXES_COORDS)
                    if checkboxClicked is not None:
                        boolValues[checkboxClicked] = not boolValues[checkboxClicked]

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

                    if any(valuesAreSelected):
                        if event.key == pygame.K_BACKSPACE:
                            values[inputClicked] = int(values[inputClicked] / 10)
                        elif event.key >= pygame.K_KP_1 and event.key <= pygame.K_KP_0 and values[inputClicked] * 10 < 1_000_000_000:
                            values[inputClicked] = values[inputClicked] * 10 + ((event.key - pygame.K_KP_1 + 1) % 10)

            # Reset display
            self.SCREEN.fill("black")
            self.SCREEN.blit(BACKGROUND, (0, 0))

            # Title
            title = titleFont.render("Start new training", True, "gold")
            titleRect = title.get_rect()
            titleRect.topleft = (175, 100)
            self.SCREEN.blit(title, titleRect)

            # Args: sessions and size
            firstTypeOfArgs = ["Sessions", "Grid size"]
            for idx, text in enumerate(firstTypeOfArgs):
                # Arg text
                buttonText = argsFont.render(text, True, "orange")
                buttonTextRect = buttonText.get_rect()
                buttonTextRect.topleft = (WIDTH_OFFSET, STARTING_HEIGHT + 75 * idx)
                self.SCREEN.blit(buttonText, buttonTextRect)

                # Input
                transparentInput = pygame.Surface((210, 50), pygame.SRCALPHA)
                pygame.draw.rect(transparentInput, (100, 100, 100, 150),
                                                   (0, 0, 210, 50))
                self.SCREEN.blit(transparentInput,
                                 (VALUE_WIDTH_OFFSET - 20,
                                  STARTING_HEIGHT - 15 + 75 * idx))
                pygame.draw.rect(self.SCREEN, "black",
                                 (VALUE_WIDTH_OFFSET - 20, STARTING_HEIGHT - 15 + 75 * idx,
                                 210, 50), 1)

                # Value
                valueColor = "orange" if valuesAreSelected[idx] is True else "white"
                valueText = argsFont.render(str(values[idx]), True, valueColor)
                valueTextRect = valueText.get_rect()
                valueTextRect.topleft = (VALUE_WIDTH_OFFSET,
                                         STARTING_HEIGHT + 75 * idx)
                self.SCREEN.blit(valueText, valueTextRect)

            # Args: dontlearn, stepbystep and nerd
            secondTypeOfArgs = ["Don't learn mode", "Step by step mode", "Nerd mode"]
            for idx, text in enumerate(secondTypeOfArgs):
                # Arg text
                buttonText = argsFont.render(text, True, "orange")
                buttonTextRect = buttonText.get_rect()
                buttonTextRect.topleft = (WIDTH_OFFSET,
                                          STARTING_HEIGHT + 150 + 75 * idx)
                self.SCREEN.blit(buttonText, buttonTextRect)
                
                # Check box
                pygame.draw.rect(self.SCREEN, "black",
                                 (VALUE_WIDTH_OFFSET - 20,
                                  STARTING_HEIGHT + 130 + 75 * idx, 50, 50), 3)
                if boolValues[idx] is True:
                    X = titleFont.render("X", True, "black")
                    Xrect = X.get_rect()
                    Xrect.topleft = (VALUE_WIDTH_OFFSET - 17,
                                  STARTING_HEIGHT + 132 + 75 * idx)
                    self.SCREEN.blit(X, Xrect)

            # Start and quit buttons
            buttonsText = ["Start", "Quit"]
            for idx, text in enumerate(buttonsText):
                isHovering = BUTTONS_COORDS[idx][0] <= mouse[0] <= BUTTONS_COORDS[idx][1] and\
                             BUTTONS_COORDS[idx][2] <= mouse[1] <= BUTTONS_COORDS[idx][3]
                buttonColor = (200, 200, 255) if isHovering else "#9A845B"

                buttonText = argsFont.render(text, True, buttonColor)
                buttonTextRect = buttonText.get_rect()
                buttonTextRect.topleft = (300 + 520 * idx,
                                          762)
                self.SCREEN.blit(BUTTON, (200 + 500 * idx,
                                          700))
                self.SCREEN.blit(buttonText, buttonTextRect)

            pygame.display.flip()
            self.CLOCK.tick(10)

    def train(self, values, boolValues):
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

        training = Training(args, False)
        