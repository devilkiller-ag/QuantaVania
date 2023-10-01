#### IMPORTS
import pygame
from pygame.image import load as loadImage
from pygame.math import Vector2 as vector

from settings import *
from support import *
from editor import Editor
from custom_level import CustomLevel

class Main:
	def __init__(self):
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		self.clock = pygame.time.Clock()
		self.import_graphics()

		## Editor & Levels
		self.editor_active = True
		self.transition = Transition(self.toggle)
		self.editor = Editor(self.land_tiles, self.switch)

		## CURSOR
		cursor_surface = loadImage('graphics/cursors/mouse.png').convert_alpha()
		cursor = pygame.cursors.Cursor((0, 0), cursor_surface)
		pygame.mouse.set_cursor(cursor)

	def import_graphics(self):
		self.land_tiles = import_images_from_folder_as_dict('graphics/terrain/land')

	def toggle(self): # Toggle (Turn On/Off) between Editor, Levels, CustomLevel, & Menu
		self.editor_active= not self.editor_active
	
	def switch(self, custom_level_grid = None): # Switch between Editor, Levels, CustomLevel, & Menu
		self.transition.active = True
		if custom_level_grid:
			self.custom_level = CustomLevel(custom_level_grid, self.switch)

	def run(self):
		while True:
			dt = self.clock.tick() / 1000 # delta time
			
			if self.editor_active:
				self.editor.run(dt)
			else:
				self.custom_level.run(dt)
			
			self.transition.display(dt)
			pygame.display.update()

class Transition:
	def __init__(self, toggle):
		self.transition_display_surface = pygame.display.get_surface()
		self.toggle = toggle
		self.active = False

		self.border_width = 0
		self.direction = 1
		self.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
		self.radius = vector(self.center).magnitude()
		self.threshold = self.radius + 100
	
	def display(self, dt):
		if self.active:
			self.border_width += 1000 * dt * self.direction
			if self.border_width >= self.threshold:
				self.direction = -1
				self.toggle()
			if self.border_width < 0:
				self.active = False
				self.border_width = 0
				self.direction = 1
			pygame.draw.circle(self.transition_display_surface, 'black', self.center, self.radius, int(self.border_width))

if __name__ == '__main__':
	main = Main()
	main.run()