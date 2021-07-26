# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 21:49:19 2021

@author: Stephanie Kaes
"""
import time

import numpy as np
import pygame
from pygame.locals import *

import Plakoto_game
import Plakoto_game as bg
#import GUI
import Plakoto

             
#-------------The user Agent -----------------------------------------    
startpos = -1
endpos = -1
valid=False
dice = [-1, -1]

def isUserAgent():
    return True


def setDice(_dice):
    global dice
    dice = _dice
    #to copy by value
    #dice[0] = _dice[0]
    #dice[1] = _dice[1]

def hasPossibleMove(board, player):
    global dice
    print('player in hasPossibleMove: ', player)
    print('dice: ', dice)
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
        startpos = -1
        endpos = -1
        return

    print("dice1: ", dice[1])
    if player == 1:
        #if sum(board[7:25]>0):
        if startpos == -1 and board[pos] >= 1:
            startpos = pos
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

        elif dice[1] != -1 and pos == startpos - dice[1] and pos >= 1:
            if board[pos] >= -1 and board[pos+24] != 1:
                endpos = pos
                valid = True
                dice[1] = -1
            else:
                startpos = -1
                endpos = -1

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

    elif player == -1:
        if startpos == -1 and board[pos] <= -1:
            startpos = pos
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
        elif dice[0] != -1 and pos > 24 and startpos + dice[0] > 24 and sum(board[1:19]<0) == 0 and sum(board[25:49]<0) == 0:
            endpos = 50
            valid = True
            dice[0] = -1
            # chosen dice
            #chosendice[move_no] = endpos
        elif dice[1] != -1 and pos > 24 and startpos + dice[1] > 24 and sum(board[1:19]<0) == 0 and sum(board[25:49]<0) == 0:
            endpos = 50
            valid = True
            dice[1] = -1

        else:
            print("deleting positions4")
            startpos = -1
            endpos = -1

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

    #eventloop(user_exists)
    # check out the legal moves available for the throw
    #possible_moves, possible_boards = bg.legal_moves(board_copy, dice, player)
    #print("possible movees: ", possible_moves)
    #print("Possible moves:\n", possible_moves)
    ## if there are no moves available
    #if len(possible_moves) == 0:
    #    return []
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

            #print("move_no: ", move_no)
            #if move_no == 0:
            #    handleInput(move_no, position, board_copy, player, dice)
            #elif move_no == 1:
            #    #print("dice", dice)
            #    #print("dice chosen during last action", chosendice[0])
            #    #print("where", np.where(dice == chosendice[0]))
            #    dice_idx = np.where(dice == chosendice[0])[0]
            #    print("dice", dice)
            #    print("dice idx", dice_idx)
            #    if len(dice_idx) > 1: # doubles
            #        handleInput(move_no, position, board_copy, player, dice)
            #    else:
            #        dice = np.delete(dice,dice_idx)
            #        print("Shortened dice: ", dice)
            #        handleInput(move_no, position, board_copy, player, [np.nan, dice])

    print("usaragent move: ", [startpos, endpos])
    return [startpos, endpos]