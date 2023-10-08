#### IMPORTS
import pygame, sys 
from pygame.math import Vector2 as vector
from pygame.mouse import get_pressed as mouse_buttons # mouse_buttons() will return  bool (if_left_mouse_button_is_pressed, if_middle_mouse_button_is_pressed, if_right_mouse_button_is_pressed)
from pygame.mouse import get_pos as mouse_postion
from pygame.image import load as loadImage
from random import choice, randint

from settings import *
from support import *
from menu import Menu, Button
from timer import Timer
from save_load_manager import SaveLoadSystem

class Editor:
	def __init__(self, land_tiles, switch, create_overworld, current_level , new_max_level):

		## main setup 
		self.editor_display_surface = pygame.display.get_surface() 
		self.canvas_data = {}
		self.switch = switch
		self.create_overworld = create_overworld
		self.current_level = current_level
		self.new_max_level = new_max_level

		## imported graphics
		self.land_tiles = land_tiles
		self.import_graphics()
		self.bg_lvl1 = loadImage("graphics/background/1.png")	# background for lvl 1

		## clouds
		self.current_clouds = []
		self.cloud_surfaces = import_images_from_folder('graphics/clouds')
		self.cloud_timer = pygame.USEREVENT + 1
		pygame.time.set_timer(self.cloud_timer, 2000)
		self.startup_clouds()

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
		self.foreground_objects = pygame.sprite.Group() # to store foreground qcomp trees
		self.background_objects = pygame.sprite.Group() # to store background qcomp trees
		self.object_drag_active = False
		self.object_timer = Timer(OBJECT_PLACING_DELAY_TIME) # To restrict player to draw another object (tree) just after placing first one. This will avoid the placing of thousands of objects (trees) on just draging the mouse after placing the first object (tree).

		# Player
		CanvasObject(
			pos = (200, WINDOW_HEIGHT / 2), 
			frames = self.animations[0]['frames'], 
			tile_id = 0, 
			origin = self.origin, 
			group = [self.canvas_objects, self.foreground_objects]
		)

		# Sky
		self.sky_handle = CanvasObject(
			pos = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), 
			frames = [self.sky_handle], 
			tile_id = 1, 
			origin = self.origin, 
			group = [self.canvas_objects, self.background_objects]
		)

		## Editor Background Music
		self.editor_music = pygame.mixer.Sound('audio/Explorer.ogg')
		self.editor_music.set_volume(0.4)
		self.editor_music.play(loops = -1)

		## Save/Load Manager
		self.saveloadmanager = SaveLoadSystem(".qvania", "saved_levels")
		self.save_level_button = Button('save', WINDOW_WIDTH - (BUTTON_SIZE + BUTTON_MARGIN), BUTTON_MARGIN, self.save_button, self.editor_display_surface)
		self.play_level_button = Button('play', BUTTON_MARGIN, BUTTON_MARGIN, self.play_button, self.editor_display_surface)

	### SUPPORT FUNCTIONS
	def import_graphics(self):
		self.water_bottom = loadImage('graphics/terrain/water/water_bottom.png').convert_alpha()
		self.sky_handle = loadImage('graphics/cursors/handle.png').convert_alpha()
		self.save_button = loadImage('graphics/ui/save_btn.png').convert_alpha()
		self.play_button = loadImage('graphics/ui/play_btn.png').convert_alpha()
		
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

	def get_current_cell(self, object = None):
		distance_to_origin = vector(mouse_postion()) - self.origin if not object else vector(object.distance_to_origin) - self.origin

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

	def check_neighbours(self, cell_position):
		# create a local cluster of cells around the target cell (so that we only need to check only those 9 tiles in the cluster and not all the tiles)
		cluster_size = 3
		local_cluster = [
			(cell_position[0] + col - int(cluster_size / 2), cell_position[1] + row - int(cluster_size / 2)) 
			for col in range(cluster_size) 
			for row in range(cluster_size)
		]
		# check neighbours
		for cell in local_cluster:
			# if cell exists in the canvas, set neighbours to [], and water_on_top False (Reset)
			if cell in self.canvas_data:
				self.canvas_data[cell].terrain_neighbours = []
				self.canvas_data[cell].water_on_top = False

				# now check neighbours
				for name, side in NEIGHBOR_DIRECTIONS.items():
					neighbor_cell = (cell[0] + side[0], cell[1] + side[1])
					
					if neighbor_cell in self.canvas_data:
						# water top neighbor
						if self.canvas_data[cell].has_water: # if water in the current tile
							if name == 'A' and self.canvas_data[neighbor_cell].has_water:# and if water tile on top 
								self.canvas_data[cell].water_on_top = True

						# terrain neighbours
						if self.canvas_data[neighbor_cell].has_terrain:
							self.canvas_data[cell].terrain_neighbours.append(name)

	def animation_update(self, dt):
		for value in self.animations.values():
			value['frame index'] += ANIMATION_SPEED * dt
			# reset frame_index after all frames of one animation are drawn
			if value['frame index'] >= value['length']:
				value['frame index'] = 0

	### FUNCTIONS TO EXPORT DESIGNED MAP TO THE LEVEL FOR USER TO PLAY
	def create_grid(self):
		'''
		Exports the level
		'''
		## empty the tile objects stored previously
		for tile in self.canvas_data.values():
			tile.objects = []
		
		## add objects to the tiles
		for object in self.canvas_objects:
			current_cell = self.get_current_cell(object)
			offset = vector(object.distance_to_origin) - (vector(current_cell) * TILE_SIZE) # how far is the topleft of the object from the origin(topleft) of the cell

			if current_cell in self.canvas_data: # tile exists already
				self.canvas_data[current_cell].add_id(object.tile_id, offset)
			else: # no tile exists yet
				self.canvas_data[current_cell] = CanvasTile(object.tile_id,  offset)
		
		## create grid
		# grid offset: For exporting tiles which really have objects/data and not other empty cells
		# top-left tile which is actually filled
		top  = (sorted(self.canvas_data.keys(), key = lambda tile: tile[1])[0])[1]
		left = (sorted(self.canvas_data.keys(), key = lambda tile: tile[0])[0])[0]
		# create empty grid
		layers = {
			'water': {}, # Ex item (pos of key: type): (128, 64): 'water top' / 'water bottom'
			'bg qcomps': {},
			'terrain': {}, # Ex item (pos of key: Filename): (128, 64): 'ABC'
			'enemies': {},
			'coins': {},
			'fg objects': {}
		}
		# fill the grid
		for tile_pos, tile in self.canvas_data.items():
			row_adjusted = tile_pos[1] - top
			col_adjusted = tile_pos[0] - left
			x = col_adjusted * TILE_SIZE
			y = row_adjusted * TILE_SIZE

			if tile.has_water:
				layers['water'][(x, y)] = tile.get_water()
			
			if tile.has_terrain:
				layers['terrain'][(x, y)] = tile.get_terrain() if tile.get_terrain() in self.land_tiles else 'X'
			
			if tile.coin:
				layers['coins'][(x + TILE_SIZE // 2, y + TILE_SIZE // 2)] = tile.coin #  '+ TILE_SIZE // 2' to make coin at the center of the tile
			
			if tile.enemy:
				layers['enemies'][(x, y)] = tile.enemy
			
			if tile.objects: # (object, offset  from the topleft)
				for obj, offset in tile.objects:
					if obj in [key for key, value in EDITOR_DATA.items() if value['style'] == 'qcomp_bg']: # bg qcomp; key = [15, 16, 17, 18]
						layers['bg qcomps'][(int(x + offset.x), int(y + offset.y))] = obj
					else: #fg objects
						layers['fg objects'][(int(x + offset.x), int(y + offset.y))] = obj
		
		return layers
	
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

			self.create_clouds(event)

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
			
			for sprite in self.canvas_objects: # update position of all sprites
				sprite.pan_position(self.origin)

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
		if event.type == pygame.MOUSEBUTTONDOWN:
			if self.menu.menu_area.collidepoint(mouse_postion()):
				self.selection_index = self.menu.click(mouse_postion(), mouse_buttons())
			
			# Save the Level When user press ENTER (EXPORT MAP AND CREATE ACTUAL LEVEL)
			if self.save_level_button.rect.collidepoint(mouse_postion()):
				if mouse_buttons()[2]: # right mouse click
					export_layer_data = self.create_grid()
					###################### INPUT #################
					self.saveloadmanager.save_data(export_layer_data, "level_2")
					self.create_overworld(self.current_level, self.new_max_level)

			# Switch to Play Mode When user press Play Button (EXPORT MAP AND CREATE ACTUAL LEVEL)
			# if self.play_level_button.rect.collidepoint(mouse_postion()):
			# 	if mouse_buttons()[2]: # right mouse click
			# 		self.editor_music.stop()
			# 		export_layer_data = self.create_grid()
			# 		self.switch(export_layer_data)

	def canvas_add(self):
		if (
			mouse_buttons()[0] and 
			not self.menu.menu_area.collidepoint(mouse_postion()) and 
			not self.save_level_button.rect.collidepoint(mouse_postion()) and 
			not self.object_drag_active
		): # if we are left clicking outside the menu area and we have not selected any object(Player, Trees)
			current_cell = self.get_current_cell()

			if EDITOR_DATA[self.selection_index]['type'] == 'tile': ## ADD TILE
				if current_cell != self.last_selected_cell:
					if current_cell in self.canvas_data:
						self.canvas_data[current_cell].add_id(self.selection_index)
					else:
						self.canvas_data[current_cell] = CanvasTile(self.selection_index)
					
					self.check_neighbours(current_cell)
					self.last_selected_cell = current_cell
			
			else: ## ADD CANVAS OBJECT
				if not self.object_timer.active:
					groups = [self.canvas_objects, self.background_objects] if EDITOR_DATA[self.selection_index]['style'] == 'qcomp_bg' else [self.canvas_objects, self.foreground_objects] 
					CanvasObject(
						pos = mouse_postion(), 
						frames = self.animations[self.selection_index]['frames'], 
						tile_id = self.selection_index, 
						origin = self.origin, 
						group = groups
					)
					self.object_timer.activate()

	def canvas_remove(self):

		if (
			mouse_buttons()[2] and 
			not self.menu.menu_area.collidepoint(mouse_postion()) and 
			not self.save_level_button.rect.collidepoint(mouse_postion())
		): # if we are right clicking outside the menu area
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
					
					self.check_neighbours(current_cell)

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
		# Draw background objects (Background QComps, Sky Handle)
		self.background_objects.draw(self.editor_display_surface)
		
		# Draw Tiles (Terrain, Water, Coin, Enemy)
		for cell_pos, tile in self.canvas_data.items():
			pos = self.origin + vector(cell_pos) * TILE_SIZE

			## terrain
			if tile.has_terrain:
				terrain_string = ''.join(tile.terrain_neighbours)
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

		# Draw foreground objects (Foreground QComps, Player)
		self.foreground_objects.draw(self.editor_display_surface)

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

	def display_sky(self, dt):
		horizon_y = self.sky_handle.rect.centery
		self.editor_display_surface.fill(SKY_COLOR)

		if horizon_y > 0:
			## Horizon Lines
			horizon_rect_1 = pygame.Rect(0, horizon_y - 10, WINDOW_WIDTH, 10)
			horizon_rect_2 = pygame.Rect(0, horizon_y - 16, WINDOW_WIDTH, 4)
			horizon_rect_3 = pygame.Rect(0, horizon_y - 20, WINDOW_WIDTH, 2)
			pygame.draw.rect(self.editor_display_surface, HORIZON_TOP_COLOR, horizon_rect_1)
			pygame.draw.rect(self.editor_display_surface, HORIZON_TOP_COLOR, horizon_rect_2)
			pygame.draw.rect(self.editor_display_surface, HORIZON_TOP_COLOR, horizon_rect_3)
			pygame.draw.line(self.editor_display_surface, HORIZON_COLOR, (0, horizon_y), (WINDOW_WIDTH, horizon_y), 3)
		
			## Clouds
			self.display_clouds(dt, horizon_y)

		## Sea
		if 0 < horizon_y < WINDOW_HEIGHT: # if horizon is on the screen:
			sea_rect = pygame.Rect(0, horizon_y, WINDOW_WIDTH, WINDOW_WIDTH)
			pygame.draw.rect(self.editor_display_surface, SEA_COLOR, sea_rect)
		if horizon_y < 0: # else fill the entire screen with water
			self.editor_display_surface.fill(SEA_COLOR)

	def display_bg(self):
		size = pygame.transform.scale(self.bg_lvl1,(1280,720))
		self.editor_display_surface.blit(size,(0,0))

	def create_clouds(self, event):
		if event.type == self.cloud_timer:
			## Create New Clouds on the right side of window
			cloud_surface = choice(self.cloud_surfaces) # randomly select a cloud from all types of cloud surfaces available
			#print("alpha:",cloud_surface.get_alpha())
			cloud_surface.set_alpha(50)
			cloud_surface = pygame.transform.scale2x(cloud_surface) if randint(0, 4) < 2 else cloud_surface # scale this cloud surfaces by 2x randomly
			
			cloud_position = [WINDOW_WIDTH + randint(50, 100), randint(0, WINDOW_HEIGHT)]
			cloud_speed = randint(20, 50)
			self.current_clouds.append({
				'surface': cloud_surface,
				'position': cloud_position,
				'speed': cloud_speed
			})

			## Delete clouds which passes the left side of window
			self.current_clouds = [cloud for cloud in self.current_clouds if cloud['position'][0] > -400]
	
	def startup_clouds(self): # To have some clouds initially as we start the editor
		for counter in range(15):
			cloud_surface = choice(self.cloud_surfaces) # randomly select a cloud from all types of cloud surfaces available
			cloud_surface = pygame.transform.scale2x(cloud_surface) if randint(0, 4) < 2 else cloud_surface # scale this cloud surfaces by 2x randomly
			cloud_surface.set_alpha(50)
			cloud_position = [randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)]
			cloud_speed = randint(20, 50)
			self.current_clouds.append({
				'surface': cloud_surface,
				'position': cloud_position,
				'speed': cloud_speed
			})

	def display_clouds(self, dt, horizon_y):
		for cloud in self.current_clouds: # cloud.keys: {surface, position, speed}
			# Move the cloud towards left
			cloud['position'][0] -= cloud['speed'] * dt
			x = cloud['position'][0]
			y = horizon_y - cloud['position'][1] #to draw clouds relative to horizon
			self.editor_display_surface.blit(cloud['surface'], (x, y))

	### FUNCTION TO RUN & UPDATE EVERYTHING
	def run(self, dt):
		self.event_loop()

		## updating
		self.animation_update(dt)
		self.canvas_objects.update(dt)
		self.object_timer.update()

		## drawing
		self.editor_display_surface.fill('white')
		self.display_bg()
		self.display_clouds(dt,self.sky_handle.rect.centery)

		self.draw_level()
		self.draw_grid_lines()
		# pygame.draw.circle(self.editor_display_surface, 'red', self.origin, 10)
		self.preview()
		self.menu.display(self.selection_index)
		self.save_level_button.display()
		self.play_level_button.display()

class CanvasTile:
	def __init__(self, tile_id, object_offset_from_tile_origin = vector()):
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

		## objects
		self.objects = []

		self.add_id(tile_id, offset = object_offset_from_tile_origin)

	def add_id(self, tile_id, offset = vector()):
		options = {key: value['style'] for key, value in EDITOR_DATA.items()}
		match options[tile_id]:
			case 'terrain': self.has_terrain = True
			case 'water': self.has_water = True
			case 'coin': self.coin = tile_id
			case 'enemy': self.enemy = tile_id
			case _: # handling objects
				if (tile_id, offset) not in self.objects:
					self.objects.append((tile_id, offset))

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
	
	def get_water(self):
		return 'bottom' if self.water_on_top else 'top'
	
	def get_terrain(self):
		return ''.join(self.terrain_neighbours)

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