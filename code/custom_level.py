#### IMPORTS
import pygame, sys 
from pygame.math import Vector2 as vector
from random import choice, randint
from pygame.image import load as loadImage

from settings import *
from support import *
from sprites import Generic, CollidableBlock, Cloud, AnimatedSprite, ParticleEffect, Coin, Spikes, CrabMonster, Shell, Player

class CustomLevel:
    def __init__(self, current_level, new_max_level, level_grid, switch, create_overworld, asset_dictionary, audio):
        self.level_display_surface = pygame.display.get_surface()
        self.switch = switch
        self.level_grid = level_grid

        ## Objects/Sprites: Player, Trees
        self.all_sprites = CameraGroup()
        self.coin_sprites = pygame.sprite.Group()
        self.damage_sprites = pygame.sprite.Group() ## Sprites of Enemies which will cause damage to player
        self.collision_sprites = pygame.sprite.Group()
        self.shell_sprites = pygame.sprite.Group()
        self.bg_lvl1 = loadImage("graphics/background/1.png")

        self.build_level(level_grid, asset_dictionary, audio['jump'])

        ## Level Limits
        self.level_limits = {
            'left': -WINDOW_WIDTH,
            'right': (sorted(list(self.level_grid['terrain'].keys()), key = lambda pos: pos[0])[-1])[0] + 500 if level_grid['terrain'] else 1800 # x of rightmost terrain tile + offset(500)
        }

        ## Additional Stuffs
        self.particles_surfaces = asset_dictionary['particles']
        self.cloud_surfaces = asset_dictionary['clouds']
        self.cloud_timer = pygame.USEREVENT + 2
        pygame.time.set_timer(self.cloud_timer, 2000)
        self.startup_clouds()

        ## Sounds
        self.bg_music = audio['music']
        self.bg_music.set_volume(0.3)
        self.bg_music.play(loops = -1)

        self.coin_sound = audio['coin']
        self.coin_sound.set_volume(0.2)

        self.hit_sound = audio['hit']
        self.hit_sound.set_volume(0.3)

        ## Overworld
        self.create_overworld = create_overworld
        self.current_level = current_level
        self.new_max_level = new_max_level

    def build_level(self, level_grid, asset_dictionary, jump_sound):
        for layer_name, layer in level_grid.items():
            for pos, data in layer.items():
                if layer_name == 'terrain':
                    Generic(pos, asset_dictionary['land'][data], [self.all_sprites, self.collision_sprites])
                
                if layer_name == 'water':
                    if data == 'top':  
                        # animated sprite
                        AnimatedSprite(asset_dictionary['water top'], pos, self.all_sprites, LEVEL_LAYERS['water'])
                    else:
                        # plain water (not animated)
                        Generic(pos, asset_dictionary['water bottom'], self.all_sprites, LEVEL_LAYERS['water'])
                
                match data:
                    case 0: # player
                        self.player = Player(pos, asset_dictionary['player'], self.all_sprites, self.collision_sprites, jump_sound)
                    case 1: # sky
                        self.horizon_y = pos[1]
                        self.all_sprites.horizon_y = pos[1]

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
                        CrabMonster(asset_dictionary['crab_monster'], pos, [self.all_sprites, self.damage_sprites], self.collision_sprites)
                    case 9: # Shell pointing left
                        Shell(
                            orientation = 'left', 
                            assets = asset_dictionary['shell'], 
                            position = pos, 
                            group = [self.all_sprites, self.collision_sprites, self.shell_sprites], 
                            pearl_surface = asset_dictionary['pearl'],
                            damage_sprites = self.damage_sprites
                        )
                    case 10: # Shell pointing right
                        Shell(
                            orientation = 'right', 
                            assets = asset_dictionary['shell'], 
                            position = pos, 
                            group = [self.all_sprites, self.collision_sprites, self.shell_sprites], 
                            pearl_surface = asset_dictionary['pearl'],
                            damage_sprites = self.damage_sprites
                        )
                    # (ii) They need to know where the player is

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
                        AnimatedSprite(asset_dictionary['palms']['small_bg'], pos, self.all_sprites, LEVEL_LAYERS['bg'])
                    case 16: # large palm bg
                        AnimatedSprite(asset_dictionary['palms']['large_bg'], pos, self.all_sprites, LEVEL_LAYERS['bg'])
                    case 17: # left palm bg
                        AnimatedSprite(asset_dictionary['palms']['left_bg'], pos, self.all_sprites, LEVEL_LAYERS['bg'])
                    case 18: # right palm bg
                        AnimatedSprite(asset_dictionary['palms']['right_bg'], pos, self.all_sprites, LEVEL_LAYERS['bg'])
            
        for sprite in self.shell_sprites:
            sprite.player = self.player

    def create_cloud(self):
        ## Create New Clouds on the right side of window
        cloud_surface = choice(self.cloud_surfaces) # randomly select a cloud from all types of cloud surfaces available
        cloud_surface = pygame.transform.scale2x(cloud_surface) if randint(0, 5) > 3 else cloud_surface # scale this cloud surfaces by 2x randomly
        x = self.level_limits['right'] + randint(100, 300)
        y = self.horizon_y - randint(-50, 600)
        Cloud((x, y), cloud_surface, self.all_sprites, self.level_limits['left'])

    def startup_clouds(self): # To have some clouds initially as we start the editor
        for counter in range(20):
            cloud_surface = choice(self.cloud_surfaces) # randomly select a cloud from all types of cloud surfaces available
            cloud_surface = pygame.transform.scale2x(cloud_surface) if randint(0, 4) < 2 else cloud_surface # scale this cloud surfaces by 2x randomly
            x = randint(self.level_limits['left'], self.level_limits['right'])
            y = self.horizon_y - randint(-50, 600)
            Cloud((x, y), cloud_surface, self.all_sprites, self.level_limits['left'])

    def get_coins(self):
        collided_coins = pygame.sprite.spritecollide(self.player, self.coin_sprites, True) # spritecolide(sprite, group, dokill)
        for sprite in collided_coins:
            self.coin_sound.play()
            ParticleEffect(self.particles_surfaces, sprite.rect.center, self.all_sprites)

            ## Increase Player Score (Or do diffrent things) according to the type of coin/qubit player collided with
            if sprite.coin_type == 'gold':
                print('gold')
            if sprite.coin_type == 'silver':
                print('silver')
            if sprite.coin_type == 'diamond':
                print('diamond')

    def get_damage(self):
        collision_sprites = pygame.sprite.spritecollide(self.player, self.damage_sprites, False, pygame.sprite.collide_mask)
        if collision_sprites:
            self.hit_sound.play()
            self.player.damage()

    def check_death(self):
        if self.player.position.y > WINDOW_HEIGHT:
            self.bg_music.stop()
            self.create_overworld(self.current_level, 0)
			
    def check_win(self):
        if self.player.position.x >= (sorted(list(self.level_grid['terrain'].keys()), key = lambda pos: pos[0])[-1])[0] - 100:
            self.bg_music.stop()
            self.create_overworld(self.current_level, self.new_max_level)

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.bg_music.stop()
                # self.switch()
                self.create_overworld(2, 3)
            
            if event.type == self.cloud_timer:
                self.create_cloud()
    
    def run(self, dt):
        ## update
        self.event_loop()
        self.all_sprites.update(dt)
        self.get_coins()
        self.get_damage()
        self.check_death()
        self.check_win()

        ## draw
        self.level_display_surface.fill(SKY_COLOR)
        size = pygame.transform.scale(self.bg_lvl1,(1280,720))
        self.level_display_surface.blit(size,(0,0))
        self.all_sprites.custom_draw(self.player)

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = vector()
    
    def draw_horizon(self):
        horizon_position = self.horizon_y - self.offset.y
        
        if horizon_position < 0:
            self.display_surface.fill(SEA_COLOR)

        if horizon_position < WINDOW_HEIGHT:
            # Sea
            sea_rect = pygame.Rect(0, horizon_position, WINDOW_WIDTH, WINDOW_HEIGHT - horizon_position)
            pygame.draw.rect(self.display_surface, SEA_COLOR, sea_rect)
        
            # Horizon Lines
            horizon_rect_1 = pygame.Rect(0, horizon_position - 10, WINDOW_WIDTH, 10)
            horizon_rect_2 = pygame.Rect(0, horizon_position - 16, WINDOW_WIDTH, 4)
            horizon_rect_3 = pygame.Rect(0, horizon_position - 20, WINDOW_WIDTH, 2)
            pygame.draw.rect(self.display_surface, HORIZON_TOP_COLOR, horizon_rect_1)
            pygame.draw.rect(self.display_surface, HORIZON_TOP_COLOR, horizon_rect_2)
            pygame.draw.rect(self.display_surface, HORIZON_TOP_COLOR, horizon_rect_3)
            pygame.draw.line(self.display_surface, HORIZON_COLOR, (0, horizon_position), (WINDOW_WIDTH, horizon_position), 3)

    def custom_draw(self, player):
        ## offset should be relative to player
        self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2

        ## Draw Clouds
        for sprite in self:
            if sprite.z_index == LEVEL_LAYERS['clouds']:
                offset_rect = sprite.rect.copy()
                offset_rect.center -= self.offset
               # self.display_surface.blit(sprite.image, offset_rect)

        ## Draw Horizon
       # self.draw_horizon()

        ## Draw everything except clouds
        for sprite in self:
            ## Drawing everything according to their z-index
            for layer in LEVEL_LAYERS.values():
                if sprite.z_index == layer and sprite.z_index != LEVEL_LAYERS['clouds']:
                    ## draw everything relative to the player
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)
