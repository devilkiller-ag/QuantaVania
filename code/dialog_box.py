#### IMPORTS
import pygame, sys 
from pygame.image import load as loadImage
from settings import *

class DialogBox(pygame.sprite.Sprite):
    def __init__(self, width, height, position, display_surface, messages, is_active):
        super().__init__()
        self.width = width
        self.height = height
        self.position = position
        self.display_surface = display_surface
        self.messages = messages
        self.current_message_index = 0
        self.message = self.messages[self.current_message_index]
        self.message_position = (50, 50)
        self.is_active = is_active
        self.message_color = DIALOG_TEXT_COLOR

        self.image = loadImage('graphics/ui/dialog_box.png')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=position)

        self.font = pygame.font.Font("graphics/ui/ARCADEPI.TTF", 20)

    def write_message(self):
        collection = [line.split(' ') for line in self.message.splitlines()]
        space = self.font.size(' ')[0]
        x, y = self.message_position
        for lines in collection:
            for words in lines:
                word_surface = self.font.render(words, False, self.message_color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= self.width - self.message_position[0]:
                    x = self.message_position[0]
                    y += word_height
                self.image.blit(word_surface, (x, y))
                x += word_width + space
            x = self.message_position[0]
            y += word_height * 2

    def next_message(self):
        if self.current_message_index < len(self.messages):
            self.current_message_index += 1
        else:
            self.is_active = False
            self.kill()

    def run(self):
        self.display_surface.blit(self.image, self.position)
        # self.write_message()

        if self.current_message_index < len(self.messages):
            self.message = self.messages[self.current_message_index]
            self.write_message()

        ## Diplay Dialog Box Navigation Message
        nav_message = "Press ENTER to continue..."
        nav_message_surface = self.font.render(nav_message, False, self.message_color)
        nav_message_rect = nav_message_surface.get_rect(midbottom = (self.width/2, self.height - 20))
        self.image.blit(nav_message_surface, nav_message_rect)

        # self.is_active = False
        # if not self.is_active:
        #     self.kill()