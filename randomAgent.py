#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The intelligent agent
see flipped_agent for an example of how to flip the board in order to always
perceive the board as player 1
"""
import numpy as np
import Plakoto_game as bg

def isUserAgent():
    return False
def action(board_copy,dice,player,i):
    # plain and simple random "AI"
    # inputs are the board, the dice and which player is to move
    # outputs the chosen move accordingly to its policy

    # check out the legal moves available for the throw
    possible_moves, possible_boards = bg.legal_moves(board_copy, dice, player)

    # if there are no moves available
    if len(possible_moves) == 0:
        return []

    # make the best move according to the policy

    # policy missing, returns a random move for the time being
    #
    #
    #
    #
    #
    move = possible_moves[np.random.randint(len(possible_moves))]
    #print(move)
    return move