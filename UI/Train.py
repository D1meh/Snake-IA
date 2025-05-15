from .utils import BACKGROUND, FONT, BUTTON_SIZE

import pygame
import os

WIDTH_OFFSET = 300
STARTING_HEIGHT = 300
VALUE_WIDTH_OFFSET = 700

class Train:

    def __init__(self, screen, clock):
        self.SCREEN = screen
        self.CLOCK = clock

    def run(self):
        # Init variables
        size = 10
        sessions = 1000
        sizeIsSelected = sessionsIsSelected = False
        dontlearn = stepbystep = nerd = False

        # Load font
        titleFont = pygame.font.Font(FONT, 50)
        argsFont = pygame.font.Font(FONT, 20)

        # Load buttons and inputs
        button = pygame.image.load(os.path.join(
            os.path.dirname(__file__), "statics/button.png"))
        button = pygame.transform.scale(button, BUTTON_SIZE)

        while True:

            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # TODO: everything lol
                    pass

                if event.type == pygame.KEYDOWN\
                        and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

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
                buttonText = argsFont.render(text, True, "orange")
                buttonTextRect = buttonText.get_rect()
                buttonTextRect.topleft = (WIDTH_OFFSET, STARTING_HEIGHT + 75 * idx)
                self.SCREEN.blit(buttonText, buttonTextRect)
                # TODO: rectangle for the input
                
                if idx == 0:
                    valueText = argsFont.render(str(sessions), True, "white")
                else:
                    valueText = argsFont.render(str(size), True, "white")
                valueTextRect = valueText.get_rect()
                valueTextRect.topleft = (VALUE_WIDTH_OFFSET,
                                         STARTING_HEIGHT + 75 * idx)
                self.SCREEN.blit(valueText, valueTextRect)

            # Args: dontlearn, stepbystep and nerd
            secondTypeOfArgs = ["Don't learn mode", "Step by step mode", "Nerd mode"]
            for idx, text in enumerate(secondTypeOfArgs):
                buttonText = argsFont.render(text, True, "orange")
                buttonTextRect = buttonText.get_rect()
                buttonTextRect.topleft = (WIDTH_OFFSET,
                                          STARTING_HEIGHT + 150 + 75 * idx)
                self.SCREEN.blit(buttonText, buttonTextRect)
                # TODO: checkcell

            # Start and quit buttons
            buttonsText = ["Start", "Quit"]
            for idx, text in enumerate(buttonsText):
                buttonText = argsFont.render(text, True, "purple")
                buttonTextRect = buttonText.get_rect()
                buttonTextRect.topleft = (300 + 520 * idx,
                                          762)
                self.SCREEN.blit(button, (200 + 500 * idx,
                                          700))
                self.SCREEN.blit(buttonText, buttonTextRect)

            pygame.display.flip()
            self.CLOCK.tick(10)