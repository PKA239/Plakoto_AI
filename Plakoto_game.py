# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 18:08:26 2021

@author: Stephanie Kaes
"""


import numpy as np
import matplotlib.pyplot as plt

import Plakoto
import randomAgent
import userAgent
import psai
import time
import os
import time
#import pubeval
import kotra




def init_board():
    # initializes the game board
    board = np.zeros(51)#29
    board[1] = -15 #gelb startet obven links
    board[24] = 15 #schwarz startet unten links
    return board

def roll_dice():
    # rolls the dice
    dice = np.random.randint(1,7,2)
    return dice

def game_over(board):
    # returns True if the game is over    
    return board[49]==15 or board[50]==-15 \
           or board[24+24] == 1 and board[1] >=0 and board[1+24] != -1 \
           or board[1+24] == -1 and board[24] <=0 and board[24+24] != 1 \
           or board[24+24] == 1 and board[1+24] == -1

def winner(board, show = False):
    #winner 1 falls: 15 steine entfert ODER Gegener in seiner startposition blockiert und eigene startposition leer

    #aus sicht von 1
    if board[49] == 15 or (board[1+24] == -1 and board[24] <= 0 and board[24+24] != 1):
        if show : print("Player 1 wins!")
        return 1

    #aus sicht von -1
    if board[50] == -15 or (board[24+24] == 1 and board[1] >= 0 and board[1+24] != -1):
        if show: print("Player -1 wins!")
        return -1
    
    if board[24+24] == 1 and board[1+24] == -1:
        if show: print("Draw!")
        return 0




def check_for_error(board):
    # checks for obvious errors
    errorInProgram = False
    
    if (sum(board[board>0]) != 15 or sum(board[board<0]) != -15):
        # too many or too few pieces on board
        errorInProgram = True
        print("Too many or too few pieces on board!")
    return errorInProgram
    
def pretty_print(board):
    string = str(np.array2string(board[1:13])+'\n'+
                np.array2string(board[24:12:-1])+'\n'+
                np.array2string(board[49:51]))
    print("board: \n", string)
    
        
def legal_move(board, die, player):
    # finds legal moves for a board and one dice
    # inputs are some BG-board, the number on the die and which player is up
    # outputs all the moves (just for the one die)
    possible_moves = []

    if player == 1:
            # adding options if player is bearing off
            if sum(board[7:25]>0) == 0 and sum(board[25:49]>0) == 0:
                if (board[die] > 0):
                    possible_moves.append(np.array([die,49]))
                    
                elif not game_over(board): # smá fix
                    # everybody's past the dice throw?
                    s = np.max(np.where(board[1:7]>0)[0]+1)
                    if s<die:
                        possible_moves.append(np.array([s,49]))
                    
            possible_start_pips = np.where(board[0:25]>0)[0]

            # finding all other legal options
            for s in possible_start_pips:
                end_pip = s-die
                if end_pip > 0:
                    if board[end_pip] > -2 and board[end_pip + 24] != player:
                        possible_moves.append(np.array([s,end_pip]))
                        
    elif player == -1:
            # adding options if player is bearing off
            if sum(board[1:19]<0) == 0 and sum(board[25:49]<0) == 0: #alle steine im endfeld und keine blockiert
                if (board[25-die] < 0): #stein entfernen
                    possible_moves.append(np.array([25-die,50]))
                elif not game_over(board): # smá fix
                    # everybody's past the dice throw?
                    s = np.min(np.where(board[19:25]<0)[0])
                    if (6-s)<die:   #stein mit zu hohem wurf entfernen, falls nicht anders möglich
                        possible_moves.append(np.array([19+s,50]))

            # finding all other legal options
            possible_start_pips = np.where(board[0:25]<0)[0]
            for s in possible_start_pips:
                end_pip = s+die
                if end_pip < 25:
                    if board[end_pip] < 2 and board[end_pip + 24] != player: #freies feld oder einzelner gegner
                        possible_moves.append(np.array([s,end_pip]))
        
    return possible_moves

def legal_moves(board, dice, player):
    # finds all possible moves and the possible board after-states
    # inputs are the BG-board, the dices rolled and which player is up
    # outputs the possible pair of moves (if they exists) and their after-states

    moves = []
    boards = []

    # try using the first dice, then the second dice
    possible_first_moves = legal_move(board, dice[0], player)
    for m1 in possible_first_moves:
        temp_board = update_board(board,m1,player)
        possible_second_moves = legal_move(temp_board,dice[1], player)
        for m2 in possible_second_moves:
            moves.append(np.array([m1,m2]))
            boards.append(update_board(temp_board,m2,player))
        
    if dice[0] != dice[1]:
        # try using the second dice, then the first one
        possible_first_moves = legal_move(board, dice[1], player)
        for m1 in possible_first_moves:
            temp_board = update_board(board,m1,player)
            possible_second_moves = legal_move(temp_board,dice[0], player)
            for m2 in possible_second_moves:
                moves.append(np.array([m1,m2]))
                boards.append(update_board(temp_board,m2,player))
            
    # if there's no pair of moves available, allow one move:
    if len(moves)==0: 
        # first dice:
        possible_first_moves = legal_move(board, dice[0], player)
        for m in possible_first_moves:
            moves.append(np.array([m]))
            boards.append(update_board(temp_board,m,player))
            
        # second dice:
        if dice[0] != dice[1]:
            possible_first_moves = legal_move(board, dice[1], player)
            for m in possible_first_moves:
                moves.append(np.array([m]))
                boards.append(update_board(temp_board,m,player))
            
    return moves, boards 

def is_legal_move(move,board_copy,dice,player,i):
    if len(move)==0: 
        return True
    global possible_moves
    possible_moves, possible_boards = legal_moves(board_copy, dice, player)
    legit_move = np.array([np.array((possible_move == move)).all() for possible_move in possible_moves]).any()
    if not legit_move:
        print("Game forfeited. Player "+str(player)+" made an illegal move")
        return False
    return True

def update_board(board, move, player):
    # updates the board
    # inputs are some board, one move and the player
    # outputs the updated board
    board_to_update = np.copy(board) 

    # if the move is there
    if len(move) > 0:
        startPip = move[0]
        endPip = move[1]

        # moving the dead piece if the move kills a piece
        block = board_to_update[endPip]==(-1*player)
        if block:
            board_to_update[endPip] = 0
            #jail = 25+(player==1)
            blockpos = endPip + 24
            #board_to_update[jail] = board_to_update[jail] - player
            board_to_update[blockpos] = - player
        
        board_to_update[startPip] = board_to_update[startPip]-1*player
        board_to_update[endPip] = board_to_update[endPip]+player

        #Falls Pip frei wird, prüfe ein geblockter gegnerischer stein frei wird
        unblock = (board_to_update[startPip]) == 0 and (board_to_update[startPip+24] != 0)
        if unblock:
            board_to_update[startPip] = board_to_update[startPip + 24]
            board_to_update[startPip + 24] = 0

    return board_to_update

def valid_move(move,board_copy,dice,player,i):
    # pretty_print(board_copy)
    # print("dice", dice)
    # print(move)
    # print(type(move))
    return True
    
def play_a_game( player1, player2, gui=False, train=False, train_config=None, commentary = False, show =False, user = False):
    board = init_board() # initialize the board
    player = np.random.randint(2)*2-1 # which player begins?

    # play on
    while not game_over(board) and not check_for_error(board):
        if commentary: print("lets go player ",player)
        
        # roll dice
        dice = roll_dice()
        if commentary: print("rolled dices:", dice)
            
        # make a move (2 moves if the same number appears on the dice)
        for i in range(1+int(dice[0] == dice[1])):
            board_copy = np.copy(board)

            #Fall User direkt behandeln, statt in die routine einbinden. Das verhalten ist zu unterschiedlich
            if player == 1 and user:
                # x, y =  eventloop(user_exists)
                Plakoto.gui.showBoard(board, dice, rect=False)
                move = player1.user_action(board_copy, dice, player, i)
                board = update_board(board, move, player)
                Plakoto.gui.showBoard(board, dice, rect=False)
                board_copy = np.copy(board)
                move = player1.user_action(board_copy, dice, player, i)
                board = update_board(board, move, player)
                Plakoto.gui.showBoard(board, dice, rect=False)


            else:
                if train:
                    if player == 1:
                        move = player1.action(board_copy,dice,player,i,train=train,train_config=train_config)

                    elif player == -1:
                        move = player2.action(board_copy,dice,player,i,train=train,train_config=train_config)

                else:
                    if player ==1:
                        move = player1.action(board_copy,dice,player,i)

                    elif player == -1:
                        #eventloop(user_exists)
                        move = player2.action(board_copy,dice,player,i)

                # check if the move is valid
                if not is_legal_move(move,board_copy,dice,player,i):
                    print("Game forfeited. Player "+str(player)+" made an illegal move")
                    return -1*player

                # update the board
                if len(move) != 0:
                    for m in move:
                        board = update_board(board, m, player)
                        if show:
                            Plakoto.gui.showBoard(board, dice)
                            time.sleep(0.5)




                                
            # give status after every move:         
            if commentary: 
                print("move from player",player,":")
                pretty_print(board)
                print("\n")
                
        # switch player
        player = -player

            
    # return the winner
    if show : pretty_print(board)
    return winner(board, show), board

def plot_perf(performance):
    plt.plot(performance)
    plt.show()
    return

def log_status(g, wins, performance, nEpochs):
    if g == 0:
        return performance
    print("game number", g)
    win_rate = wins/nEpochs
    print("win rate:", win_rate)
    performance.append(win_rate)
    return performance


        
  