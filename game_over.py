import pygame
import sys
from ui_elements import Button
from state import State


class GameOver:
    def retry(self):
        State.currentPage = "PLAY"

    def mainMenu(self):
        State.currentPage = "MAINMENU"

    def __init__(self) -> None:
        pygame.init()
        screen = pygame.display.set_mode((800, 600))

        fontObj = pygame.font.Font('./assets/fonts/Pixeltype.ttf', 100)
        cursorFont = pygame.font.SysFont("cambria", 35)

        gameOverText = fontObj.render("GAME OVER", True, "red")
        gameOverTextRect = gameOverText.get_rect(
            center=(screen.get_width()/2, 200))

        # abaroshCover = pygame.image.load("assets/title_image/Abarosh.png")
        # w, h = abaroshCover.get_size()
        # aspectRatio = float(w)/h
        # abaroshCover = pygame.transform.scale(
        #     abaroshCover, (250, 250/aspectRatio))
        # abaroshCoverRect = abaroshCover.get_rect(
        #     center=(screen.get_width()/2, abaroshTextRect.bottom+130))

        buttons = []
        margin = 30
        retry = Button(screen, screen.get_width()//2,
                       gameOverTextRect.bottom+100, "Retry", self.retry)
        mainMenu = Button(screen, screen.get_width()//2, margin +
                          retry.rect.bottom, "Main Menu", self.mainMenu)
        buttons.append(retry)
        buttons.append(mainMenu)

        offsetX = -18
        offsetY = 8
        cursor = cursorFont.render(">", True, "white")
        cursorRect = cursor.get_rect(
            center=(retry.rect.left+offsetX, retry.rect.centery-offsetY))
        hoveredIdx = 0
        running = True
        while State.currentPage == "GAMEOVER":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        button.checkForInput(pygame.mouse.get_pos())
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        hoveredIdx += 1
                        if hoveredIdx >= len(buttons):
                            hoveredIdx = 0
                    if event.key == pygame.K_UP:
                        hoveredIdx -= 1
                        if hoveredIdx < 0:
                            hoveredIdx = len(buttons) - 1

                    if event.key == pygame.K_RETURN:
                        buttons[hoveredIdx].callback()

            screen.fill((0, 0, 0))
            screen.set_alpha(100)
            # screen.blit(abaroshCover, abaroshCoverRect)
            screen.blit(gameOverText, gameOverTextRect)

            for i, button in enumerate(buttons):
                button.update()
                if (button.changeColor(pygame.mouse.get_pos())):
                    hoveredIdx = i

            hoveredButton = buttons[hoveredIdx]
            cursorRect = cursor.get_rect(
                center=(hoveredButton.text_rect.left+offsetX, hoveredButton.rect.centery-offsetY))
            hoveredButton.textColChange()
            screen.blit(cursor, cursorRect)

            pygame.display.update()
