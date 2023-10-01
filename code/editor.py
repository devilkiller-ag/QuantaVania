#### IMPORTS
import pygame, sys 
from pygame.math import Vector2 as vector
from pygame.mouse import get_pressed as mouse_buttons # mouse_buttons() will return  bool (if_left_mouse_button_is_pressed, if_middle_mouse_button_is_pressed, if_right_mouse_button_is_pressed)
from pygame.mouse import get_pos as mouse_postion
from pygame.image import load as loadImage

from settings import *
from support import *
from menu import Menu
from timer import Timer

class Editor:
	def __init__(self, land_tiles):

		## main setup 
		self.editor_display_surface = pygame.display.get_surface()
		self.canvas_data = {}

		## imported graphics
		self.land_tiles = land_tiles
		self.import_graphics()

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

		## Menu
		self.menu = Menu()

		## Objects/Sprites: Player, Trees
		self.canvas_objects = pygame.sprite.Group()
		self.object_drag_active = False
		self.object_timer = Timer(OBJECT_PLACING_DELAY_TIME) # To restrict player to draw another object (tree) just after placing first one. This will avoid the placing of thousands of objects (trees) on just draging the mouse after placing the first object (tree).

		# Player
		CanvasObject(
			pos = (200, WINDOW_HEIGHT / 2), 
			frames = self.animations[0]['frames'], 
			tile_id = 0, 
			origin = self.origin, 
			group = self.canvas_objects
		)

		# Sky
		self.sky_handle = CanvasObject(
			pos = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), 
			frames = [self.sky_handle], 
			tile_id = 1, 
			origin = self.origin, 
			group = self.canvas_objects
		)

	### SUPPORT FUNCTIONS
	def import_graphics(self):
		self.water_bottom = loadImage('graphics/terrain/water/water_bottom.png').convert_alpha()
		self.sky_handle = loadImage('graphics/cursors/handle.png').convert_alpha()
		
		# import animations
		self.animations = {} # Ex: {3: {'frame index': 0, 'frames': [graphics_surfaces_01, graphics_surface_02], 'length': 2}}
		for key, value in EDITOR_DATA.items():
			if value['graphics']:
				graphics = import_images_from_folder(value['graphics'])
				self.animations[key] = {
					'frame index': 0,
					'frames': graphics,
					'length': len(graphics)
				}

		# import preview surfaces
		self.preview_surfaces = {key: loadImage(value['preview']) for key, value in EDITOR_DATA.items() if value['preview']}

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

	def mouse_on_which_object(self):
		for sprite in self.canvas_objects:
			if sprite.rect.collidepoint(mouse_postion()):
				return sprite

	def check_neighbors(self, cell_position):
		# create a local cluster of cells around the target cell (so that we only need to check only those 9 tiles in the cluster and not all the tiles)
		cluster_size = 3
		local_cluster = [
			(cell_position[0] + col - int(cluster_size / 2), cell_position[1] + row - int(cluster_size / 2)) 
			for col in range(cluster_size) 
			for row in range(cluster_size)
		]
		# check neighbors
		for cell in local_cluster:
			# if cell exists in the canvas, set neighbors to [], and water_on_top False (Reset)
			if cell in self.canvas_data:
				self.canvas_data[cell].terrain_neighbors = []
				self.canvas_data[cell].water_on_top = False

				# now check neighbors
				for name, side in NEIGHBOR_DIRECTIONS.items():
					neighbor_cell = (cell[0] + side[0], cell[1] + side[1])
					
					if neighbor_cell in self.canvas_data:
						# water top neighbor
						if self.canvas_data[cell].has_water: # if water in the current tile
							if name == 'A' and self.canvas_data[neighbor_cell].has_water:# and if water tile on top 
								self.canvas_data[cell].water_on_top = True

						# terrain neighbors
						if self.canvas_data[neighbor_cell].has_terrain:
							self.canvas_data[cell].terrain_neighbors.append(name)

	def animation_update(self, dt):
		for value in self.animations.values():
			value['frame index'] += ANIMATION_SPEED * dt
			# reset frame_index after all frames of one animation are drawn
			if value['frame index'] >= value['length']:
				value['frame index'] = 0

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

			self.object_drag(event)

			self.canvas_add()
			self.canvas_remove()

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
			self.origin = vector(mouse_postion()) - self.pan_offset # update origin
			for sprite in self.canvas_objects: # update position of all sprites
				sprite.pan_position(self.origin)

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

	def canvas_add(self):
		if mouse_buttons()[0] and not self.menu.menu_area.collidepoint(mouse_postion()) and not self.object_drag_active: # if we are left clicking outside the menu area and we have not selected any object(Player, Trees)
			current_cell = self.get_current_cell()

			if EDITOR_DATA[self.selection_index]['type'] == 'tile': ## ADD TILE
				if current_cell != self.last_selected_cell:
					if current_cell in self.canvas_data:
						self.canvas_data[current_cell].add_id(self.selection_index)
					else:
						self.canvas_data[current_cell] = CanvasTile(self.selection_index)
					
					self.check_neighbors(current_cell)
					self.last_selected_cell = current_cell
			
			else: ## ADD CANVAS OBJECT
				if not self.object_timer.active:
					CanvasObject(
						pos = mouse_postion(), 
						frames = self.animations[self.selection_index]['frames'], 
						tile_id = self.selection_index, 
						origin = self.origin, 
						group = self.canvas_objects
					)
					self.object_timer.activate()

	def canvas_remove(self):

		if mouse_buttons()[2] and not self.menu.menu_area.collidepoint(mouse_postion()): # if we are right clicking outside the menu area
			
			## delete objects
			selected_object = self.mouse_on_which_object()
			if selected_object:
				if EDITOR_DATA[selected_object.tile_id]['style'] not in ['player', 'sky']: # user should not be able to delete hero(player) or sky_handle
					selected_object.kill()
			
			## delete tiles
			if self.canvas_data:
				current_cell = self.get_current_cell()
				if current_cell in self.canvas_data:
					self.canvas_data[current_cell].remove_id(self.selection_index)

					if self.canvas_data[current_cell].is_empty:
						del self.canvas_data[current_cell]
					
					self.check_neighbors(current_cell)

	def object_drag(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN and mouse_buttons()[0]:
			for sprite in self.canvas_objects:
				if sprite.rect.collidepoint(event.pos):
					sprite.start_drag()
					self.object_drag_active = True
		
		if event.type == pygame.MOUSEBUTTONUP and self.object_drag_active:
			for sprite in self.canvas_objects:
				if sprite.selected:
					sprite.end_drag(self.origin)
					self.object_drag_active = False

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

	def draw_level(self):
		# Draw Tiles (Terrain, Water, Coin, Enemy)
		for cell_pos, tile in self.canvas_data.items():
			pos = self.origin + vector(cell_pos) * TILE_SIZE

			## terrain
			if tile.has_terrain:
				terrain_string = ''.join(tile.terrain_neighbors)
				terrain_style = terrain_string if terrain_string in self.land_tiles else 'X'
				self.editor_display_surface.blit(self.land_tiles[terrain_style], pos)
			
			## water
			if tile.has_water:
				if tile.water_on_top:
					self.editor_display_surface.blit(self.water_bottom, pos)
				else:
					water_frames = self.animations[3]['frames'] # Since Water Tiles has key 3 in the EDITOR_DATA
					index = int(self.animations[3]['frame index'])
					water_surface = water_frames[index]
					self.editor_display_surface.blit(water_surface, pos)

			## coin
			if tile.coin:
				coin_frames = self.animations[tile.coin]['frames']
				index= int(self.animations[tile.coin]['frame index'])
				coin_surface = coin_frames[index]
				coin_rect_area = coin_surface.get_rect(center=(pos[0] + TILE_SIZE // 2, pos[1] + TILE_SIZE // 2)) # to center the coins in the grid_box/tile
				self.editor_display_surface.blit(coin_surface, coin_rect_area)

			## enemy
			if tile.enemy:
				enemy_frames = self.animations[tile.enemy]['frames']
				index= int(self.animations[tile.enemy]['frame index'])
				enemy_surface = enemy_frames[index]
				enemy_rect_area = enemy_surface.get_rect(midbottom=(pos[0] + TILE_SIZE // 2, pos[1] + TILE_SIZE)) # to make the enemies touch the bottom of the grid_box/tile
				self.editor_display_surface.blit(enemy_surface, enemy_rect_area)

		# Draw Objects (Player, Trees)
		self.canvas_objects.draw(self.editor_display_surface)

	def preview(self):
		selected_object = self.mouse_on_which_object()
		if not self.menu.menu_area.collidepoint(mouse_postion()): # if we are not in the menu
			## draws marker around the object when hovered over 
			if selected_object:
				marker_rect = selected_object.rect.inflate(10, 10)
				marker_line_color = 'black'
				market_line_width = 3
				marker_line_size = 15
				# topleft marker
				pygame.draw.lines(
					self.editor_display_surface, 
					marker_line_color, 
					False, 
					((
						marker_rect.topleft[0], marker_rect.topleft[1] + marker_line_size), 
						marker_rect.topleft,  
						(marker_rect.topleft[0] + marker_line_size, marker_rect.topleft[1])
					), 
					market_line_width
				)
				# bottomleft marker
				pygame.draw.lines(
					self.editor_display_surface, 
					marker_line_color, 
					False, 
					((
						marker_rect.bottomleft[0], marker_rect.bottomleft[1] - marker_line_size), 
						marker_rect.bottomleft,  
						(marker_rect.bottomleft[0] + marker_line_size, marker_rect.bottomleft[1])
					), 
					market_line_width
				)
				# topright marker
				pygame.draw.lines(
					self.editor_display_surface, 
					marker_line_color, 
					False, 
					((
						marker_rect.topright[0], marker_rect.topright[1] + marker_line_size), 
						marker_rect.topright,  
						(marker_rect.topright[0] - marker_line_size, marker_rect.topright[1])
					), 
					market_line_width
				)
				# bottomright marker
				pygame.draw.lines(
					self.editor_display_surface, 
					marker_line_color, 
					False, 
					((
						marker_rect.bottomright[0], marker_rect.bottomright[1] - marker_line_size), 
						marker_rect.bottomright,  
						(marker_rect.bottomright[0] - marker_line_size, marker_rect.bottomright[1])
					), 
					market_line_width
				)

			## preview the tile / object if we are placing any object on the canvas
			else:
				data_type_dict = {key: value for key, value in EDITOR_DATA.items()}
				preview_surface = self.preview_surfaces[self.selection_index].copy()
				preview_surface.set_alpha(200)

				# preview tile
				if data_type_dict[self.selection_index] == 'tile':
					current_cell = self.get_current_cell()
					preview_rect = preview_surface.get_rect(topleft = self.origin + vector(current_cell) * TILE_SIZE)

				# preview object
				else:
					preview_rect = preview_surface.get_rect(center = mouse_postion())

				self.editor_display_surface.blit(preview_surface, preview_rect)


	### FUNCTION TO RUN & UPDATE EVERYTHING
	def run(self, dt):
		self.event_loop()

		# updating
		self.animation_update(dt)
		self.canvas_objects.update(dt)
		self.object_timer.update()


		# drawing
		self.editor_display_surface.fill('white')
		self.draw_level()
		self.draw_grid_lines()
		pygame.draw.circle(self.editor_display_surface, 'red', self.origin, 10)
		self.preview()
		self.menu.display(self.selection_index)


class CanvasTile:
	def __init__(self, tile_id):
		self.is_empty = False

		## terrain
		self.has_terrain = False
		self.terrain_neighbours = []

		## water
		self.has_water = False
		self.water_on_top = False

		## coin
		self.coin = None # can be equal to 4, 5, or 6

		## enemy
		self.enemy = None # can be equal to 7, 8, 9, or 10

		self.add_id(tile_id)

	def add_id(self, tile_id):
		options = {key: value['style'] for key, value in EDITOR_DATA.items()}
		match options[tile_id]:
			case 'terrain': self.has_terrain = True
			case 'water': self.has_water = True
			case 'coin': self.coin = tile_id
			case 'enemy': self.enemy = tile_id

	def remove_id(self, tile_id):
		options = {key: value['style'] for key, value in EDITOR_DATA.items()}
		match options[tile_id]:
			case 'terrain': self.has_terrain = False
			case 'water': self.has_water = False
			case 'coin': self.coin = None
			case 'enemy': self.enemy = None
		self.check_content()
	
	def check_content(self):
		if not self.has_terrain and not self.has_water and not self.coin and not self.enemy:
			self.is_empty = True


class CanvasObject(pygame.sprite.Sprite):
	def __init__(self, pos, frames, tile_id, origin, group):
		super().__init__(group)
		self.tile_id = tile_id

		## animation
		self.frames = frames
		self.frame_index = 0

		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect(center = pos)

		## movement
		self.distance_to_origin = vector(self.rect.topleft) - origin
		self.selected = False
		self.mouse_offset = vector()
	
	## FUNCTIONS TO HANDLE OBJECT DRAG
	def start_drag(self):
		self.selected = True
		self.mouse_offset = vector(mouse_postion()) - vector(self.rect.topleft)

	def drag(self):
		if self.selected:
			self.rect.topleft = mouse_postion() - self.mouse_offset 

	def end_drag(self, origin):
		self.selected = False
		self.distance_to_origin = vector(self.rect.topleft) - origin

	## FUNCTIONS TO HANDLE ANIMATIONS
	def animate(self, dt):
		self.frame_index += ANIMATION_SPEED * dt
		if self.frame_index >= len(self.frames):
			self.frame_index = 0
		self.image = self.frames[int(self.frame_index)]
		self.rect = self.image.get_rect(midbottom = self.rect.midbottom)

	## FUNCTIONS TO HANDLE OBJECT MOVEMENT ALONG WITH CANVAS DRAG
	def pan_position(self, origin):
		self.rect.topleft = origin + self.distance_to_origin # change the positon of object according to the pan movement

	def update(self, dt):
		self.animate(dt)
		self.drag()