import pygame
import pygame_menu
from pygame_menu import Theme
import numpy as np

import math


def window_init():

    pygame.init()
    pygame.font.init()
    pygame.display.init()
    pygame.font.SysFont('Arial', 30)
    return pygame.display.set_mode((400, 600))

def set_player():
    pass
def start_the_game():
    #eventloop()
    pass
def get_sim_no(value: str) -> None:
    """
    This function tests the text input widget.
    :param value: The widget value
    :return: None
    """
    no = '{0}'.format(value)
    print("Number of Simulations: {0}".format(value))
    try:
        no = int(no)
    except:
        print("Invalid user input. Number of Simulations must be an integer.")
        print("Default used: 100")
        no = 100
    return no

def eventloop():
    # Event loop
    x = np.nan
    y = np.nan
    continue_loop = True
    click_event_counter = 0
    while continue_loop:
        for event in pygame.event.get():


            #if event.type == pygame.QUIT:
            #    continue_loop = False


            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                # Only if left mouse key is pressed, the input is considered valid
                if mouse_presses[0]:
                    click_event_counter += 1
                    print(click_event_counter)
                    print("Left Mouse key was clicked")
                    x, y = pygame.mouse.get_pos()
                    print("Position of mousebuttons", x, y)
                    #continue_loop = False
                    #pygame.quit()
                    return x, y
                elif mouse_presses[0] == False:
                    print("Please left-click on a field.")
   #pygame.quit()


def menu():
    """
    THEME_PLAKOTO = Theme(
        background_color=(40, 41, 35),
        cursor_color=(255, 255, 255),
        cursor_selection_color=(80, 80, 80),
        scrollbar_color=(39, 41, 42),
        scrollbar_slider_color=(65, 66, 67),
        selection_color=(255, 255, 255),
        title_background_color=(139, 0, 0),
        title_font_color=(215, 215, 215),
        widget_font_color=(200, 200, 200),
    )"""


    surface = window_init()
    menu = pygame_menu.Menu('test', 400, 600,
                            theme=pygame_menu.themes.THEME_DARK)
    # default values for players

    # menu.add.text_input('Name :', default='THM Student')
    menu.add.selector('Player 1 :', [('Random Agent', 1, 1), ('PS-AI', 2, 1), ('User', 3, 1)], onchange=set_player)
    menu.add.selector('Player 2 :', [('Random Agent', 1, 2), ('PS-AI', 2, 2), ('User', 3, 2)], onchange=set_player)

    # menu.add.button('Play', quit_menu(menu))

    menu.add.button('Play', start_the_game)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    menu.add.text_input('No. Simulations: ', default='100', maxchar=10, onreturn = get_sim_no)


    menu.mainloop(surface)


if __name__ == '__main__':
    #main(user=True, show=True)
    menu()