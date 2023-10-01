#### IMPORTS
import pygame, sys 
from pygame.math import Vector2 as vector

from settings import *
from support import *
from sprites import Generic, CollidableBlock, AnimatedSprite, ParticleEffect, Coin, Spikes, CrabMonster, Shell, Player

class CustomLevel:
    def __init__(self, level_grid, switch, asset_dictionary):
        self.level_display_surface = pygame.display.get_surface()
        self.switch = switch

        ## Objects/Sprites: Player, Trees
        self.all_sprites = pygame.sprite.Group()
        self.coin_sprites = pygame.sprite.Group()
        self.damage_sprites = pygame.sprite.Group() ## Sprites of Enemies which will cause damage to player
        self.collision_sprites = pygame.sprite.Group()
        
        self.build_level(level_grid, asset_dictionary)

        ## Additional Stuffs
        self.particles_surfaces = asset_dictionary['particles']

    def build_level(self, level_grid, asset_dictionary):
        for layer_name, layer in level_grid.items():
            for pos, data in layer.items():
                if layer_name == 'terrain':
                    Generic(pos, asset_dictionary['land'][data], [self.all_sprites, self.collision_sprites])
                
                if layer_name == 'water':
                    if data == 'top':  
                        # animated sprite
                        AnimatedSprite(asset_dictionary['water top'], pos, self.all_sprites)
                    else:
                        # plain water (not animated)
                        Generic(pos, asset_dictionary['water bottom'], self.all_sprites)
                
                match data:
                    case 0: # player
                        self.player = Player(pos, asset_dictionary['player'], self.all_sprites, self.collision_sprites)
                    case 1: # sky
                        pass

                    ## Coins
                    case 4: # gold coin
                        Coin('gold' , asset_dictionary['gold'], pos, [self.all_sprites, self.coin_sprites])
                    case 5: # silver coin
                        Coin('silver' , asset_dictionary['silver'], pos, [self.all_sprites, self.coin_sprites])
                    case 6: # diamond coin
                        Coin('diamond' , asset_dictionary['diamond'], pos, [self.all_sprites, self.coin_sprites])
                    
                    ## Enemies
                    case 7: # Spikes
                        Spikes(asset_dictionary['spikes'], pos, [self.all_sprites, self.damage_sprites])
                    case 8: # CrabMonster
                        print(asset_dictionary['crab_monster']['idle'])
                        CrabMonster(asset_dictionary['crab_monster'], pos, [self.all_sprites, self.damage_sprites])
                    case 9: # Shell pointing left
                        Shell('left', asset_dictionary['shell'], pos, [self.all_sprites, self.collision_sprites])
                    case 10: # Shell pointing right
                        Shell('right', asset_dictionary['shell'], pos, [self.all_sprites, self.collision_sprites])

                    ## Foreground Palm Trees
                    case 11: # small palm fg
                        AnimatedSprite(asset_dictionary['palms']['small_fg'], pos, self.all_sprites)
                        CollidableBlock(pos, (76, 50), [self.collision_sprites]) # Invisible because CollidableBlock is not added to to self.all_sprites and CollidableBlock iself do not have any draw method which can be called through self.collision_sprites
                    case 12: # large palm fg
                        AnimatedSprite(asset_dictionary['palms']['large_fg'], pos, self.all_sprites)
                        CollidableBlock(pos, (76, 50), [self.collision_sprites]) ## Hit & Trail Values
                    case 13: # left palm fg
                        AnimatedSprite(asset_dictionary['palms']['left_fg'], pos, self.all_sprites)
                        CollidableBlock(pos, (76, 50), [self.collision_sprites])
                    case 14: # right palm fg
                        AnimatedSprite(asset_dictionary['palms']['right_fg'], pos, self.all_sprites)
                        CollidableBlock(pos + vector(50, 0), (76, 50), [self.collision_sprites])

                    ## Background Palm Trees
                    case 15: # small palm bg
                        AnimatedSprite(asset_dictionary['palms']['small_bg'], pos, self.all_sprites)
                    case 16: # large palm bg
                        AnimatedSprite(asset_dictionary['palms']['large_bg'], pos, self.all_sprites)
                    case 17: # left palm bg
                        AnimatedSprite(asset_dictionary['palms']['left_bg'], pos, self.all_sprites)
                    case 18: # right palm bg
                        AnimatedSprite(asset_dictionary['palms']['right_bg'], pos, self.all_sprites)

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