#### IMPORTS
import pygame, sys 
from pygame.math import Vector2 as vector

from settings import *
from support import *

class CustomLevel:
    def __init__(self, grid, switch):
        self.level_display_surface = pygame.display.get_surface()
        self.switch = switch

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.switch()   
    def run(self, dt):
        self.event_loop()
        self.level_display_surface.fill('red')