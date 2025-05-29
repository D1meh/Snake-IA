import os
import json
import pygame

from .utils import FONT, BACKGROUND, mouseClickedOnButton, fadeout, BUTTON

STATS_FILE = os.path.join(
             os.path.dirname(__file__), "statics/stats.json")

TEMPLATE = {
    "size": 0,
    "trainingSessions": 0,
    "data": {
        "ran#Times": 0,

        "maxSize": 0,
        "averageSize": 0,
        "maxAverageSize": 0,
        "averageSizeOnFirstHalf": 0,
        "averageSizeOnSecondHalf": 0,
        "averageSizeOnLastTenth": 0,

        "maxDuration": 0,
        "averageDuration": 0,
        "maxAverageDuration": 0,
        "averageDurationOnFirstHalf": 0,
        "averageDurationOnSecondHalf": 0,
        "averageDurationOnLastTenth": 0
    }
}

# ShowAllStats

STATS_COORDS = {
    0: (195, 780, 380, 420),
    1: (195, 780, 480, 520),
    2: (195, 780, 580, 620)
}

BUTTONS_COORDS = {
    0: (50, 340, 750, 855),  # Previous
    1: (450, 740, 750, 855),  # Next
    2: (850, 1140, 750, 855)   # Back
}

WIDTH_OFFSET = 200

# ShowStat

BACK_COORDS = {
    0: (450, 740, 750, 855),  # Back
}


class Stats:
    def __init__(self):
        pass

    @staticmethod
    def updateStats(sizes, durations, gridSize, sessions):
        # Load existing stats or use template
        stats = None
        with open(STATS_FILE, "r") as f:
            content = json.load(f)
            for item in content:
                if item["size"] == gridSize \
                        and item["trainingSessions"] == sessions:
                    stats = item
                    break
            if stats is None:
                stats = TEMPLATE.copy()
                stats["size"] = gridSize
                stats["trainingSessions"] = sessions

        # Update stats
        data = stats["data"]
        coefficient = stats["trainingSessions"] * data["ran#Times"]
        half = max(len(sizes) // 2, 1)
        lastTenth = max(len(sizes) // 10, 1)

        data["ran#Times"] += 1
        data["maxSize"] = max(data["maxSize"], max(sizes))
        data["averageSize"] = (data["averageSize"] * coefficient + sum(sizes))\
            / (coefficient + len(sizes))
        data["maxAverageSize"] = (data["maxAverageSize"] *
                                  (data["ran#Times"] - 1) + max(sizes))\
            / data["ran#Times"]
        data["averageSizeOnFirstHalf"] = (data["averageSizeOnFirstHalf"]
                                          * coefficient + sum(sizes[:half]))\
            / (coefficient + half)
        data["averageSizeOnSecondHalf"] = (data["averageSizeOnSecondHalf"]
                                           * coefficient + sum(sizes[half:]))\
            / (coefficient + half)
        data["averageSizeOnLastTenth"] = (data["averageSizeOnLastTenth"]
                                          * coefficient
                                          + sum(sizes[-lastTenth:]))\
            / (coefficient + lastTenth)

        data["maxDuration"] = max(data["maxDuration"], max(durations))
        data["averageDuration"] = (data["averageDuration"]
                                   * coefficient + sum(durations))\
            / (coefficient + len(durations))
        data["maxAverageDuration"] = (data["maxAverageDuration"] *
                                      (data["ran#Times"] - 1) + max(durations)
                                      ) / data["ran#Times"]
        data["averageDurationOnFirstHalf"] = \
            (data["averageDurationOnFirstHalf"] * coefficient
             + sum(durations[:half])) / (coefficient + half)
        data["averageDurationOnSecondHalf"] = \
            (data["averageDurationOnSecondHalf"] * coefficient +
             sum(durations[half:])) / (coefficient + half)
        data["averageDurationOnLastTenth"] = \
            (data["averageDurationOnLastTenth"] * coefficient +
             sum(durations[-lastTenth:])) / (coefficient + lastTenth)

        # Save updated stats
        for i, item in enumerate(content):
            if item["size"] == gridSize\
                    and item["trainingSessions"] == sessions:
                content[i] = stats
                break
        else:
            content.append(stats)

        with open(STATS_FILE, "w") as f:
            json.dump(content, f, indent=4)

    @staticmethod
    def showStat(screen, clock, stats):
        # Load font
        titleFont = pygame.font.Font(FONT, 70)
        buttonsFont = pygame.font.Font(FONT, 20)

        while True:
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    fadeout(screen)
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if mouseClickedOnButton(mouse, BACK_COORDS) == 0:
                        return

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

            # Reset display
            screen.fill("black")
            screen.blit(BACKGROUND, (0, 0))

            # Title
            title = titleFont.render("Statistics", True, "gold")
            titleRect = title.get_rect()
            titleRect.topleft = (275, 100)
            screen.blit(title, titleRect)

            # Display stats
            texts = {
                "Grid Size:": stats['size'],
                "Training Sessions:": stats['trainingSessions'],
                "Ran # Times:": stats['data']['ran#Times'],
                "": "",  # Skip line
                "Max Size:": stats['data']['maxSize'],
                "Average Size:": f"{stats['data']['averageSize']:.2f}",
                "Average Max Size:": f"{stats['data']['maxAverageSize']:.2f}",
                "Average Size on First Half:":\
                    f"{stats['data']['averageSizeOnFirstHalf']:.2f}",
                "Average Size on Second Half:":\
                    f"{stats['data']['averageSizeOnSecondHalf']:.2f}",
                "Average Size on Last Tenth:":\
                    f"{stats['data']['averageSizeOnLastTenth']:.2f}",
                " ": "",  # Skip line
                "Max Duration:": stats['data']['maxDuration'],
                "Average Duration:": f"{stats['data']['averageDuration']:.2f}",
                "Average Max Duration:":\
                    f"{stats['data']['maxAverageDuration']:.2f}",
                "Average Duration on First Half:":\
                    f"{stats['data']['averageDurationOnFirstHalf']:.2f}",
                "Average Duration on Second Half:":\
                    f"{stats['data']['averageDurationOnSecondHalf']:.2f}",
                "Average Duration on Last Tenth:":\
                    f"{stats['data']['averageDurationOnLastTenth']:.2f}"
            }

            idx = 0
            for key, value in texts.items():

                keyText = buttonsFont.render(key, True, "white")
                keyTextRect = keyText.get_rect()
                keyTextRect.topleft = (WIDTH_OFFSET, 250 + idx * 30)
                screen.blit(keyText, keyTextRect)

                valueText = buttonsFont.render(str(value), True, "orange")
                valueTextRect = valueText.get_rect()
                valueTextRect.topleft = (WIDTH_OFFSET + len(key) * 20,
                                         250 + idx * 30)
                screen.blit(valueText, valueTextRect)

                idx += 1

            # Back button
            x1, x2, y1, y2 = BACK_COORDS[0]
            isHovering = x1 <= mouse[0] <= x2 and y1 <= mouse[1] <= y2
            buttonColor = (200, 200, 255) if isHovering else "#9A845B"
            buttonText = buttonsFont.render("Back", True, buttonColor)
            buttonTextRect = buttonText.get_rect()
            buttonTextRect.topleft = (560, 812)
            screen.blit(BUTTON, (450, 750))
            screen.blit(buttonText, buttonTextRect)

            pygame.display.flip()
            clock.tick(10)

    @staticmethod
    def showAllStats(screen, clock):

        indexToStart = 0

        # Load font
        titleFont = pygame.font.Font(FONT, 70)
        buttonsFont = pygame.font.Font(FONT, 20)

        # Load stats
        with open(STATS_FILE, "r") as f:
            content = json.load(f)

        while True:

            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    fadeout(screen)
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    statToDisplay = mouseClickedOnButton(mouse, STATS_COORDS)
                    buttonClicked = mouseClickedOnButton(mouse, BUTTONS_COORDS)
                    if statToDisplay is not None:
                        Stats.showStat(screen, clock,
                                       content[indexToStart + statToDisplay])
                    elif buttonClicked == 0:  # Previous
                        if indexToStart > 0:
                            indexToStart -= 1
                    elif buttonClicked == 1:  # Back
                        return
                    elif buttonClicked == 2:  # Next
                        if indexToStart + 3 < len(content):
                            indexToStart += 1

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

            # Reset display
            screen.fill("black")
            screen.blit(BACKGROUND, (0, 0))

            # Title
            title = titleFont.render("Statistics", True, "gold")
            titleRect = title.get_rect()
            titleRect.topleft = (275, 100)
            screen.blit(title, titleRect)

            # Display stats
            for idx in range(3):
                indexToShow = indexToStart + idx
                if indexToShow >= len(content):
                    break

                stat = content[indexToShow]
                text = f"Grid Size: {stat['size']}, "
                text += f"Sessions: {stat['trainingSessions']}"

                x1, x2, y1, y2 = STATS_COORDS[idx]
                isHovering = x1 <= mouse[0] <= x2 and y1 <= mouse[1] <= y2
                buttonColor = "orange" if isHovering else "white"

                buttonText = buttonsFont.render(text, True, buttonColor)
                buttonTextRect = buttonText.get_rect()
                buttonTextRect.topleft = (WIDTH_OFFSET, 400 + idx * 100)
                screen.blit(buttonText, buttonTextRect)

            # Buttons
            buttonsText = ["Previous", "Back", "Next"]
            for idx, text in enumerate(buttonsText):
                x1, x2, y1, y2 = BUTTONS_COORDS[idx]
                isHovering = x1 <= mouse[0] <= x2 and y1 <= mouse[1] <= y2
                buttonColor = (200, 200, 255) if isHovering else "#9A845B"

                buttonText = buttonsFont.render(text, True, buttonColor)
                buttonTextRect = buttonText.get_rect()
                buttonTextRect.topleft = (
                    100 + (10 - len(text)) * 10 + 400 * idx, 812)
                screen.blit(BUTTON, (50 + 400 * idx, 750))
                screen.blit(buttonText, buttonTextRect)

            pygame.display.flip()
            clock.tick(10)
