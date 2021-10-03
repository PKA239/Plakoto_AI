#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The intelligent agent.
The code for this agent was copied from https://github.com/weekend37/Backgammon/blob/master/kotra.py
and then edited.
Many of the functions have been rewritten to work with plakoto instead of backgammon.
A function to load trained models has been added to.
The most essential code for deep-q-learning stayed the same and is marked.
"""
import numpy as np

import Plakoto_game

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

#Buffer for Samples/minibatches
from basic_buffer import BasicBuffer

def isUserAgent():
    return False
"""
The Config and the creation of the model is strongly inspired by https://github.com/weekend37/Backgammon/blob/master/kotra.py
"""
class config:
    nS = 48+1 # state space demension: boardspace + isAnotherMoveComing
    eps = 0.05
    lr = 0.05
    gamma = 0.99
    # update the target network every C steps
    C = 100
    batch_size = 32
    D_max = 1000

print('Model initialized with parameters:','\n'*2, config, '\n'*2)

# Policy Network | Deep Q-network
DQN = keras.Sequential()
DQN.add(layers.Dense(64, kernel_initializer='random_uniform', activation='relu'))
DQN.add(layers.Dense(64, activation='relu'))
DQN.add(layers.Dense(64, activation='relu'))
DQN.add(layers.Dense(1, activation='sigmoid'))

DQN.compile(optimizer = 'Adam',loss = 'mse')



# Target network. Gets copied from policy-network at certain intervals
DQN_target = tf.keras.models.clone_model(DQN) # https://www.tensorflow.org/api_docs/python/tf/keras/models/clone_model
DQN_target.compile(optimizer = 'Adam',loss = 'mse')

# replay buffer to reduce correlation
replay_buffer = BasicBuffer(config.D_max)
replay_buffer_bearing_off = BasicBuffer(config.D_max)

# for tracking progress
counter = 0
saved_models = []

print("Network architecture: \n", DQN)

# ------------------------------- Helper functions ---------------------------------
def loadModel(name):
    global DQN
    if name == '64_64_32_1_tanh':
        DQN = keras.Sequential()
        DQN.add(layers.Dense(64, kernel_initializer='random_uniform', activation='tanh'))
        DQN.add(layers.Dense(64, kernel_initializer='random_uniform', activation='tanh'))
        DQN.add(layers.Dense(32, activation='tanh'))
        DQN.add(layers.Dense(1, activation='sigmoid'))
        DQN.compile(optimizer='Adam', loss='mse')
        DQN_target = tf.keras.models.clone_model(DQN)
        DQN_target.compile(optimizer='Adam', loss='mse')
        DQN.load_weights('./weights/64_64_32_1_tanh_sig/DQN_600000')
    if name == '64_32_1_relu_1700k':
        DQN = keras.Sequential()
        DQN.add(layers.Dense(64, kernel_initializer='random_uniform', activation='relu'))
        DQN.add(layers.Dense(32, activation='relu'))
        DQN.add(layers.Dense(1, activation='sigmoid'))
        DQN.compile(optimizer='Adam', loss='mse')
        DQN_target = tf.keras.models.clone_model(DQN)
        DQN_target.compile(optimizer='Adam', loss='mse')
        DQN.load_weights('./weights/64_32_1_relu_1700/DQN_1700000')
    if name == '64_32_1_relu_700k':
        DQN = keras.Sequential()
        DQN.add(layers.Dense(64, kernel_initializer='random_uniform', activation='relu'))
        DQN.add(layers.Dense(32, activation='relu'))
        DQN.add(layers.Dense(1, activation='sigmoid'))
        DQN.compile(optimizer='Adam', loss='mse')
        DQN_target = tf.keras.models.clone_model(DQN)
        DQN_target.compile(optimizer='Adam', loss='mse')
        DQN.load_weights('./weights/64_32_1_relu_700k/DQN_700000')
    if name == '64_32_1_relu_2000k':
        DQN = keras.Sequential()
        DQN.add(layers.Dense(64, kernel_initializer='random_uniform', activation='relu'))
        DQN.add(layers.Dense(32, activation='relu'))
        DQN.add(layers.Dense(1, activation='sigmoid'))
        DQN.compile(optimizer='Adam', loss='mse')
        DQN_target = tf.keras.models.clone_model(DQN)
        DQN_target.compile(optimizer='Adam', loss='mse')
        DQN.load_weights('./weights/64_32_1_relu_2000/DQN_2000000')
    if name == '128_1_tanh_1200k':
        DQN = keras.Sequential()
        DQN.add(layers.Dense(128, kernel_initializer='random_uniform', activation='tanh'))
        DQN.add(layers.Dense(1, activation='sigmoid'))
        DQN.compile(optimizer='Adam', loss='mse')
        DQN_target = tf.keras.models.clone_model(DQN)
        DQN_target.compile(optimizer='Adam', loss='mse')
        DQN.load_weights('./weights/128_1_tanh_1200/DQN_1200000')
    if name == '16_8_8_8_4_4_1_relu_700k':
        DQN = keras.Sequential()
        DQN.add(layers.Dense(16, kernel_initializer='random_uniform', activation='tanh'))
        DQN.add(layers.Dense(8, activation='tanh'))
        DQN.add(layers.Dense(8, activation='tanh'))
        DQN.add(layers.Dense(8, activation='tanh'))
        DQN.add(layers.Dense(4, activation='tanh'))
        DQN.add(layers.Dense(4, activation='tanh'))
        DQN.add(layers.Dense(1, activation='sigmoid'))
        DQN_target = tf.keras.models.clone_model(DQN)
        DQN_target.compile(optimizer='Adam', loss='mse')
        DQN.load_weights('./weights/16_8_8_8_4_4_1_relu_700/DQN_700000')


"""
flip_board and flip_move are inspired by https://github.com/weekend37/Backgammon/blob/master/kotra.py
but had to be changed in order to work with the 50-position state that we use for plakoto.
"""
def flip_board(board_copy):
    #flips the game board and returns a new copy
    idx = np.array([0,24,23,22,21,20,19,18,17,16,15,14,13,
    12,11,10,9,8,7,6,5,4,3,2,1,
    48,47,46,45,44,43,42,41,40,39,38,37,
    36,35,34,33,32,31,30,29,28,27,26,25,
    50,49])
    flipped_board = -np.copy(board_copy[idx])
    return flipped_board

def flip_move(move):
    #flips move
    if len(move)!=0:
        for m in move:
            for m_i in range(2):
                m[m_i] = np.array([0,24,23,22,21,20,19,18,17,16,15,14,13,
                        12,11,10,9,8,7,6,5,4,3,2,1,
                        48,47,46,45,44,43,42,41,40,39,38,37,
                        36,35,34,33,32,31,30,29,28,27,26,25,
                        50,49])[m[m_i]]
    return move
#takes board without positions 49 and 50 and appends if there is a sencond set of moves in case of a double
board_2_state = lambda board, first_of_2: np.append(board[1:49], first_of_2)
W
game_won      = lambda board: int(board[49]>=15 or
                                  board[1+24] == -1 and
                                   board[24] <= 0 and
                                   board[24+24] != 1)

"""
https://github.com/weekend37/Backgammon/blob/master/kotra.py
"""
def game_over_update(board, reward):
    target = np.array([[reward]])
    S = np.array([board_2_state(board, 1)])
    replay_buffer.push(S, None, reward, S, target, done=True)

def action(board_copy,dice,player,i, train=False,train_config=None):

    """
    The following code is mostly copied from https://github.com/weekend37/Backgammon/blob/master/kotra.py
    """

    # global variables
    global counter

    # starts by flipping the board so that the player always sees himself as player 1
    if player == -1:
        board_copy = flip_board(board_copy)

    # check out the legal moves available for the throw
    possible_moves, possible_boards = Plakoto_game.legal_moves(board_copy, dice, player=1)

    # if there are no moves available, return an empty move
    if len(possible_moves) == 0:
        return []

    model = DQN
    buffer = replay_buffer
    # Current state and Q value, possible next states
    State = np.array([board_2_state(board_copy, i == 2)])  # i -> second dice?
    Q = model(State)
    first_of_2 = 1 + (dice[0] == dice[1]) - i #sind würfel pasch -> erster wurf von 2
    #Array aus möglichen nächsten states (boards)
    S_next = np.array([board_2_state(b, first_of_2) for b in possible_boards])  # possible next states

    # Find best action and it's q-value without epsilon-greedy
    Q_next = model(S_next)     #bewertet jede action aus s_next
    action = np.argmax(Q_next) #nimmt action mit höchster bewertung

    # epsilon-greedy. Nimm mit wahrscheinlichkeit epsilon einen zufälligen statt besten zug
    if train and np.random.rand() < config.eps:
        action = np.random.randint(len(possible_moves))


    if train:

        # state chosen from eta-greedy
        S_best = np.array([board_2_state(possible_boards[action], first_of_2)])

        # update Target network
        target_model = DQN_target
        Q_max = target_model(S_best)


        reward = game_won(possible_boards[action])
        targetQ = Q + config.lr * (reward + config.gamma * Q_max - Q)


        buffer.push(State, None, reward, S_next, targetQ, done=True)

        # update the target network every C steps
        if counter % config.C == 0:
            target_model.set_weights(model.get_weights())

        # train model from buffer
        if counter % config.batch_size == 0 and counter > 0:
            state_batch, action_batch, reward_batch, next_state_batch, target_batch, done_batch = replay_buffer.sample(
                config.batch_size)

            # train with state and target-Q
            # model takes state and calculates Q-Value
            # calculate loss by comparing Q-Value with given target-Q Value
            # backpropergate and adjust weights
            DQN.train_on_batch(np.array(state_batch), np.array(target_batch))

        # save model every 1000_000 training moves
        if counter % 100000 == 0 and not counter in saved_models and counter != 0:
            # save both networks
            filepath = "./psai_weights/DQN_" + str(counter)
            print("saving weights in file:" + filepath)
            DQN.save(filepath, overwrite=True, include_optimizer=True)

            #for colab
            #filepath = "/content/drive/My Drive/ai4games/psai_weights_Dense128Relu/DQN_" + str(counter)
            #print("saving weights in file:" + filepath)
            #DQN.save(filepath, overwrite=True, include_optimizer=True)

        counter += 1

    # Make the move
    move = possible_moves[action]

    if player == -1:
        # if the table was flipped the move has to be flipped as well
        move = flip_move(move)

    return move