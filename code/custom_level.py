#### IMPORTS
import pygame, sys 
from pygame.math import Vector2 as vector

from settings import *
from support import *
from sprites import Generic, AnimatedSprite, ParticleEffect, Coin, Player

class CustomLevel:
    def __init__(self, level_grid, switch, asset_dictionary):
        self.level_display_surface = pygame.display.get_surface()
        self.switch = switch

        ## Objects/Sprites: Player, Trees
        self.all_sprites = pygame.sprite.Group()
        self.coin_sprites = pygame.sprite.Group()
        
        self.build_level(level_grid, asset_dictionary)

        ## Additional Stuffs
        self.particles_surfaces = asset_dictionary['particles']

    def build_level(self, level_grid, asset_dictionary):
        for layer_name, layer in level_grid.items():
            for pos, data in layer.items():
                if layer_name == 'terrain':
                    Generic(pos, asset_dictionary['land'][data],self.all_sprites)
                
                if layer_name == 'water':
                    if data == 'top':
                        # animated sprite
                        AnimatedSprite(asset_dictionary['water top'], pos, self.all_sprites)
                    else:
                        # plain water (not animated)
                        Generic(pos, asset_dictionary['water bottom'], self.all_sprites)
                
                match data:
                    case 0: # player
                        self.player = Player(pos, self.all_sprites)
                    case 1: # sky
                        pass
                    case 4: # gold coin
                        Coin('gold' , asset_dictionary['gold'], pos, [self.all_sprites, self.coin_sprites])
                    case 5: # silver coin
                        Coin('silver' , asset_dictionary['silver'], pos, [self.all_sprites, self.coin_sprites])
                    case 6: # diamond coin
                        Coin('diamond' , asset_dictionary['diamond'], pos, [self.all_sprites, self.coin_sprites])

    def get_coins(self):
        collided_coins = pygame.sprite.spritecollide(self.player, self.coin_sprites, True) # spritecolide(sprite, group, dokill)
        for sprite in collided_coins:
            ParticleEffect(self.particles_surfaces, sprite.rect.center, self.all_sprites)

            ## Increase Player Score (Or do diffrent things) according to the type of coin/qubit player collided with
            if sprite.coin_type == 'gold':
                print('gold')
            if sprite.coin_type == 'silver':
                print('silver')
            if sprite.coin_type == 'diamond':
                print('diamond')


    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.switch() 
    
    def run(self, dt):
        ## update
        self.event_loop()
        self.all_sprites.update(dt)
        self.get_coins()

        ## draw
        self.level_display_surface.fill(SKY_COLOR)
        self.all_sprites.draw(self.level_display_surface)