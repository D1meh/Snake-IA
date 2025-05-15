import pygame

WINDOW_SIZE = 1200, 1000

class Menu:

    def __init__(self):
        self.SCREEN = pygame.display.set_mode(WINDOW_SIZE)
        self.CLOCK = pygame.time.Clock()
        pygame.display.set_caption("Learn2Slither")

    def run(self):
        titleFont = pygame.font.SysFont("Arial", 50)
        buttonsFont = pygame.font.SysFont("Arial", 15)

        while True:

            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pass

                if event.type == pygame.KEYDOWN\
                        and event.key == pygame.K_ESCAPE:
                    pygame.quit()

            self.SCREEN.fill("black")
            title = titleFont.render("Learn2Slither", True, "white")
            titleRect = title.get_rect()
            titleRect.topleft = (450, 100)
            self.SCREEN.blit(title, titleRect)

            pygame.display.flip()
            self.CLOCK.tick(30)

