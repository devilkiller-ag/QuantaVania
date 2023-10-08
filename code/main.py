#### IMPORTS
import pygame
from pygame.image import load as loadImage
from pygame.math import Vector2 as vector
from os import walk

from settings import *
from support import *
from overworld import Overworld
from editor import Editor
from custom_level import CustomLevel

class Main:
	def __init__(self):
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		pygame.display.set_caption("QuantaVania")
		self.clock = pygame.time.Clock()
		self.import_graphics()

		## Game Atributes
		self.max_level = 1
		self.status = 'overworld'

		## Editor & Levels
		self.editor_active = True
		self.transition = Transition(self.toggle)
		self.editor = Editor(self.land_tiles, self.switch, self.create_overworld, self.max_level, self.max_level)

		## Assets Data
		self.asset_dictionary = {
			'clouds': self.clouds,
			'land': self.land_tiles,
			'water bottom': self.water_bottom,
			'water top': self.water_top_animation,
			'gold': self.gold,
			'silver': self.silver,
			'diamond': self.diamond,
			'particles': self.particles,
			'qcomps': self.qcomps,
			'spikes': self.spikes,
			'crab_monster': self.crab_monster,
			'shoot_monster': self.shoot_monster,
			'explosion': self.explosion,
			'player': self.player_graphics
		}

		## Import Saved Levels
		self.all_levels = import_levels(SAVE_FOLDER_NAME)
		# print(all_levels)

		## Overworld
		self.overworld = Overworld(self.all_levels, 0, self.max_level, self.display_surface, self.create_level)

		## CURSOR
		cursor_surface = loadImage('graphics/cursors/mouse.png').convert_alpha()
		cursor = pygame.cursors.Cursor((0, 0), cursor_surface)
		pygame.mouse.set_cursor(cursor)

	def create_level(self, current_level):
		self.custom_level = CustomLevel(
			current_level, 
			self.all_levels[f'level_{current_level}']['unlock'],
			self.all_levels[f'level_{current_level}']['data'], 
			self.switch, 
			self.create_overworld, 
			self.asset_dictionary, 
			self.level_sounds
		)
		self.status = 'level'

	def create_overworld(self, current_level, new_max_level):
		if new_max_level > self.max_level:
			self.max_level = new_max_level
		self.overworld = Overworld(self.all_levels, current_level, self.max_level, self.display_surface, self.create_level)
		self.status = 'overworld'

	def import_graphics(self):
		# clouds
		self.clouds = import_images_from_folder('graphics/clouds')
		
		# terrains
		self.land_tiles = import_images_from_folder_as_dict('graphics/terrain/land')
		self.water_bottom = loadImage('graphics/terrain/water/water_bottom.png').convert_alpha()
		self.water_top_animation = import_images_from_folder('graphics/terrain/water/animation')

		# coins
		self.gold = import_images_from_folder('graphics/items/gold')
		self.silver = import_images_from_folder('graphics/items/silver')
		self.diamond = import_images_from_folder('graphics/items/diamond')
		self.particles = import_images_from_folder('graphics/items/particle')

		# qcomp trees
		self.qcomps = {folder: import_images_from_folder(f'graphics/terrain/qcomp/{folder}') for folder in list(walk('graphics/terrain/qcomp'))[0][1]}

		# enemies
		self.spikes = loadImage('graphics/enemies/spikes/spikes.png').convert_alpha()
		self.crab_monster = {folder: import_images_from_folder(f'graphics/enemies/crab_monster/{folder}') for folder in list(walk('graphics/enemies/crab_monster'))[0][1]}
		self.shoot_monster = {folder: import_images_from_folder(f'graphics/enemies/shoot_monster_left/{folder}') for folder in list(walk('graphics/enemies/shoot_monster_left'))[0][1]} # only importing shoot_monster_left as we can easily get all the graphics of shoot_monster_right by flipping the graphics of shoot_monster_left
		self.explosion = import_images_from_folder('graphics/items/explosion')

		# player
		self.player_graphics = {folder: import_images_from_folder(f'graphics/player/{folder}') for folder in list(walk('graphics/player'))[0][1]}

		# sounds
		self.level_sounds = {
			'coin': pygame.mixer.Sound('audio/coin.wav'),
			'hit': pygame.mixer.Sound('audio/hit.wav'),
			'jump': pygame.mixer.Sound('audio/jump.wav'),
			'music': pygame.mixer.Sound('audio/SuperHero.ogg')
		}

	def toggle(self): # Toggle (Turn On/Off) between Editor, Levels, CustomLevel, & Menu
		self.editor_active = not self.editor_active
		if self.editor_active:
			self.editor.editor_music.play()
	
	def switch(self, custom_level_grid = None): # Switch between Editor, Levels, CustomLevel, & Menu
		
		sounds_dictionary = self.level_sounds

		self.transition.active = True
		if custom_level_grid:
			self.custom_level = CustomLevel(custom_level_grid, self.switch, self.create_overworld, self.asset_dictionary, sounds_dictionary)

	def run(self):
		while True:
			dt = self.clock.tick() / 1000 # delta time
			
			if self.status == 'overworld':
				self.overworld.run(dt)
			elif self.status == 'level':
				self.custom_level.run(dt)
			else: # self.status == 'editor'
				self.editor.run(dt)
			# 	if self.editor_active:
			# 		self.editor.run(dt)
			# 	else:
			# 		self.custom_level.run(dt)

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