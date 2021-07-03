#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The intelligent agent
see flipped_agent for an example of how to flip the board in order to always
perceive the board as player 1
"""
import numpy as np
import Backgammon


def flip_board(board_copy):
    # flips the game board and returns a new copy
    idx = np.array([0, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13,
                    12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 26, 25, 28, 27])
    flipped_board = -np.copy(board_copy[idx])

    return flipped_board


def flip_move(move):
    if len(move) != 0:
        for m in move:
            for m_i in range(2):
                m[m_i] = np.array([0, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13,
                                   12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 26, 25, 28, 27])[m[m_i]]
    return move

def action(board_copy, dice, player, i):
    # the champion to be
    # inputs are the board, the dice and which player is to move
    # outputs the chosen move accordingly to its policy

    # check out the legal moves available for the throw
    possible_moves, possible_boards = Backgammon.legal_moves(board_copy, dice, player)

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

    return move
