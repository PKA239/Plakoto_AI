#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The intelligent agent
see flipped_agent for an example of how to flip the board in order to always
perceive the board as player 1
"""
import numpy as np
import Backgammon

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

#Buffer for Samples/minibatches
from basic_buffer import BasicBuffer

class config:
    nS = 48+1 # state space demension: boardspace + isAnotherMoveComing
    eps = 0.05
    lr = 0.05
    gamma = 0.99
    C = 100
    batch_size = 32
    D_max = 1000

print('Model initialized with parameters:','\n'*2, config, '\n'*2)

# Policy Network | Deep Q-network
DQN = keras.Sequential([
    layers.Dense(50, activation='relu', kernel_initializer='random_uniform', input_shape=(config.nS,)),
    # layers.Dense(4, activation='relu', kernel_initializer='random_uniform'),
    layers.Dense(1, activation='sigmoid', kernel_initializer='random_uniform')
])
DQN.compile(optimizer = 'Adam',loss = 'mse')

# Target network. Gets copied from policy-network at certain intervals
DQN_target = tf.keras.models.clone_model(DQN) # https://www.tensorflow.org/api_docs/python/tf/keras/models/clone_model
DQN_target.compile(optimizer = 'Adam',loss = 'mse')

# Policy Network bearing off phase
DQN_bearing_off = tf.keras.models.clone_model(DQN)
DQN_bearing_off.compile(optimizer = 'Adam',loss = 'mse')

# Target network bearing off phase
DQN_bearing_off_target = tf.keras.models.clone_model(DQN)
DQN_bearing_off_target.compile(optimizer = 'Adam',loss = 'mse')

# replay buffer to reduce correlation
replay_buffer = BasicBuffer(config.D_max)
replay_buffer_bearing_off = BasicBuffer(config.D_max)

# for tracking progress
counter = 0
bearing_off_counter = 0
saved_models = []

print("Network architecture: \n", DQN)

# ------------------------------- Helper functions ---------------------------------

def flip_board(board_copy):
    print("flipped board")
    #flips the game board and returns a new copy
    idx = np.array([0,24,23,22,21,20,19,18,17,16,15,14,13,
    12,11,10,9,8,7,6,5,4,3,2,1,
    48,47,46,45,44,43,42,41,40,39,38,37,
    36,35,34,33,32,31,30,29,28,27,26,25,
    50,49])
    flipped_board = -np.copy(board_copy[idx])
    return flipped_board

def flip_move(move):
    if len(move)!=0:
        for m in move:
            for m_i in range(2):
                #m[m_i] = np.array([0,24,23,22,21,20,19,18,17,16,15,14,13,
                #                12,11,10,9,8,7,6,5,4,3,2,1,26,25,28,27])[m[m_i]]
                m[m_i] = np.array([0,24,23,22,21,20,19,18,17,16,15,14,13,
                        12,11,10,9,8,7,6,5,4,3,2,1,
                        48,47,46,45,44,43,42,41,40,39,38,37,
                        36,35,34,33,32,31,30,29,28,27,26,25,
                        50,49])[m[m_i]]
    return move

def action(board_copy,dice,player,i):
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
