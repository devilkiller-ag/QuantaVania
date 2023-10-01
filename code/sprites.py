#### IMPORTS
import pygame, sys 
from pygame.math import Vector2 as vector

from settings import *

class Generic(pygame.sprite.Sprite):
    def __init__(self, position, surface, group):
        super().__init__(group)
        self.image = surface
        self.rect = self.image.get_rect(topleft = position)

## Smple Invisible Collidible Block to be place over shells, foreground tree tops (putting over tree tops so that user can only collide with Tree top and not to the tree trunk)
class CollidableBlock(Generic):
    def __init__(self, position, size, group):
        surface = pygame.Surface(size)
        super().__init__(position, surface, group)

## Simple Animated Sprites
class AnimatedSprite(Generic):
    def __init__(self, assets, position, group):
        self.animation_frames = assets
        self.frame_index = 0
        super().__init__(position, self.animation_frames[self.frame_index], group)

    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt
        if self.frame_index >= len(self.animation_frames):
            self.frame_index = 0
        self.image = self.animation_frames[int(self.frame_index)]

    def update(self, dt):
        self.animate(dt)

class ParticleEffect(AnimatedSprite):
    def __init__(self, assets, position, group):
        super().__init__(assets, position, group)
        self.rect = self.image.get_rect(center = position)
    
    def animate(self, dt): # Animate only once (not forever)
        self.frame_index += ANIMATION_SPEED * dt
        if(self.frame_index < len(self.animation_frames)):
            self.image = self.animation_frames[int(self.frame_index)]
        else:
            self.kill() # destroy the particle effect after one animation

class Coin(AnimatedSprite):
    def __init__(self, coin_type, assets, position, group):
        super().__init__(assets, position, group)
        self.rect = self.image.get_rect(center = position)
        self.coin_type = coin_type

## Enemies
class Spikes(Generic):
    def __init__(self, surface, position, group):
        super().__init__(position, surface, group)

class CrabMonster(Generic):
    def __init__(self, assets, position, group):
        self.animation_frames = assets
        self.frame_index = 0
        self.orientation = 'right'
        surface = self.animation_frames[f'run_{self.orientation}'][self.frame_index]
        super().__init__(position, surface, group)
        self.rect.bottom = self.rect.top + TILE_SIZE

class Shell(Generic):
    def __init__(self, orientation, assets, position, group):
        self.orientation = orientation

        self.animation_frames = assets.copy() # Making a copy because we will just flip the graphics of shell_left to get the graphics of shell_right (Making a copy will ensure it's not fliping the original imported assets)
        if(orientation == 'right'):
            for key, value in self.animation_frames.items():
                self.animation_frames[key] = [pygame.transform.flip(surface, True, False) for surface in value]
        
        self.frame_index = 0
        self.status = 'idle'
        surface = self.animation_frames[self.status][self.frame_index]
        super().__init__(position, surface, group)
        self.rect.bottom = self.rect.top + TILE_SIZE

## Player
class Player(Generic):
    def __init__(self, position, group, collision_sprites):
        super().__init__(position, pygame.Surface((80, 64)), group)
        self.image.fill('red')

        ## Movement
        self.direction = vector()
        self.position = vector(self.rect.center)
        self.speed = PLAYER_SPEED
        self.gravity = GRAVITY
        self.on_floor = False

        ## Collision
        self.collision_sprites = collision_sprites
        self.hitbox = self.rect.inflate(-50, 0) ## Hit & Trail Value
    
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.on_floor:
            self.direction.y = -2

    def move(self, dt):
        ## Horizontal Movement
        self.position.x += self.direction.x * self.speed * dt
        # Making x position of center of hitbox and player rect same
        self.hitbox.centerx = round(self.position.x)
        self.rect.centerx = (self.hitbox.centerx)
        self.collision('horizontal')

        ## Vertical Movement
        self.position.y += self.direction.y * self.speed * dt
        # Making y position of center of hitbox and player rect same
        self.hitbox.centery = round(self.position.y)
        self.rect.centery = (self.hitbox.centery)
        self.collision('vertical')

    def apply_gravity(self, dt):
        self.direction.y += self.gravity * dt
        self.rect.y += self.gravity

    def check_on_floor(self):
        floor_rect = pygame.Rect(self.hitbox.bottomleft, (self.hitbox.width, 2)) # Create a virtual floor below the player hitbox
        floor_sprites = [sprite for sprite in self.collision_sprites if sprite.rect.colliderect(floor_rect)]
        self.on_floor = True if floor_sprites else False


    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox):
                if direction == 'horizontal':
                    if self.direction.x > 0: # player moving towards right
                        self.hitbox.right = sprite.rect.left
                    if self.direction.x < 0: # player moving towards left
                        self.hitbox.left = sprite.rect.right
                    self.rect.centerx = self.hitbox.centerx
                    self.position.x = self.hitbox.centerx
                else: # direction == 'vertical
                    if self.direction.y < 0: # player moving towards top
                        self.hitbox.top = sprite.rect.bottom
                    if self.direction.y > 0: # player moving towards bottom
                        self.hitbox.bottom = sprite.rect.top
                    self.rect.centery = self.hitbox.centery
                    self.position.y = self.hitbox.centery
                    self.direction.y = 0 # Reset player vertical speed (and hence the gravity)


    def update(self, dt):
        self.input()
        self.apply_gravity(dt)
        self.move(dt)
        self.check_on_floor()