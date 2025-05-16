from .utils import fadeout, mouseClickedOnButton, BACKGROUND, FONT, BUTTON_SIZE, BUTTON
from .Train import Train

import pygame
import os

BUTTONS_COORDS = {
    0: (460, 740, 430, 510), # Start
    1: (460, 740, 555, 635), # Play
    2: (460, 740, 680, 760), # Statistics
    3: (460, 740, 805, 885)  # Quit
}

class Menu:

    def __init__(self, screen, clock):
        self.SCREEN = screen
        self.CLOCK = clock
        pygame.display.set_caption("Learn2Slither - Main")

    # Public

    def run(self):
        # Load font
        titleFont = pygame.font.Font(FONT, 70)
        buttonsFont = pygame.font.Font(FONT, 20)

        # Load buttons
        # button = pygame.image.load(os.path.join(
        #     os.path.dirname(__file__), "statics/button.png"))
        # button = pygame.transform.scale(button, BUTTON_SIZE)

        while True:

            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    fadeout(self.SCREEN)
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    buttonClicked = mouseClickedOnButton(mouse, BUTTONS_COORDS)
                    if buttonClicked == 0:
                        Train(self.SCREEN, self.CLOCK).run()
                    elif buttonClicked == 1:
                        pass
                    elif buttonClicked == 2:
                        pass
                    elif buttonClicked == 3:
                        fadeout(self.SCREEN)
                        pygame.quit()
                        exit()

                if event.type == pygame.KEYDOWN\
                        and event.key == pygame.K_ESCAPE:
                    fadeout(self.SCREEN)
                    pygame.quit()
                    exit()

            # Reset display
            self.SCREEN.fill("black")
            self.SCREEN.blit(BACKGROUND, (0, 0))

            # Title
            title = titleFont.render("Learn2Slither", True, "gold")
            titleRect = title.get_rect()
            titleRect.topleft = (175, 100)
            self.SCREEN.blit(title, titleRect)

            # Buttons
            buttonsText = ["Train AI", "Play", "Statistics", "Quit"]
            for idx, text in enumerate(buttonsText):
                isHovering = BUTTONS_COORDS[idx][0] <= mouse[0] <= BUTTONS_COORDS[idx][1] and\
                             BUTTONS_COORDS[idx][2] <= mouse[1] <= BUTTONS_COORDS[idx][3]
                buttonColor = (200, 200, 255) if isHovering else "#9A845B"

                buttonText = buttonsFont.render(text, True, buttonColor)
                buttonTextRect = buttonText.get_rect()
                buttonTextRect.topleft = (505 + (10 - len(text)) * 10,
                                          462 + 125 * idx)
                self.SCREEN.blit(BUTTON, (450,
                                          400 + 125 * idx))
                self.SCREEN.blit(buttonText, buttonTextRect)

            pygame.display.flip()
            self.CLOCK.tick(10)

