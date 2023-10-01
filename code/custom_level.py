#### IMPORTS
import pygame, sys 
from pygame.math import Vector2 as vector

from settings import *
from support import *
from sprites import Generic, Player

class CustomLevel:
    def __init__(self, level_grid, switch, asset_dictionary):
        self.level_display_surface = pygame.display.get_surface()
        self.switch = switch

        ## Objects/Sprites: Player, Trees
        self.all_sprites = pygame.sprite.Group()

        self.build_level(level_grid, asset_dictionary)

    def build_level(self, level_grid, asset_dictionary):
        for layer_name, layer in level_grid.items():
            for pos, data in layer.items():
                if layer_name == 'terrain':
                    Generic(pos, asset_dictionary['land'][data],self.all_sprites)
                
                match data:
                    case 0: # player
                        self.player = Player(pos, self.all_sprites)
                    case 1: # sky
                        pass
                    case 4: # gold coin
                        pass

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.switch()   
    def run(self, dt):
        self.event_loop()
        self.level_display_surface.fill(SKY_COLOR)
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.level_display_surface)