import pygame
import os

WINDOW_SIZE = 1200, 1000
BUTTON_SIZE = 300, 150

class Menu:

    def __init__(self):
        self.SCREEN = pygame.display.set_mode(WINDOW_SIZE)
        self.CLOCK = pygame.time.Clock()
        pygame.display.set_caption("Learn2Slither")

    def run(self):
        titleFont = pygame.font.Font(os.path.join(
            os.path.dirname(__file__), "statics/PerfectoCalligraphy.ttf"), 70)
        buttonsFont = pygame.font.Font(os.path.join(
            os.path.dirname(__file__), "statics/PressStart2P.ttf"), 20)

        background = pygame.image.load(os.path.join(
            os.path.dirname(__file__), "statics/purple.jpg"))
        background = pygame.transform.scale(background, WINDOW_SIZE)

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
                    pass

                if event.type == pygame.KEYDOWN\
                        and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

            # Reset display
            self.SCREEN.fill("black")
            self.SCREEN.blit(background, (0, 0))

            # Title
            title = titleFont.render("Learn2Slither", True, "gold")
            titleRect = title.get_rect()
            titleRect.topleft = (425, 100)
            self.SCREEN.blit(title, titleRect)

            # Buttons
            buttonsText = ["Start", "Statistics","Quit"]
            for idx, text in enumerate(buttonsText):
                buttonText = buttonsFont.render(text, True, "purple")
                buttonTextRect = buttonText.get_rect()
                buttonTextRect.topleft = (505 + (10 - len(text)) * 10,
                                          462 + 150 * idx)
                self.SCREEN.blit(button, (450,
                                          400 + 150 * idx))
                self.SCREEN.blit(buttonText, buttonTextRect)

            pygame.display.flip()
            self.CLOCK.tick(30)

