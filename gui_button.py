# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 19:40:26 2021

@author: Stephanie Kaes


Source: https://pythonprogramming.altervista.org/buttons-in-pygame/#:~:text=%20How%20to%20make%20a%20button%20in%20pygame%3A,butto%20%28when%20you%20click%20for%20example%29%20More%20
"""
import pygame
import time

#pygame.init()
#screen = pygame.display.set_mode((500, 600))
#clock = pygame.time.Clock()
#font = pygame.font.SysFont("Arial", 20)

class Button:
    """Create a button, then blit the surface in the while loop"""
 
    def __init__(self, gui, text,  pos, font, bg="black", feedback=""):
        self.gui = gui
        self.x, self.y = pos
        self.font = pygame.font.SysFont("Arial", font)
        if feedback == "":
            self.feedback = "text"
        else:
            self.feedback = feedback
        self.change_text(text, bg)
 
    def change_text(self, text, bg="black"):
        """Change the text whe you click"""
        self.text = self.font.render(text, 1, pygame.Color("White"))
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
 
    def show(self, button, gui):
        self.gui.screen.blit(button.surface, (self.x, self.y))
 
    def click(self, clock, event):
        x, y = pygame.mouse.get_pos()        
        if pygame.mouse.get_pressed()[0]:
            if self.rect.collidepoint(x, y):
                self.change_text(self.feedback, bg="red")
                
  

def mainloop(clock, gui):
    """ The infinite loop where things happen """
    loop = True
    clickcount = 0
    while loop:
        for event in pygame.event.get():
            print(clickcount)
            
            if event.type == pygame.QUIT:
                pygame.quit()
                        
            if clickcount >=1:
                loop = False
                break

        clock.tick(30)
        pygame.display.update()
 