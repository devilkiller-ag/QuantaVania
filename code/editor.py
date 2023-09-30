#### IMPORTS
import pygame, sys 
from pygame.math import Vector2 as vector
from pygame.mouse import get_pressed as mouse_buttons # mouse_buttons() will return  bool (if_left_mouse_button_is_pressed, if_middle_mouse_button_is_pressed, if_right_mouse_button_is_pressed)
from pygame.mouse import get_pos as mouse_postion

from settings import *
from menu import Menu

class Editor:
	def __init__(self):

		## main setup 
		self.editor_display_surface = pygame.display.get_surface()
		self.canvas_data = {}

		## navigation
		self.origin = vector()
		self.pan_active = False
		self.pan_offset = vector()

		## support/grid lines
		self.grid_lines_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT)) # new surface for grid as we want to decrease it's opacity (If we draw it on same surface then decreasing opacity will decrease opacity of all the objects drawn on that surface)
		self.grid_lines_surface.set_colorkey('green')
		self.grid_lines_surface.set_alpha(30)

		## selection: what type of object/data is selected by the player in the editor
		self.selection_index = 2 # By Default set to 2, i.e., terrain
		self.last_selected_cell = None

		## menu
		self.menu = Menu()

	### SUPPORT FUNCTIONS
	def get_current_cell(self):
		distance_to_origin = vector(mouse_postion()) - self.origin

		if distance_to_origin.x > 0:
			col = int(distance_to_origin.x / TILE_SIZE)
		else:
			col = int(distance_to_origin.x / TILE_SIZE) - 1

		if distance_to_origin.y > 0:
			row = int(distance_to_origin.y / TILE_SIZE)
		else:
			row = int(distance_to_origin.y / TILE_SIZE) - 1

		return col, row

	### FUNCTIONS TO HANDLE INPUTS
	def event_loop(self):
		for event in pygame.event.get():
			# Detect if user wants to quit the game
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			
			self.pan_input(event) # pass the event to pan_input to detect if user wants to pan the editor area and act accordingly
			self.selection_hotkeys(event)
			self.menu_click(event)
			self.canvas_add(event)

	def pan_input(self, event):
		# Check if user wants to pan by using middle mouse button (pressed / released)
		if (event.type == pygame.MOUSEBUTTONDOWN and mouse_buttons()[2]):
			self.pan_active = True
			self.pan_offset = vector(mouse_postion()) - self.origin
		elif (not mouse_buttons()[2]):
			self.pan_active = False
		
		# mouse wheel
		if (event.type == pygame.MOUSEWHEEL):
			if pygame.key.get_pressed()[pygame.K_LCTRL]:
				# left control + scroll up to go towards down, and left control + scroll down to go towards up
				self.origin.y -= event.y * 50 # 50 is a factor for making movement little large on mouse scroll (hit & trail)
			else:
				# scroll up to go towards right and scroll down to go towards left
				self.origin.x -= event.y * 50 # 50 is a factor for making movement little large on mouse scroll (hit & trail)
		
		# panning update
		if self.pan_active:
			self.origin = vector(mouse_postion()) - self.pan_offset

	def selection_hotkeys(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT:
				self.selection_index += 1
			elif event.key == pygame.K_LEFT:
				self.selection_index -= 1

		self.selection_index = 2 if self.selection_index == None else self.selection_index # To avoid error if user clicks on menu button boundary (which causes selection_index to be set to None)
		self.selection_index = max(2, min(self.selection_index, 18)) # To limit the selection index between 2 to 18 (because between that's what editor data have index)

	def menu_click(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN and self.menu.menu_area.collidepoint(mouse_postion()):
			self.selection_index = self.menu.click(mouse_postion(), mouse_buttons())

	def canvas_add(self, event):
		if mouse_buttons()[0] and not self.menu.menu_area.collidepoint(mouse_postion()): # if we are lef clicking outside the menu area
			current_cell = self.get_current_cell()
			
			if current_cell != self.last_selected_cell:
				if current_cell in self.canvas_data:
					self.canvas_data[current_cell].add_id(self.selection_index)
				else:
					self.canvas_data[current_cell] = CanvasTile(self.selection_index)
				
				self.last_selected_cell = current_cell

	### FUNCTIONS TO DRAW THINGS
	def draw_grid_lines(self):
		num_cols = WINDOW_WIDTH // TILE_SIZE
		num_rows = WINDOW_HEIGHT // TILE_SIZE

		# Psuedo Origin (Always in the top-left box): To make the lines always on the display on scroll
		origin_offset = vector(
			x = self.origin.x - int(self.origin.x / TILE_SIZE) * TILE_SIZE,
			y = self.origin.y - int(self.origin.y / TILE_SIZE) * TILE_SIZE
		) 
		
		self.grid_lines_surface.fill('green')

		for col in range(num_cols + 1):
			x = origin_offset.x + (col * TILE_SIZE)
			pygame.draw.line(self.grid_lines_surface, LINE_COLOR, (x, 0), (x, WINDOW_HEIGHT))

		for row in range(num_rows + 1):
			y = origin_offset.y + (row * TILE_SIZE)
			pygame.draw.line(self.grid_lines_surface, LINE_COLOR, (0, y), (WINDOW_WIDTH, y))

		self.editor_display_surface.blit(self.grid_lines_surface, (0, 0))


	### FUNCTION TO RUN EVERYTHING
	def run(self, dt):
		self.event_loop()

		# drawing
		self.editor_display_surface.fill('white')
		self.draw_grid_lines()
		pygame.draw.circle(self.editor_display_surface, 'red', self.origin, 10)
		self.menu.display(self.selection_index)

class CanvasTile:
	def __init__(self, tile_id):

		## terrain
		self.has_terrain = False
		self.terrain_neighbours = []

		## water
		self.has_water = False
		self.water_on_top = False

		## coin
		self.coin = None # can be equal to 4, 5, or 6

		## enemy
		self.enemy = None

		## objects
		self.objects = []

		self.add_id(tile_id)

	def add_id(self, tile_id):
		options = {key: value['style'] for key, value in EDITOR_DATA.items()}
		match options[tile_id]:
			case 'terrain': self.has_terrain = True
			case 'water': self.has_water = True
			case 'coin': self.coin = tile_id
			case 'enemy': self.enemy = tile_id