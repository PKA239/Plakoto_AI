# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 21:49:19 2021

@author: Stephanie Kaes
"""
import numpy as np
import Backgammon_game as bg

             
#-------------The user Agent -----------------------------------------    

def user_action(x, y, board_copy,dice,player,i):
    # user agent
    # inputs are the board, the dice and which player is to move
    # outputs the chosen move accordingly to mouse input

    #eventloop(user_exists)
    # check out the legal moves available for the throw
    possible_moves, possible_boards = bg.legal_moves(board_copy, dice, player)

    # if there are no moves available
    if len(possible_moves) == 0:
        return []

    
    move = possible_moves[np.random.randint(len(possible_moves))]
    

    return move