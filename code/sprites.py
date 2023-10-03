#### IMPORTS
import pygame, sys 
from pygame.math import Vector2 as vector
from random import choice, randint

from settings import *
from timer import Timer

class Generic(pygame.sprite.Sprite):
    def __init__(self, position, surface, group, z_index = LEVEL_LAYERS['main']):
        super().__init__(group)
        self.image = surface
        self.rect = self.image.get_rect(topleft = position)
        self.z_index = z_index

## Smple Invisible Collidible Block to be place over shells, foreground tree tops (putting over tree tops so that user can only collide with Tree top and not to the tree trunk)
class CollidableBlock(Generic):
    def __init__(self, position, size, group):
        surface = pygame.Surface(size)
        super().__init__(position, surface, group)

## Cloud
class Cloud(Generic):
    def __init__(self, position, surface, group, left_limit):
        super().__init__(position, surface, group, LEVEL_LAYERS['clouds'])
        self.left_limit = left_limit

        # Movement
        self.position = vector(self.rect.topleft)
        self.speed = randint(20, 30)
    
    def update(self, dt):
        self.position.x -= self.speed * dt
        self.rect.x = self.position.x

        if self.rect.x <= self.left_limit:
            self.kill()

## Simple Animated Sprites
class AnimatedSprite(Generic):
    def __init__(self, assets, position, group, z_index = LEVEL_LAYERS['main']):
        self.animation_frames = assets
        self.frame_index = 0
        super().__init__(position, self.animation_frames[self.frame_index], group, z_index)

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
        self.mask = pygame.mask.from_surface(self.image)

class CrabMonster(Generic):
    def __init__(self, assets, position, group, collision_sprites):
        ## Animation
        self.animation_frames = assets
        self.frame_index = 0
        self.orientation = 'right'
        surface = self.animation_frames[f'run_{self.orientation}'][self.frame_index]
        super().__init__(position, surface, group)
        self.rect.bottom = self.rect.top + TILE_SIZE
        self.mask = pygame.mask.from_surface(self.image)

        ## Movement
        self.direction = vector(choice((1, -1)), 0)
        self.orientation = 'left' if self.direction.x  < 0 else 'right'
        self.position = vector(self.rect.topleft)
        self.speed  = 120
        self.collision_sprites = collision_sprites

        ## Destroy tooth at the beginning if he is not on the floor
        if not [sprite for sprite in self.collision_sprites if sprite.rect.collidepoint(self.rect.midbottom + vector(0, 10))]:
            self.kill()
    
    def animate(self, dt):
        current_animation = self.animation_frames[f'run_{self.orientation}']
        self.frame_index += ANIMATION_SPEED * dt
        self.frame_index = 0 if self.frame_index >= len(current_animation) else self.frame_index
        self.image = current_animation[int(self.frame_index)]
        self.mask = pygame.mask.from_surface(self.image)
    
    def move(self, dt):
        right_gap = self.rect.bottomright + vector(1, 1) # Gap at the bottom right corner of the monster sprite (we will use it detect clif side on it's right)
        right_block = self.rect.midright + vector(1, 0) # Gap at the mid right side of the monster sprite (we will use it detect wall on it's right)
        left_gap = self.rect.bottomleft + vector(-1, 1) # Gap at the bottom left corner of the monster sprite (we will use it detect clif side on it's left)
        left_block = self.rect.midleft + vector(-1, 0) # Gap at the mid left side of the monster sprite (we will use it detect wall on it's left)\

        if self.direction.x > 0: # moving right
            # floor collision
            floor_sprites = [sprite for sprite in self.collision_sprites if sprite.rect.collidepoint(right_gap)]
            # wall collision
            wall_sprites = [sprite for sprite in self.collision_sprites if sprite.rect.collidepoint(right_block)]

            if wall_sprites or not floor_sprites:
                self.direction.x *= -1
                self.orientation = 'left'

        if self.direction.x < 0: # moving left
            # floor collision
            floor_sprites = [sprite for sprite in self.collision_sprites if sprite.rect.collidepoint(left_gap)]
            # wall collision
            wall_sprites = [sprite for sprite in self.collision_sprites if sprite.rect.collidepoint(left_block)]

            if wall_sprites or not floor_sprites:
                self.direction.x *= -1
                self.orientation = 'right'

        self.position.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.position.x)

    def update(self, dt):
        self.animate(dt)
        self.move(dt)

class Shell(Generic):
    def __init__(self, orientation, assets, position, group, pearl_surface, damage_sprites):
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

        ## Pearls
        self.pearl_surface = pearl_surface
        self.has_shot = False
        self.attack_cooldown = Timer(2000)
        self.damage_sprites = damage_sprites
    
    def get_status(self):
        #if player is close enough (when distance btw shell and player is < 500px)
        if vector(self.player.rect.center).distance_to(vector(self.rect.center)) < 500 and not self.attack_cooldown.active:
            self.status = 'attack'
        else:
            self.status = 'idle'

    def animate(self, dt):
        current_animation = self.animation_frames[self.status]
        self.frame_index += ANIMATION_SPEED * dt
        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            if self.has_shot:
                self.attack_cooldown.activate()
                self.has_shot = False
        self.image = current_animation[int(self.frame_index)]

        if int(self.frame_index) == 2 and self.status == 'attack' and not self.has_shot: ## Only shoot pearl when shell is at frame 3 (showing shooting mouth)
            pearl_direction = vector(-1, 0) if self.orientation == 'left' else vector(1, 0)
            # create a pearl 
            offset = (pearl_direction * 50) if self.orientation == 'left' else (pearl_direction * 20) ## To place pearl exactly inside the shell mouth(Hit & Trail Value)
            offset += vector(0, -10) # Vertically center the pearl to the level of shell mouth
            Pearl(self.rect.center + offset, pearl_direction, self.pearl_surface, [self.groups()[0], self.damage_sprites]) # self.groups()[0]: all_sprites group
            self.has_shot = True

    def update(self, dt):
        self.get_status()
        self.animate(dt)
        self.attack_cooldown.update()

class Pearl(Generic):
    def __init__(self, position, direction, surface, group):
        super().__init__(position, surface, group)
        self.mask = pygame.mask.from_surface(self.image)

        ## Movement
        self.position = vector(self.rect.topleft)
        self.direction = direction
        self.speed = 150

        ## Self Destruct
        self.timer = Timer(6000)
        self.timer.activate()
    
    def update(self, dt):
        ## Movement
        self.position.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.position.x)

        ## Check Timer and destroy
        self.timer.update()
        if not self.timer.active:
            self.kill()

## Player
class Player(Generic):
    def __init__(self, position, assets, group, collision_sprites, jump_sound):
        ## Animation
        self.animation_frames = assets
        self.frame_index = 0
        self.status = 'idle'
        self.orientation = 'right'
        surface = self.animation_frames[f'{self.status}_{self.orientation}'][self.frame_index]

        super().__init__(position, surface, group)
        self.mask = pygame.mask.from_surface(self.image)

        ## Movement
        self.direction = vector()
        self.position = vector(self.rect.center)
        self.speed = PLAYER_SPEED
        self.gravity = GRAVITY
        self.on_floor = False

        ## Collision
        self.collision_sprites = collision_sprites
        self.hitbox = self.rect.inflate(-50, 0) ## Hit & Trail Value

        ## Invulnerability Timmer
        self.invulnerability_timer = Timer(200)

        ## Sounds
        self.jump_sound = jump_sound
        self.jump_sound.set_volume(0.1)
    
    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def animate(self, dt):
        current_animation = self.animation_frames[f'{self.status}_{self.orientation}']
        self.frame_index += ANIMATION_SPEED * dt
        if self.frame_index >= len(current_animation):
            self.frame_index = 0
        self.image = current_animation[int(self.frame_index)]
        self.mask = pygame.mask.from_surface(self.image)

        if self.invulnerability_timer.active:
            invulnerability_mode_surface = self.mask.to_surface()
            invulnerability_mode_surface.set_colorkey('black')
            self.image = invulnerability_mode_surface

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.orientation = 'right'
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.orientation = 'left'
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.on_floor:
            self.jump_sound.play()
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

    def damage(self):
        if not self.invulnerability_timer.active:
            self.invulnerability_timer.activate()
            self.direction.y -= 1.5
            # print("Ouch!")

    def update(self, dt):
        self.input()
        self.apply_gravity(dt)
        self.move(dt)
        self.check_on_floor()
        self.invulnerability_timer.update()

        self.get_status()
        self.animate(dt)