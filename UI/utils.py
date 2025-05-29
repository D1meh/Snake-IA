import pygame
import time
import os

WINDOW_SIZE = 1200, 1000
BUTTON_SIZE = 300, 150

BACKGROUND = pygame.image.load(os.path.join(
             os.path.dirname(__file__), "statics/blue.jpg"))
BACKGROUND = pygame.transform.scale(BACKGROUND, WINDOW_SIZE)

FONT = os.path.join(
            os.path.dirname(__file__), "statics/PressStart2P.ttf")

BUTTON = pygame.image.load(os.path.join(
            os.path.dirname(__file__), "statics/button.png"))
BUTTON = pygame.transform.scale(BUTTON, BUTTON_SIZE)


def fadeout(screen):
    fade = pygame.Surface(WINDOW_SIZE)
    fade.fill((0, 0, 0))
    for i in range(75):
        fade.set_alpha(i)
        screen.blit(fade, (0, 0))
        pygame.display.flip()
        time.sleep(0.007)


def mouseClickedOnButton(mouse, coord):
    x, y = mouse
    for key, value in coord.items():
        if value[0] <= x <= value[1] and value[2] <= y <= value[3]:
            return key

    return None


def grayscale(surface):
    for x in range(surface.get_width()):
        for y in range(surface.get_height()):
            r, g, b, a = surface.get_at((x, y))
            gray = int((r + g + b) / 3)
            surface.set_at((x, y), (gray, gray, gray, a))
    return surface

def getSnakeFacingDirection(snake):
    head = snake[0]
    tail = snake[1]

    if head[0] == tail[0]:
        if head[1] < tail[1]:
            return 'U'
        else:
            return 'D'
    elif head[1] == tail[1]:
        if head[0] < tail[0]:
            return 'L'
        else:
            return 'R'
