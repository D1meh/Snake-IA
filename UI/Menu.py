from .utils import fadeout, mouseClickedOnButton, BACKGROUND, FONT, BUTTON
from .Train import Train
from .Stats import Stats

import pygame

BUTTONS_COORDS = {
    0: (460, 740, 430, 510),  # Start
    1: (460, 740, 555, 635),  # Play
    2: (460, 740, 680, 760),  # Statistics
    3: (460, 740, 805, 885)   # Quit
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
                        Train(self.SCREEN, self.CLOCK).run(settingsForAI=False)
                    elif buttonClicked == 2:
                        Stats.showAllStats(self.SCREEN, self.CLOCK)
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
                x1, x2, y1, y2 = BUTTONS_COORDS[idx]
                isHovering = x1 <= mouse[0] <= x2 and\
                    y1 <= mouse[1] <= y2
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
