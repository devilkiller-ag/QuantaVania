#### IMPORTS
import pygame, sys 
from pygame.math import Vector2 as vector

from settings import *

class Generic(pygame.sprite.Sprite):
    def __init__(self, position, surface, group):
        super().__init__(group)
        self.image = surface
        self.rect = self.image.get_rect(topleft = position)

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

class Player(Generic):
    def __init__(self, position, group):
        super().__init__(position, pygame.Surface((32, 64)), group)
        self.image.fill('red')

        ## Movement
        self.direction = vector()
        self.position = vector(self.rect.topleft)
        self.speed = PLAYER_SPEED
    
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1

        else:
            self.direction.x = 0

    def move(self, dt):
        self.position += self.direction * self.speed * dt
        self.rect.topleft = (round(self.position.x), round(self.position.y))

    def update(self, dt):
        self.input()
        self.move(dt)