import numpy as np
import matplotlib.pyplot as plt
import randomAgent
import userAgent
import pygame
from pygame.locals import *
import psai
import os
import time
import Plakoto
import Plakoto_game as bg
import pygame_menu
#import GUI


class Gui():
    pygame.init()
    pygame.font.init()
    UserTurn = False
    font = pygame.font.SysFont('Arial', 30)
    height = 720
    width = 1280
    screen = pygame.display.set_mode((width, height))
    screenMenu = pygame.display.set_mode((width, height))
    menu = pygame_menu.Menu('Backgammon Plakoto', width, height,
                            theme=pygame_menu.themes.THEME_ORANGE)
    marksurface = pygame.surface.Surface((width, height))
    markgroup = pygame.sprite.Group()

    rect24 = pygame.Rect(40, 385, 85, 310)
    rect23 = pygame.Rect(151, 420, 55, 275)
    rect22 = pygame.Rect(229, 385, 85, 310)
    rect21 = pygame.Rect(342, 420, 55, 275)
    rect20 = pygame.Rect(423, 385, 85, 310)
    rect19 = pygame.Rect(533, 420, 55, 275)
    rect18 = pygame.Rect(675, 385, 85, 310)
    rect17 = pygame.Rect(787, 420, 55, 275)
    rect16 = pygame.Rect(867, 385, 85, 310)
    rect15 = pygame.Rect(978, 420, 55, 275)
    rect14 = pygame.Rect(1059, 385, 85, 310)
    rect13 = pygame.Rect(1169, 420, 55, 275)

    rect1 = pygame.Rect(55, 25, 55, 275)
    rect2 = pygame.Rect(137, 25, 85, 310)
    rect3 = pygame.Rect(246, 25, 55, 275)
    rect4 = pygame.Rect(328, 25, 85, 310)
    rect5 = pygame.Rect(437, 25, 55, 275)
    rect6 = pygame.Rect(520, 25, 85, 310)
    rect7 = pygame.Rect(690, 25, 55, 275)
    rect8 = pygame.Rect(772, 25, 85, 310)
    rect9 = pygame.Rect(882, 25, 55, 275)
    rect10 = pygame.Rect(965, 25, 85, 310)
    rect11 = pygame.Rect(1072, 25, 55, 275)
    rect12 = pygame.Rect(1155, 25, 85, 310)

    rect25 = pygame.Rect(0, 385, 35, 310) #bearing off space
    rect0 = pygame.Rect(0, 25, 35, 310) #bearing off space

    def __init__(self):
        self.width = 1280
        self.height = 720
        player1 = randomAgent
        player2 = randomAgent
        # self.screen = pygame.display.set_mode((self.width, self.height))

        # Prepare the window's title bar
        pygame.display.set_caption('Backgammon - Plakoto')
        pygame.display.set_icon(pygame.image.load("dice6.png"))

        # Prepare the board
        self.boardImg = pygame.image.load('board2.png')
        self.boardImg = pygame.transform.scale(self.boardImg, (1280, 720))
        self.blackChecker = pygame.image.load('blackChecker.png')
        self.blackChecker = pygame.transform.scale(self.blackChecker, (55, 55))
        self.whiteChecker = pygame.image.load('whiteChecker.png')
        self.whiteChecker = pygame.transform.scale(self.whiteChecker, (55, 55))
        self.dice1 = pygame.image.load('dice1.png')
        self.dice1 = pygame.transform.scale(self.dice1, (60, 60))
        self.dice2 = pygame.image.load('dice2.png')
        self.dice2 = pygame.transform.scale(self.dice2, (60, 60))
        self.dice3 = pygame.image.load('dice3.png')
        self.dice3 = pygame.transform.scale(self.dice3, (60, 60))
        self.dice4 = pygame.image.load('dice4.png')
        self.dice4 = pygame.transform.scale(self.dice4, (60, 60))
        self.dice5 = pygame.image.load('dice5.png')
        self.dice5 = pygame.transform.scale(self.dice5, (60, 60))
        self.dice6 = pygame.image.load('dice6.png')
        self.dice6 = pygame.transform.scale(self.dice6, (60, 60))
        # self.mark = pygame.image.load('mark.png')
        self.mark = pygame.image.load('thm.png')
        self.largeMark = pygame.transform.scale(self.mark, (85, 50))
        self.smallMark = pygame.transform.scale(self.mark, (55, 50))
        # self.markUpsideDown = pygame.image.load('mark2.png')
        self.markUpsideDown = pygame.image.load('thm.png')
        self.largeMarkUpsideDown = pygame.transform.scale(self.markUpsideDown, (85, 50))
        self.smallMarkUpsideDown = pygame.transform.scale(self.markUpsideDown, (55, 50))

    def hoverloop(self, x, y):
        pos = self.getHoverPosition(x, y)
        empty = Color(0, 0, 0, 0)  # The last 0 indicates 0 alpha, a transparent color
        self.marksurface.fill(empty)  # erases old marks
        if pos == 24: self.marksurface.blit(self.largeMark, (40, 665))
        pygame.display.update()

    def getPosition(self, x, y):
        if self.rect1.collidepoint(x, y): return 1
        if self.rect2.collidepoint(x, y): return 2
        if self.rect3.collidepoint(x, y): return 3
        if self.rect4.collidepoint(x, y): return 4
        if self.rect5.collidepoint(x, y): return 5
        if self.rect6.collidepoint(x, y): return 6
        if self.rect7.collidepoint(x, y): return 7
        if self.rect8.collidepoint(x, y): return 8
        if self.rect9.collidepoint(x, y): return 9
        if self.rect10.collidepoint(x, y): return 10
        if self.rect11.collidepoint(x, y): return 11
        if self.rect12.collidepoint(x, y): return 12
        if self.rect13.collidepoint(x, y): return 13
        if self.rect14.collidepoint(x, y): return 14
        if self.rect15.collidepoint(x, y): return 15
        if self.rect16.collidepoint(x, y): return 16
        if self.rect17.collidepoint(x, y): return 17
        if self.rect18.collidepoint(x, y): return 18
        if self.rect19.collidepoint(x, y): return 19
        if self.rect20.collidepoint(x, y): return 20
        if self.rect21.collidepoint(x, y): return 21
        if self.rect22.collidepoint(x, y): return 22
        if self.rect23.collidepoint(x, y): return 23
        if self.rect24.collidepoint(x, y): return 24
        if self.rect25.collidepoint(x, y): return 25
        if self.rect0.collidepoint(x, y): return 0

    def showBoard(self, board, dice, rect=False):
        def putChecker(color, x, y):
            if color == -1: self.screen.blit(self.whiteChecker, (x, y))
            if color == 1: self.screen.blit(self.blackChecker, (x, y))
            if color == 0: print("color not set")

        def putDice1(eyes):
            if eyes == 1: self.screen.blit(self.dice1, (580, 334))
            if eyes == 2: self.screen.blit(self.dice2, (582, 332))
            if eyes == 3: self.screen.blit(self.dice3, (585, 331))
            if eyes == 4: self.screen.blit(self.dice4, (581, 334))
            if eyes == 5: self.screen.blit(self.dice5, (586, 332))
            if eyes == 6: self.screen.blit(self.dice6, (587, 335))

        def putDice2(eyes):
            if eyes == 1: self.screen.blit(self.dice1, (647, 332))
            if eyes == 2: self.screen.blit(self.dice2, (641, 330))
            if eyes == 3: self.screen.blit(self.dice3, (645, 335))
            if eyes == 4: self.screen.blit(self.dice4, (640, 331))
            if eyes == 5: self.screen.blit(self.dice5, (643, 336))
            if eyes == 6: self.screen.blit(self.dice6, (640, 330))

        self.screen.fill([255, 255, 255])
        self.screen.blit(self.boardImg, (0, 0))
        putDice1(dice[0])
        putDice2(dice[1])

        x = 55
        for i in range(1, 13):
            if i == 7: x += 70
            if board[i] == 0:
                x += 95
                continue

            y = 20
            # blockierter stein falls vorhanden
            if (board[i + 24] != 0):
                putChecker(board[i + 24], x, y)
                y += 50

            color = 0
            if board[i] < 0: color = -1
            if board[i] > 0: color = 1
            for j in range(0, round(abs(board[i]))):
                if j == 6:
                    text = self.font.render(str(round(abs(board[i]))), False, (255, 100, 100))
                    self.screen.blit(text, (x + 10, y - 40))
                    break
                putChecker(color, x, y)
                y += 50

            x += 95

        x = self.width - 110  # es wird von rechts nach links gezeichnet
        for i in range(13, 25):
            if i == 19: x -= 70
            if board[i] == 0:
                x -= 95
                continue

            y = self.height - 80
            # blockierter stein falls vorhanden
            if (board[i + 24] != 0):
                putChecker(board[i + 24], x, y)
                y -= 50

            color = 0
            if board[i] < 0: color = -1
            if board[i] > 0: color = 1
            for j in range(0, round(abs(board[i]))):
                if j == 6:
                    text = self.font.render(str(round(abs(board[i]))), False, (255, 100, 100))
                    self.screen.blit(text, (x + 10, y + 60))
                    break
                putChecker(color, x, y)
                y -= 50

            x -= 95

        if rect:
            pygame.draw.rect(self.screen, (255, 0, 0, 100), self.rect1)
            pygame.draw.rect(self.screen, (255, 0, 0, 100), self.rect2)
            pygame.draw.rect(self.screen, (255, 0, 0, 100), self.rect3)
            pygame.draw.rect(self.screen, (255, 0, 0, 100), self.rect4)
            pygame.draw.rect(self.screen, (255, 0, 0, 100), self.rect5)
            pygame.draw.rect(self.screen, (255, 0, 0, 100), self.rect6)
            pygame.draw.rect(self.screen, (255, 0, 0, 100), self.rect7)
            pygame.draw.rect(self.screen, (255, 0, 0, 100), self.rect8)
            pygame.draw.rect(self.screen, (255, 0, 0, 100), self.rect9)
            pygame.draw.rect(self.screen, (255, 0, 0, 100), self.rect10)
            pygame.draw.rect(self.screen, (255, 0, 0, 100), self.rect11)
            pygame.draw.rect(self.screen, (255, 0, 0, 100), self.rect12)
            pygame.draw.rect(self.screen, (255, 0, 0, 100), self.rect13)
            pygame.draw.rect(self.screen, (255, 0, 0, 100), self.rect14)
            pygame.draw.rect(self.screen, (255, 0, 0, 100), self.rect15)
            pygame.draw.rect(self.screen, (255, 0, 0, 100), self.rect16)
            pygame.draw.rect(self.screen, (255, 0, 0, 100), self.rect17)
            pygame.draw.rect(self.screen, (255, 0, 0, 100), self.rect18)
            pygame.draw.rect(self.screen, (255, 0, 0, 100), self.rect19)
            pygame.draw.rect(self.screen, (255, 0, 0, 100), self.rect20)
            pygame.draw.rect(self.screen, (255, 0, 0, 100), self.rect21)
            pygame.draw.rect(self.screen, (255, 0, 0, 100), self.rect22)
            pygame.draw.rect(self.screen, (255, 0, 0, 100), self.rect23)
            pygame.draw.rect(self.screen, (255, 0, 0, 100), self.rect24)
            pygame.draw.rect(self.screen, (255, 0, 0, 100), self.rect0)
            pygame.draw.rect(self.screen, (255, 0, 0, 100), self.rect25)

        pygame.display.flip()

    def show_thm_logo(self):
        self.startImg = pygame.image.load('thm.png')
        self.startImg = pygame.transform.scale(self.startImg, (1280, 720))
        self.screen.fill([255, 255, 255])
        self.screen.blit(self.startImg, (0, 0))
        # text = self.font.render("Klick to start the game.", False, (255, 100, 100))
        # self.screen.blit(text, (100, 100))
        pygame.display.flip()

        time.sleep(0.4)
        # pygame.display.update()



    # ------------ Event loop -----------------------------------------------
    # def eventloop_help(event):
    #    # General check
    #    if (event.type == MOUSEBUTTONUP):
    #        None
    #
    #    elif event.type == pygame.QUIT:
    #        pygame.quit()
    #
    #    elif (event.type == pygame.K_u):
    #        pygame.display.update()

    def eventloop(self, user=False):
        # Event loop
        x = np.nan
        y = np.nan
        continue_loop = True

        while continue_loop:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()

                # elif event.type == pygame.MOUSEBUTTONDOWN and self.UserTurn:
                #    mouse_presses = pygame.mouse.get_pressed(0)
                #    # Only if left mouse key is pressed, the input is considered valid
                #    if mouse_presses[0]:
                #        x, y = pygame.mouse.get_pos()
                #        position = gui.getPosition(x, y)
                #        userAgent.receivePos(position)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_presses = pygame.mouse.get_pressed()
                    # Only if left mouse key is pressed, the input is considered valid
                    if mouse_presses[0]:
                        print("Left Mouse key was clicked")
                        x, y = pygame.mouse.get_pos()
                        print("Position of mousebuttons", x, y)
                        continue_loop = False
                        return x, y
                    elif mouse_presses[0] == False:
                        print("Please left-click on a field.")
