# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 21:49:19 2021

@author: Stephanie Kaes
"""
import pygame
import Plakoto_game
import Plakoto

             
#-------------The user Agent -----------------------------------------
import classGUI

startpos = -1
endpos = -1
valid=False
dice = [-1, -1]

def isUserAgent():
    return True


def setDice(_dice):
    global dice
    dice = _dice

def hasPossibleMove(board, player):
    global dice
    #print('player in hasPossibleMove: ', player)
    #print('dice: ', dice)
    for i in range(0,25):
        if board[i] > 0 and player == 1 and dice[0] != -1 and board[i-dice[0]] >= -1:
            return True
        if board[i] > 0 and player == 1 and dice[1] != -1 and board[i-dice[1]] >= -1:
            return True
        if board[i] > 0 and player == 1 and dice[0] != -1 and sum(board[7:25]>0) == 0 and sum(board[25:49]>0) == 0 and i - dice[0] <= 0:
            return True
        if board[i] > 0 and player == 1 and dice[1] != -1 and sum(board[7:25]>0) == 0 and sum(board[25:49]>0) == 0 and i - dice[1] <= 0:
            return True

        if board[i] < 0 and player == -1 and dice[0] != -1 and board[i+dice[0]] <= 1:
            return True
        if board[i] < 0 and player == -1 and dice[1] != -1 and board[i+dice[1]] <= 1:
            return True
        if board[i] < 0 and player == -1 and dice[0] != -1 and sum(board[1:19]<0) == 0 and sum(board[25:49]<0) == 0 and i + dice[0] >= 25:
            return True
        if board[i] < 0 and player == -1 and dice[1] != -1 and sum(board[1:19]<0) == 0 and sum(board[25:49]<0) == 0 and i + dice[1] >= 25:
            return True
    print('no possible moves')
    return False

def handleInput(pos, board, player, dice):
    Plakoto_game.pretty_print(board)
    global startpos
    global endpos
    global valid

    #startposition setzen
    
    #For debugging-------------------

    print("\n")
    print("startpos", startpos)
    #print("board", board)
    #print("pos", pos)
    #print("board[pos]", board[pos])
    #-------------------------------

    if pos == None:
        print("deleting positions1")
        Plakoto.gui.showBoard(board, dice, player)
        startpos = -1
        endpos = -1
        return

    print("dice1: ", dice[1])
    if player == 1:
        #if sum(board[7:25]>0):
        if startpos == -1 and board[pos] >= 1:
            startpos = pos
            Plakoto.gui.showBoard(board, dice, player, mark=pos)
            print("startpos gesetzt ", startpos)
        elif dice[0] != -1 and pos == startpos - dice[0] and pos >= 1:
            if board[pos] >= -1 and board[pos+24] != 1:
                endpos = pos
                valid = True
                dice[0] = -1
                #chosendice[move_no] = startpos - pos
                print("final position set. ", endpos)

            else:
                startpos = -1
                endpos = -1
                Plakoto.gui.showBoard(board, dice, player)

        elif dice[1] != -1 and pos == startpos - dice[1] and pos >= 1:
            if board[pos] >= -1 and board[pos+24] != 1:
                endpos = pos
                valid = True
                dice[1] = -1
            else:
                startpos = -1
                endpos = -1
                Plakoto.gui.showBoard(board, dice, player)

        elif dice[0] != -1 and pos < 1 and startpos - dice[0] < 1 and sum(board[7:25]>0) == 0 and sum(board[25:49]>0) == 0:
            #chosen dice ergänzen
            endpos = 49
            valid = True
            dice[0] = -1
        elif dice[1] != -1 and pos < 1 and startpos - dice[1] < 1 and sum(board[7:25]>0) == 0 and sum(board[25:49]>0) == 0:
            endpos = 49
            valid = True
            dice[1] = -1

        else:
            print("deleting positions2")
            startpos = -1
            endpos = -1
            Plakoto.gui.showBoard(board, dice, player)

    elif player == -1:
        if startpos == -1 and board[pos] <= -1:
            startpos = pos
            Plakoto.gui.showBoard(board, dice, player, mark=pos)
        elif dice[0] != -1 and pos == startpos + dice[0] and pos <= 24:
            if board[pos] <= 1 and board[pos+24] != -1:
                endpos = pos
                valid = True
                dice[0] = -1
                #chosendice[move_no] = pos - startpos

            else:
                print("deleting positions3")
                startpos = -1
                endpos = -1
                Plakoto.gui.showBoard(board, dice, player)

        elif dice[1] != -1 and pos == startpos + dice[1] and pos <= 24:
            if board[pos] <= 1 and board[pos+24] != -1:
                endpos = pos
                valid = True
                dice[1] = -1
                #chosendice[move_no] = pos - startpos

            else:
                print("deleting positions3")
                startpos = -1
                endpos = -1
                Plakoto.gui.showBoard(board, dice, player)
        elif dice[0] != -1 and pos > 24 and startpos + dice[0] > 24 and sum(board[1:19]<0) == 0 and sum(board[25:49]<0) == 0:
            endpos = 50
            valid = True
            dice[0] = -1

        elif dice[1] != -1 and pos > 24 and startpos + dice[1] > 24 and sum(board[1:19]<0) == 0 and sum(board[25:49]<0) == 0:
            endpos = 50
            valid = True
            dice[1] = -1

        else:
            print("deleting positions4")
            startpos = -1
            endpos = -1
            Plakoto.gui.showBoard(board, dice, player)

def user_action(board_copy,player,i):
    # user agent
    # inputs are the board, the dice and which player is to move
    # outputs the chosen move accordingly to mouse input

    global startpos
    global endpos
    global valid
    global dice

    #global chosendice
    startpos = -1
    endpos = -1
    valid = False

    if not hasPossibleMove(board_copy, player):
        return []

    #--------- Eventloop of user_action ----------------------------------------
    while not valid:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            position = Plakoto.gui.getPosition(x, y)
            handleInput(position, board_copy, player, dice)

    print("usaragent move: ", [startpos, endpos])
    return [startpos, endpos]