import numpy as np
import matplotlib.pyplot as plt

import Backgammon
from Backgammon import *
import kotra
import randomAgent
import time

def plot_perf(performance):
    plt.plot(performance)
    plt.show()
    return

def evaluate(agent, evaluation_agent, n_eval, n_games):
    wins = 0
    for i in range(n_eval):
        winner, board = Backgammon.play_a_game(agent, evaluation_agent)
        wins += int(winner==1)
    winrate = round(wins/n_eval*100,3)
    print("Win-rate after training for "+str(n_games)+" games: "+str(winrate)+"%" )
    return winrate

def train(n_games=1000, n_epochs=199, n_eval=50, show=False):
    agent = kotra
    evaluation_agent = randomAgent
    pygame.quit()
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

        winner, board = Backgammon.play_a_game(agent, agent, train=True, train_config={'g':g})
        agent.game_over_update(board, int(winner==1))
        agent.game_over_update(kotra.flip_board(board), int(winner==-1))

    runTime = time.time() - startTime
    print("runTime:", runTime)
    print("average time:", runTime / n_games)
    plot_perf(winrates)

# ----- main -----
train()