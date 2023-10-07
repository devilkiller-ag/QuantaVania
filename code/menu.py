#### IMPORTS
import pygame
from pygame.image import load as loadImage

from settings import *

class Menu:
    def __init__(self):
        self.menu_display_surface = pygame.display.get_surface()
        self.create_data()
        self.create_buttons()


    def create_data(self):
        self.menu_surfaces = {}

        for key, value in EDITOR_DATA.items():
            if value['menu_type']: # to only select data which have to be shown in menu for user to select
                if not value['menu_type'] in self.menu_surfaces:
                    self.menu_surfaces[value['menu_type']] = [(key, loadImage(value['menu_surf']))]
                else:
                    self.menu_surfaces[value['menu_type']].append((key, loadImage(value['menu_surf'])))


    def create_buttons(self):
        ## General Menu Area
        menu_size = 180
        menu_margin = 6
        menu_position = (WINDOW_WIDTH - (menu_size + menu_margin), WINDOW_HEIGHT - (menu_size + menu_margin)) # TOP_LEFT POSITION OF MENU
        self.menu_area = pygame.Rect(menu_position, (menu_size, menu_size))

        ## Menu Button Areas
        button_margin = 5
        generic_button_area = pygame.Rect(self.menu_area.topleft, (self.menu_area.width / 2, self.menu_area.height / 2))
        self.tile_button_area = generic_button_area.copy().inflate(-button_margin, -button_margin)
        self.coin_button_area = generic_button_area.copy().move(self.menu_area.width / 2, 0).inflate(-button_margin, -button_margin)
        self.enemy_button_area = generic_button_area.copy().move(0, self.menu_area.height / 2).inflate(-button_margin, -button_margin)
        self.qcomp_button_area = generic_button_area.copy().move(self.menu_area.width / 2, self.menu_area.height / 2).inflate(-button_margin, -button_margin)
        
        ## Create Menu Buttons
        self.buttons = pygame.sprite.Group()
        MenuButton(self.tile_button_area, self.buttons, self.menu_surfaces['terrain'])
        MenuButton(self.coin_button_area, self.buttons, self.menu_surfaces['coin'])
        MenuButton(self.enemy_button_area, self.buttons, self.menu_surfaces['enemy'])
        MenuButton(self.qcomp_button_area, self.buttons, self.menu_surfaces['qcomp fg'], self.menu_surfaces['qcomp bg'])


    def click(self, mouse_position, mouse_buttons):
        for sprite in self.buttons:
            if sprite.rect.collidepoint(mouse_position):
                if mouse_buttons[1]: # middle mouse click
                    if sprite.items['alt']:
                        sprite.main_active = not sprite.main_active  
                    else:
                        sprite.main_active = True

                elif mouse_buttons[2]: # right mouse click
                    sprite.switch()
                    
                return sprite.get_id()

    def highlight_indicator(self, index):
        index = 2 if index == None else index # To avoid error if user clicks on button boundary (which causes index to be set to None)

        if EDITOR_DATA[index]['menu_type'] == 'terrain':
            pygame.draw.rect(self.menu_display_surface, BUTTON_LINE_COLOR, self.tile_button_area.inflate(4, 4), 5, 4)
        elif EDITOR_DATA[index]['menu_type'] == 'coin':
            pygame.draw.rect(self.menu_display_surface, BUTTON_LINE_COLOR, self.coin_button_area.inflate(4, 4), 5, 4)
        elif EDITOR_DATA[index]['menu_type'] == 'enemy':
            pygame.draw.rect(self.menu_display_surface, BUTTON_LINE_COLOR, self.enemy_button_area.inflate(4, 4), 5, 4)
        elif EDITOR_DATA[index]['menu_type'] in ('qcomp bg', 'qcomp fg'):
            pygame.draw.rect(self.menu_display_surface, BUTTON_LINE_COLOR, self.qcomp_button_area.inflate(4, 4), 5, 4)

    def display(self, index):
        self.buttons.update()
        self.buttons.draw(self.menu_display_surface)
        self.highlight_indicator(index)

class MenuButton(pygame.sprite.Sprite):
    def __init__(self, rect, group, items, items_alt = None):
        super().__init__(group)
        
        self.image = pygame.Surface(rect.size)
        self.rect = rect

        # items
        self.items = {'main': items, 'alt': items_alt}
        self.index = 0
        self.main_active = True

    def get_id(self):
        return ((self.items['main' if self.main_active else 'alt'])[self.index])[0]
    
    def switch(self):
        self.index += 1
        self.index = 0 if self.index >= len(self.items['main' if self.main_active else 'alt']) else self.index
    
    def update(self):
        self.image.fill(BUTTON_BG_COLOR)
        button_surface = ((self.items['main' if self.main_active else 'alt'])[self.index])[1]
        button_area = button_surface.get_rect(center = (self.rect.width / 2, self.rect.height / 2))
        self.image.blit(button_surface, button_area)

class Button(): ## For Editor Save Play Buttons
    def __init__(self, type, x, y, image, display_surface):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.display_surface = display_surface

    def display(self):
        self.display_surface.blit(self.image, (self.rect.x, self.rect.y))