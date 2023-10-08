import pygame,sys

from settings import *
from support import import_images_from_folder

class Buttons:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image,(int(width*scale), int(height*scale))).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.toprect = (x,y)
        self.clicked = False

    def draw(self,surface):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action

class MainMenu:
    def __init__(self):
        self