"""
Created on Fri Jul  9 18:08:26 2021

@author: Stephanie Kaes, Paul K. Christof
"""

"""
Plakoto interface
Run this program to play a game of Backgammon
The agent is stored in another file 
Most (if not all) of your agent-develeping code should be written in the agent.py file
Feel free to change this file as you wish but you will only submit your agent 
so make sure your changes here won't affect his performance.
"""

import pygame
import pygame_menu
import time
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import Plakoto_game as bg
import classGUI
import randomAgent
import userAgent
import psai

def start_game():
    print("starting game")
    agent_play_1 = randomAgent
    agent_play_2 = randomAgent

    if player1 == 'userAgent':
        agent_play_1 = userAgent
    if player1 == 'AI (64_64_32_1_tanh_1200k)':
        agent_play_1 = psai
        agent_play_1.loadModel('64_32_1_tanh_sig')
    if player1 == 'AI (64_32_1_relu_1700k)':
        agent_play_1 = psai
        agent_play_1.loadModel('64_32_1_relu_1700k')
    if player1 == 'AI (64_32_1_relu_2000k)':
        agent_play_1 = psai
        agent_play_1.loadModel('64_32_1_relu_2000k')
    if player1 == 'AI (64_32_1_relu_700k)':
        agent_play_1 = psai
        agent_play_1.loadModel('64_32_1_relu_700k')
    if player1 == 'AI (16_8_8_8_4_4_1_relu_700k)':
        agent_play_1 = psai
        agent_play_1.loadModel('16_8_8_8_4_4_1_relu_700k')
    if player1 == 'AI (128_1_tanh1200k)':
        agent_play_1 = psai
        agent_play_1.loadModel('128_1_tanh')

    if player1 == 'randomAgent':
        agent_play_1 = randomAgent

    if player2 == 'userAgent':
        agent_play_2 = userAgent
    if player2 == 'AI (64_64_32_1_tanh_1200k)':
        agent_play_2 = psai
        agent_play_2.loadModel('64_32_1_tanh_sig')
    if player2 == 'AI (64_32_1_relu_1700k)':
        agent_play_2 = psai
        agent_play_2.loadModel('64_32_1_relu_1700k')
    if player2 == 'AI (64_32_1_relu_2000k)':
        agent_play_2 = psai
        agent_play_2.loadModel('64_32_1_relu_2000k')
    if player2 == 'AI (64_32_1_relu_700k)':
        agent_play_2 = psai
        agent_play_2.loadModel('64_32_1_relu_700k')
    if player2 == 'AI (16_8_8_8_4_4_1_relu_700k)':
        agent_play_2 = psai
        agent_play_2.loadModel('16_8_8_8_4_4_1_relu_700k')
    if player2 == 'AI (128_1_tanh_1200k)':
        agent_play_2 = psai
        agent_play_2.loadModel('128_1_tanh_1200k')
    if player2 == 'randomAgent':
        agent_play_2 = randomAgent

    if player1 == 'userAgent' or player2 == 'userAgent':
        print("starting game using user agent")
        winner, board = bg.play_a_game(agent_play_1, agent_play_2, user=True, show = True)
        print("Winner: ", winner)
    else:
        print("starting game without any user agent")
        winner, board = bg.play_a_game(agent_play_1, agent_play_2, user=False, show = True)
        
        print("Winner: ", winner)
    menu.mainloop(gui.screenMenu)

def set_sim_results(score1 = 0, score2 = 0, draw = 0):
    global menu


    score1, score2, draw = simulate()
    menu.add.label("\n ", font_size=24)
    menu.add.label("Simulation results ", font_size=24)
    menu.add.label("Score Player1: " + str(score1),  font_size=20)
    menu.add.label("Score Player2: " + str(score2),  font_size=20)
    menu.add.label("Draw: " + str(draw), font_size=20)
    pygame.display.update()

simNumber = 100
def simulate():
    agent_play_1 = randomAgent
    agent_play_2 = randomAgent

    if player1 == 'userAgent':
        return

    if player1 == 'AI (64_64_32_1_tanh_1200k)':
        agent_play_1 = psai
        agent_play_1.loadModel('64_32_1_tanh_sig')
    if player1 == 'AI (64_32_1_relu_1700k)':
        agent_play_1 = psai
        agent_play_1.loadModel('64_32_1_relu_1700k')
    if player1 == 'AI (64_32_1_relu_2000k)':
        agent_play_1 = psai
        agent_play_1.loadModel('64_32_1_relu_2000k')
    if player1 == 'AI (64_32_1_relu_700k)':
        agent_play_1 = psai
        agent_play_1.loadModel('64_32_1_relu_700k')
    if player1 == 'AI (16_8_8_8_4_4_1_relu_700k)':
        agent_play_1 = psai
        agent_play_1.loadModel('16_8_8_8_4_4_1_relu_700k')
    if player1 == 'AI (128_1_tanh1200k)':
        agent_play_1 = psai
        agent_play_1.loadModel('128_1_tanh')

    if player1 == 'randomAgent':
        agent_play_1 = randomAgent

    if player2 == 'userAgent':
        return
    if player2 == 'AI (64_64_32_1_tanh_1200k)':
        agent_play_2 = psai
        agent_play_2.loadModel('64_32_1_tanh_sig')
    if player2 == 'AI (64_32_1_relu_1700k)':
        agent_play_2 = psai
        agent_play_2.loadModel('64_32_1_relu_1700k')
    if player2 == 'AI (64_32_1_relu_2000k)':
        agent_play_2 = psai
        agent_play_2.loadModel('64_32_1_relu_2000k')
    if player2 == 'AI (64_32_1_relu_700k)':
        agent_play_2 = psai
        agent_play_2.loadModel('64_32_1_relu_700k')
    if player2 == 'AI (16_8_8_8_4_4_1_relu_700k)':
        agent_play_2 = psai
        agent_play_2.loadModel('16_8_8_8_4_4_1_relu_700k')
    if player2 == 'AI (128_1_tanh_1200k)':
        agent_play_2 = psai
        agent_play_2.loadModel('128_1_tanh')
    if player2 == 'randomAgent':
        agent_play_2 = randomAgent

# marked code snipped copied and edited from https://github.com/weekend37/Backgammon
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    startTime = time.time()
    winners = {}
    winners["1"] = 0
    winners["-1"] = 0
    winners["0"] = 0  # Collecting stats of the games

    performance = list()

    print("Playing " + str(simNumber) + " between" + str(player1) + "1 and " + str(player2) + "-1")

    wins = 0
    nEpochs = 1_000
    for g in range(simNumber):

        print("playing game number: " + str(g))
        if g % nEpochs == 0:
            performance = bg.log_status(g, wins, performance, nEpochs)
            wins = 0

        winner, board = bg.play_a_game(agent_play_1, agent_play_2, user=False, show=False)  # g, commentary=False)
        winners[str(winner)] += 1
        wins += (bg.winner == 1)

    print("Out of", simNumber, "games,")
    print("player", 1, "won", winners["1"], "times and")
    print("player", -1, "won", winners["-1"], "times and")
    print(winners["0"], " games were a draw")
    runTime = time.time() - startTime
    print("runTime:", runTime)
    print("average time:", runTime / simNumber)
    bg.plot_perf(performance)

    return(winners["1"],  winners["-1"], winners["0"])
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


def get_sim_no(value: str):
    """
    This function returns the text input widget (number of simulations).
    :param value: The widget value
    :return: int
    """
    global simNumber
    no = '{0}'.format(value)
    print("Number of Simulations: {0}".format(value))
    try:
        no = int(no)
    except:
        print("Invalid user input. Number of Simulations must be an integer.")
        print("Default used: 100")
        no = 100
    simNumber = no


def set_player(value, playerno):
    """
    Changes player according to user input on menu.
    """
    print("value: ", value)
    print("playerno: ", playerno)

    global player1
    global player2

    if playerno == 1:
        player1 = value[0][0]
    else:
        player2 = value[0][0]


player1 = 'randomAgent'
player2 = 'randomAgent'

gui = classGUI.Gui()

menu = pygame_menu.Menu('Backgammon Plakoto', gui.width, gui.height,
                            theme=pygame_menu.themes.THEME_DARK)


def main(user=False, show=False):
    global player1
    global player2
    global menu
    pygame.init()
    pygame.display.init()
    clock = pygame.time.Clock()

    # mainloop(clock, gui)
    # ----------------------
    if not show: gui.screen = pygame.quit()

    menu.add.selector('Player 1 :', [('randomAgent', 1), ('AI (64_32_1_relu_700k)', 1),('AI (64_32_1_relu_1700k)', 1),('AI (64_32_1_relu_2000k)', 1), ('AI (128_1_tanh_1200k)', 1), ('AI (64_64_32_1_tanh_1200k)', 1), ('AI (16_8_8_8_4_4_1_relu_700k)', 1), ('userAgent', 1)], onchange=set_player)
    menu.add.selector('Player 2 :', [('randomAgent', 2), ('AI (64_32_1_relu_700k)', 2),('AI (64_32_1_relu_1700k)', 2),('AI (64_32_1_relu_2000k)', 2), ('AI (128_1_tanh_1200k)', 2), ('AI (64_64_32_1_tanh_1200k)', 2), ('AI (16_8_8_8_4_4_1_relu_700k)', 2), ('userAgent', 2)], onchange=set_player)
    menu.add.button('Play', start_game)
    menu.add.button('Simulate', set_sim_results)
    menu.add.text_input('No. Simulations: ', default='100', maxchar=10, onreturn=get_sim_no)
    menu.add.label("\n ", font_size=10)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.add.label("by Paul K. Christof & Stephanie Käs", font_size=10)

    menu.mainloop(gui.screenMenu)


if __name__ == '__main__':
    main(user=True, show=True)
