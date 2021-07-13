import numpy as np
import matplotlib.pyplot as plt

import Backgammon_game
from Backgammon_game import *
import kotra
import psai
import randomAgent
import time
import pygame

def plot_perf(performance):
    plt.plot(performance)
    plt.show()
    return

def evaluate(agent, evaluation_agent, n_eval, n_games):
    wins = 0
    for i in range(n_eval):
        winner, board = Backgammon_game.play_a_game(agent, evaluation_agent)
        wins += int(winner==1)
    winrate = round(wins/n_eval*100,3)
    print("Win-rate after training for "+str(n_games)+" games: "+str(winrate)+"%" )
    return winrate

def train(n_games=10000, n_epochs=500, n_eval=20, show=False, file=""):
    pygame.quit()
    agent = psai
    evaluation_agent = randomAgent
    winrates = []
    print("start training")
    startTime = time.time()
    for g in range(n_games):
        #print(g)
        if g%10 == 0: print(g)
        if g % n_epochs == 0 and g != 0:
            winrate = evaluate(agent, evaluation_agent, n_eval, n_games=g)
            winrates.append(winrate)
            print(g, winrate)

        winner, board = Backgammon_game.play_a_game(agent, agent, train=True, train_config={'g':g}, gui=False)
        agent.game_over_update(board, int(winner==1))
        agent.game_over_update(psai.flip_board(board), int(winner==-1))

    runTime = time.time() - startTime
    print("runTime:", runTime)
    print("average time:", runTime / n_games)
    plot_perf(winrates)

# ----- main -----
train()