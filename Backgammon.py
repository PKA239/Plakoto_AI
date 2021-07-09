#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#https://www.youtube.com/watch?v=KLl1tXoaNgk
"""
Backgammon interface
Run this program to play a game of Backgammon
The agent is stored in another file 
Most (if not all) of your agent-develeping code should be written in the agent.py file
Feel free to change this file as you wish but you will only submit your agent 
so make sure your changes here won't affect his performance.
"""
import numpy as np
import matplotlib.pyplot as plt
import randomAgent
import pygame
import psai
from pygame.locals import *
import time
import os
import time
#import pubeval
import kotra
import Backgammon_game as bg

from gui_button import Button, mainloop
# ----------- The Pygame globals -------------------------------------
class Gui():    
       

    def __init__(self):
        self.width = 1280
        self.height = 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.SysFont('Arial', 30)
        
        
       
        #Prepare the window's title bar
        pygame.display.set_caption('Backgammon - Plakoto')
        pygame.display.set_icon(pygame.image.load("dice6.png"))
        
        #Prepare the board
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


    def showBoard(self, board, dice):
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
        self.screen.blit(self.boardImg, (0,0))
        putDice1(dice[0])
        putDice2(dice[1])
        #dice1 = font.render(str(dice[0]), False, (255, 255, 255))
        #dice2 = font.render(str(dice[1]), False, (255, 255, 255))
        #screen.blit(dice1, (620, 340))
        #screen.blit(dice2, (650, 340))
    
        x = 55
        for i in range(1, 13):
            if i == 7: x+=70
            if board[i] == 0:
                x +=95
                continue
    
            y = 20
            #blockierter stein falls vorhanden
            if(board[i+24] != 0):
                putChecker(board[i+24], x, y)
                y += 50
    
            color = 0
            if board[i]<0: color = -1
            if board[i]>0: color = 1
            for j in range(0, round(abs(board[i]))):
                if j == 6:
                    text = self.font.render(str(round(abs(board[i]))), False, (255, 100, 100))
                    self.screen.blit(text, (x+10, y-40))
                    break
                putChecker(color, x, y)
                y+=50
    
            x += 95
    
        x = self.width-110 # es wird von rechts nach links gezeichnet
        for i in range(13, 25):
            if i == 19: x-=70
            if board[i] == 0:
                x -=95
                continue
    
            y = self.height-80
            #blockierter stein falls vorhanden
            if(board[i+24] != 0):
                putChecker(board[i+24], x, y)
                y -= 50
    
            color = 0
            if board[i]<0: color = -1
            if board[i]>0: color = 1
            for j in range(0, round(abs(board[i]))):
                if j == 6:
                    text = self.font.render(str(round(abs(board[i]))), False, (255, 100, 100))
                    self.screen.blit(text, (x+10, y+60))
                    break
                putChecker(color, x, y)
                y-=50
    
            x -= 95
    
        pygame.display.update()
    
    def show_thm_logo(self):        
        self.startImg = pygame.image.load('thm.png')
        self.startImg = pygame.transform.scale(self.startImg, (1280, 720))
        self.screen.fill([255, 255, 255])
        self.screen.blit(self.startImg, (0,0))
        #text = self.font.render("Klick to start the game.", False, (255, 100, 100))
        #self.screen.blit(text, (100, 100))
        pygame.display.flip()
        
        time.sleep(0.4)
        #pygame.display.update()
    
    
    #------------- The start menu GUI -----------------------------------------
    def menu(self):
        TODO
               
        #pygame.display.update()
             
        
        #Load the first picture
        start_img = pygame.image.load('???')
        
        pygame.display.update()
        #pygame.display.flip()
        #time.sleep(5)
        #pygame.display.quit()
    
        return 0
        






        
        
        

    
def main(user_exists, show = False):  
    
    #Initialize Pygame
    pygame.init()
    pygame.display.init()    
    pygame.font.init()   
    clock = pygame.time.Clock()
    gui = Gui()
    
    gui.show_thm_logo()
    
    
    #-------NOT WORKING YET
    button = Button(gui,
    "Click here",
    (100, 100),
    font=30,
    bg="navy",
    feedback="You clicked me")
 
    mainloop(clock, button, gui)
    #----------------------
    
    
    if not show: gui.screen = pygame.quit()
    
    
    startTime=time.time()
    winners = {}; winners["1"]=0; winners["-1"]=0; winners["0"]=0 # Collecting stats of the games
    nGames = 100 # how many games?
    performance = list()

    if user_exists:
        player1 = bg.user_action
    else: 
        player1 = randomAgent
    
    wd = os.getcwd()   
    print("wd", wd)
    player2 = randomAgent #Player 2 is always randomAgent
    #player2 = psai
    #player2.loadModel('/weights/DQN_2000000_20210705T003309Z_001/DQN_2000000')
 
    wins = 0
    nEpochs = 1_000
    
    #----------------------------------------------------------------------------------------------
    
  
    
    # Play game
    print("Playing "+str(nGames)+" between"+str(player1)+"1 and "+str(player2)+"-1")
    
   
    for g in range(nGames):
                
        print("playing game number: " + str(g))
        if g % nEpochs == 0:
            
            
            performance = bg.log_status(g, wins, performance, nEpochs)
            wins = 0
            
       
        
        bg.play_a_game(player1, player2, gui = gui, show=show, user_exists = user_exists) # g, commentary=False)
        #bg.play_a_game(player1, player2, gui, False, None, False, show=show, user_exists = user_exists) # g, commentary=False)
        
        winners[str(bg.winner)] += 1
        wins += (bg.winner==1)       
        
        
        
        
        
        
    print("Out of", nGames, "games,")
    print("player", 1, "won", winners["1"],"times and")
    print("player", -1, "won", winners["-1"],"times and")
    print(winners["0"], " games were a draw")
    runTime=time.time()-startTime
    print("runTime:", runTime)
    print("average time:", runTime/nGames)
    bg.plot_perf(performance)

    #time.sleep(5)
    #time.sleep(60*60)



    
    
if __name__ == '__main__':
    main(user_exists=True, show=True)
