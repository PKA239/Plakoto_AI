#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The intelligent agent
see flipped_agent for an example of how to flip the board in order to always
perceive the board as player 1
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
DQN = keras.Sequential()
DQN.add(layers.Dense(64, input_shape=(49,), kernel_initializer='random_uniform', activation='tanh'))
DQN.add(layers.Dense(32, activation='tanh'))
DQN.add(layers.Dense(1, activation='sigmoid'))

#DQN = keras.Sequential([
#    layers.Dense(50, activation='relu', kernel_initializer='random_uniform', input_shape=(config.nS,)),
#    layers.Dense(1, activation='sigmoid', kernel_initializer='random_uniform')
#])

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
    if name == '64_32_1_tanh_sig':
        DQN = keras.Sequential()
        DQN.add(layers.Dense(64, input_shape=(49,), kernel_initializer='random_uniform', activation='tanh'))
        DQN.add(layers.Dense(32, activation='tanh'))
        DQN.add(layers.Dense(1, activation='sigmoid'))
        DQN.compile(optimizer='Adam', loss='mse')
        DQN_target = tf.keras.models.clone_model(DQN)
        DQN_target.compile(optimizer='Adam', loss='mse')
        DQN.load_weights('/weights/64_32_1_tanh_sig/DQN_600000')


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

board_2_state = lambda board, first_of_2: np.append(board[1:49], first_of_2) #forst_of_two means dice
#bearing_off   = lambda board: sum(board[7:25]>0)==0
game_won      = lambda board: int(board[49]>=15 or (board[1+24] == -1 and board[24] <= 0 and board[24+24] != 1))

def game_over_update(board, reward):
    target = np.array([[reward]])
    S = np.array([board_2_state(board, 1)])
    replay_buffer.push(S, None, reward, S, target, done=True)

def action(board_copy,dice,player,i, train=False,train_config=None):

    # global variables
    global counter
    global bearing_off_counter

    # starts by flipping the board so that the player always sees himself as player 1
    if player == -1:
        board_copy = flip_board(board_copy)

    # check out the legal moves available for the throw
    possible_moves, possible_boards = Plakoto_game.legal_moves(board_copy, dice, player=1)

    # if there are no moves available, return an empty move
    if len(possible_moves) == 0:
        return []

    #if not bearing_off(board_copy):
    model = DQN
    buffer = replay_buffer
    # Current state and Q value, possible next states
    S = np.array([board_2_state(board_copy, i == 2)])  # i -> second dice?
    Q = model(S)
    first_of_2 = 1 + (dice[0] == dice[1]) - i
    S_primes = np.array([board_2_state(b, first_of_2) for b in possible_boards])  # possible next states

    # Find best action and it's q-value w/ epsilon-greedy
    Q_primes = model(S_primes)  # q-value per state
    action = np.argmax(Q_primes)
    
    
    if train and np.random.rand() < config.eps:  # epsilon-greedy when training
        action = np.random.randint(len(possible_moves))


    if train:

        # state chosen from eta-greedy
        S_prime = np.array([board_2_state(possible_boards[action], first_of_2)])

        # update Target network
        target_model = DQN_target
        Q_max = target_model(S_prime)

        # Das Kernstück des ganzen
        reward = game_won(possible_boards[action])  # game won on chosen state?
        target = Q + config.lr * (reward + config.gamma * Q_max - Q)
        buffer.push(S, None, reward, S_prime, target, done=True)

        # update the target network every C steps
        if counter % config.C == 0:
            target_model.set_weights(model.get_weights())

        # train model from buffer
        if counter % config.batch_size == 0 and counter > 0: #and bearing_off_counter > config.batch_size
            state_batch, action_batch, reward_batch, next_state_batch, target_batch, done_batch = replay_buffer.sample(
                config.batch_size)

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
