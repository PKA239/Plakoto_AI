#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
import time
# import sys
import time
#import pubeval
import kotra

def init_board():
    # initializes the game board
    board = np.zeros(51)#29
    board[1] = -15 #weiß startet obven rechts
    board[24] = 15 #schwarz startet unten rechts
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

        #kein kill mehr, blocken einfügen

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
    
def play_a_game(player1, player2, train=False, train_config=None, commentary = False, show=False):
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
            
            if train:
                if player == 1:
                    move = player1.action(board_copy,dice,player,i,train=train,train_config=train_config) 
                elif player == -1:
                    move = player2.action(board_copy,dice,player,i,train=train,train_config=train_config)
            else:
                if player == 1:
                    move = player1.action(board_copy,dice,player,i) 
                elif player == -1:
                    move = player2.action(board_copy,dice,player,i)

            # check if the move is valid
            if not is_legal_move(move,board_copy,dice,player,i):
                print("Game forfeited. Player "+str(player)+" made an illegal move")
                return -1*player
                
            # update the board
            if len(move) != 0:
                for m in move:
                    if show:
                        showBoard(board, dice)
                        time.sleep(0.05)
                    board = update_board(board, m, player)
                    if show:
                        showBoard(board, dice)


                                
            # give status after every move:         
            if commentary: 
                print("move from player",player,":")
                pretty_print(board)
                print("\n")
                
        # players take turns 
        player = -player

        # if game_over(board) and player == -1:
        #     print("final move, dice and board:")
        #     print(move)
        #     print(dice)
        #     pretty_print(board)
        #     exit()

            
    # return the winner
    if show : pretty_print(board)
    return winner(board, show), board
    #return -1*player, board

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

def showBoard(board, dice):
    def putChecker(color, x, y):
        if color == -1: screen.blit(whiteChecker, (x, y))
        if color == 1: screen.blit(blackChecker, (x, y))
        if color == 0: print("color not set")

    screen.fill([255, 255, 255])
    screen.blit(boardImg, (0,0))
    dice1 = font.render(str(dice[0]), False, (255, 255, 255))
    dice2 = font.render(str(dice[1]), False, (255, 255, 255))
    screen.blit(dice1, (620, 340))
    screen.blit(dice2, (650, 340))

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
                text = font.render(str(round(abs(board[i]))), False, (255, 100, 100))
                screen.blit(text, (x+10, y-40))
                break
            putChecker(color, x, y)
            y+=50

        x += 95

    x = width-110 # es wird von rechts nach links gezeichnet
    for i in range(13, 25):
        if i == 19: x-=70
        if board[i] == 0:
            x -=95
            continue

        y = height-80
        #blockierter stein falls vorhanden
        if(board[i+24] != 0):
            putChecker(board[i+24], x, y)
            y -= 50

        color = 0
        if board[i]<0: color = -1
        if board[i]>0: color = 1
        for j in range(0, round(abs(board[i]))):
            if j == 6:
                text = font.render(str(round(abs(board[i]))), False, (255, 100, 100))
                screen.blit(text, (x+10, y+60))
                break
            putChecker(color, x, y)
            y-=50

        x -= 95

    pygame.display.update()

pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Arial', 30)
width = 1280
height = 720
boardImg = pygame.image.load('board.gif')
boardImg = pygame.transform.scale(boardImg, (1280, 720))
blackChecker = pygame.image.load('blackChecker.png')
blackChecker = pygame.transform.scale(blackChecker, (55, 55))
whiteChecker = pygame.image.load('whiteChecker.png')
whiteChecker = pygame.transform.scale(whiteChecker, (55, 55))
screen = pygame.display.set_mode((width, height))
def main(show=False):
    if not show: screen = pygame.quit()
    startTime=time.time()
    winners = {}; winners["1"]=0; winners["-1"]=0; winners["0"]=0 # Collecting stats of the games
    nGames = 1 # how many games?
    performance = list()
    player1 = randomAgent
    player2 = randomAgent
    wins = 0
    nEpochs = 1_000
    
    
    
    print("Playing "+str(nGames)+" between"+str(player1)+"1 and "+str(player2)+"-1")
    for g in range(nGames):
        #print("playing game number: " + str(g))
        if g % nEpochs == 0:
            performance = log_status(g, wins, performance, nEpochs)
            wins = 0
        winner, board = play_a_game(player1, player2, False, None, False, show=show) # g, commentary=False)
        #winners[str(winner[0])] += 1
        winners[str(winner)] += 1
        wins += (winner==1)
    print("Out of", nGames, "games,")
    print("player", 1, "won", winners["1"],"times and")
    print("player", -1, "won", winners["-1"],"times and")
    print(winners["0"], " games were a draw")
    runTime=time.time()-startTime
    print("runTime:", runTime)
    print("average time:", runTime/nGames)
    plot_perf(performance)

    #time.sleep(5)
    #time.sleep(60*60)
    mousetest()


def mousetest():
    # https://www.pygame.org/docs/ref/mouse.html
    while True:
      for event in pygame.event.get():
            if event.type == pygame.QUIT:
               pygame.quit()
               return
            elif event.type == pygame.MOUSEWHEEL:
               print(event)
               print(event.x, event.y)
               print(event.flipped)
               print(event.which)
               # can access properties with
               # proper notation(ex: event.y)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                if mouse_presses[0]:
                    print("Left Mouse key was clicked")
                    print("Position of mousebuttons", pygame.mouse.get_pos)
      clock.tick(60)
    #print("State of mousebuttons", pygame.mouse.get_pressed)
    #print("Position of mousebuttons", pygame.mouse.get_pos)
    
    
if __name__ == '__main__':
    main(show=True)


    #testboard = np.zeros(29 + 28)  # 29
    #testboard[1] = -15
    #testboard[2] = -1
    #testboard[3] = -2
    #testboard[3+28] = 1
    #testboard[4] = -4
    #testboard[5] = -4
    #testboard[6] = -4
    #testboard[7] = -4
    #testboard[8] = -4
    #testboard[9] = -4
    #testboard[10] = -4
    #testboard[11] = -4
    #testboard[12] = -4
    #testboard[13] = 5
    #testboard[14] = 2
    #testboard[14+28] = -1
    #testboard[15] = 6
    #testboard[16] = 6
    #testboard[17] = 6
    #testboard[18] = 6
    #testboard[19] = 6
    #testboard[20] = 6
    #testboard[21] = 6
    #testboard[22] = 6
    #testboard[23] = 6
    #testboard[24] = 15
    #showBoard(testboard)