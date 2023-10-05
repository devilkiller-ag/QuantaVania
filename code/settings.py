# general setup
TILE_SIZE = 64
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
ANIMATION_SPEED = 8
OBJECT_PLACING_DELAY_TIME = 400 # To restrict player to draw another object (tree) just after placing first one. This will avoid the placing of thousands of objects (trees) on just draging the mouse after placing the first object (tree).
GRAVITY = 4

# editor graphics 
EDITOR_DATA = {
	0: {'style': 'player', 'type': 'object', 'menu_type': None, 'menu_surf': None, 'preview': None, 'graphics': 'graphics/player/idle_right'},
	1: {'style': 'sky',    'type': 'object', 'menu_type': None, 'menu_surf': None, 'preview': None, 'graphics': None},
	
	2: {'style': 'terrain', 'type': 'tile', 'menu_type': 'terrain', 'menu_surf': 'graphics/menu/land.png',  'preview': 'graphics/preview/land.png',  'graphics': None},
	3: {'style': 'water',   'type': 'tile', 'menu_type': 'terrain', 'menu_surf': 'graphics/menu/water.png', 'preview': 'graphics/preview/water.png', 'graphics': 'graphics/terrain/water/animation'},
	
	4: {'style': 'coin', 'type': 'tile', 'menu_type': 'coin', 'menu_surf': 'graphics/menu/gold.png',    'preview': 'graphics/preview/gold.png',    'graphics': 'graphics/items/gold'},
	5: {'style': 'coin', 'type': 'tile', 'menu_type': 'coin', 'menu_surf': 'graphics/menu/silver.png',  'preview': 'graphics/preview/silver.png',  'graphics': 'graphics/items/silver'},
	6: {'style': 'coin', 'type': 'tile', 'menu_type': 'coin', 'menu_surf': 'graphics/menu/diamond.png', 'preview': 'graphics/preview/diamond.png', 'graphics': 'graphics/items/diamond'},

	7:  {'style': 'enemy', 'type': 'tile', 'menu_type': 'enemy', 'menu_surf': 'graphics/menu/spikes.png',      'preview': 'graphics/preview/spikes.png',      'graphics': 'graphics/enemies/spikes'},
	8:  {'style': 'enemy', 'type': 'tile', 'menu_type': 'enemy', 'menu_surf': 'graphics/menu/crab_monster.png',       'preview': 'graphics/preview/crab_monster.png',       'graphics': 'graphics/enemies/crab_monster/idle'},
	9:  {'style': 'enemy', 'type': 'tile', 'menu_type': 'enemy', 'menu_surf': 'graphics/menu/shell_left.png',  'preview': 'graphics/preview/shell_left.png',  'graphics': 'graphics/enemies/shell_left/idle'},
	10: {'style': 'enemy', 'type': 'tile', 'menu_type': 'enemy', 'menu_surf': 'graphics/menu/shell_right.png', 'preview': 'graphics/preview/shell_right.png', 'graphics': 'graphics/enemies/shell_right/idle'},
	
	11: {'style': 'palm_fg', 'type': 'object', 'menu_type': 'palm fg', 'menu_surf': 'graphics/menu/small_fg.png', 'preview': 'graphics/preview/small_fg.png', 'graphics': 'graphics/terrain/palm/small_fg'},
	12: {'style': 'palm_fg', 'type': 'object', 'menu_type': 'palm fg', 'menu_surf': 'graphics/menu/large_fg.png', 'preview': 'graphics/preview/large_fg.png', 'graphics': 'graphics/terrain/palm/large_fg'},
	13: {'style': 'palm_fg', 'type': 'object', 'menu_type': 'palm fg', 'menu_surf': 'graphics/menu/left_fg.png',  'preview': 'graphics/preview/left_fg.png',  'graphics': 'graphics/terrain/palm/left_fg'},
	14: {'style': 'palm_fg', 'type': 'object', 'menu_type': 'palm fg', 'menu_surf': 'graphics/menu/right_fg.png', 'preview': 'graphics/preview/right_fg.png', 'graphics': 'graphics/terrain/palm/right_fg'},

	15: {'style': 'palm_bg', 'type': 'object', 'menu_type': 'palm bg', 'menu_surf': 'graphics/menu/small_bg.png', 'preview': 'graphics/preview/small_bg.png', 'graphics': 'graphics/terrain/palm/small_bg'},
	16: {'style': 'palm_bg', 'type': 'object', 'menu_type': 'palm bg', 'menu_surf': 'graphics/menu/large_bg.png', 'preview': 'graphics/preview/large_bg.png', 'graphics': 'graphics/terrain/palm/large_bg'},
	17: {'style': 'palm_bg', 'type': 'object', 'menu_type': 'palm bg', 'menu_surf': 'graphics/menu/left_bg.png',  'preview': 'graphics/preview/left_bg.png',  'graphics': 'graphics/terrain/palm/left_bg'},
	18: {'style': 'palm_bg', 'type': 'object', 'menu_type': 'palm bg', 'menu_surf': 'graphics/menu/right_bg.png', 'preview': 'graphics/preview/right_bg.png', 'graphics': 'graphics/terrain/palm/right_bg'},
}

'''
NEIGHBOR CODE IS SET AS:

	H A B
    G @ C
    F E D
    
where @ is the target cell whose neighbors are to be reffered
''' 
NEIGHBOR_DIRECTIONS = {
	'A': (0,-1),
	'B': (1,-1),
	'C': (1,0),
	'D': (1,1),
	'E': (0,1),
	'F': (-1,1),
	'G': (-1,0),
	'H': (-1,-1)
}

LEVEL_LAYERS = {
	'clouds': 1,
	'ocean': 2,
	'bg': 3,
	'water': 4,
	'main': 5
}

# colors 
SKY_COLOR = '#ddc6a1'
SEA_COLOR = '#92a9ce'
HORIZON_COLOR = '#f5f1de'
HORIZON_TOP_COLOR = '#d1aa9d'
LINE_COLOR = 'black'
BUTTON_BG_COLOR = '#33323d'
BUTTON_LINE_COLOR = '#f5f1de'
QUANTUM_CIRCUIT_BG_COLOR = '#444654'
QUANTUM_CIRCUIT_WIRE_COLOR = '#ffffff'
QUANTUM_GATE_PHASE_COLOR = '#97ad40'

# player settings
PLAYER_SPEED = 300

# buttons
BUTTON_SIZE = 50
BUTTON_MARGIN = 6

# Overworld
OVERWORLD_NODE_POSITIONS = [(110,400), (300,220), (480,610), (610,350), (880,210), (1050,400)]

# Saving Levels Settings
SAVE_FILE_EXTENSION = '.qvania'
SAVE_FOLDER_NAME = 'saved_levels'

## Quantum Circuit Grid for Player/Enemy Shooting
BASIS_STATES = {
    1: [
        '|0>', 
        '|1>'
    ],
    2: [
        '|00>',
        '|01>',
        '|10>',
        '|11>'
    ],
    3: [
        '|000>',
        '|001>',
        '|010>',
        '|011>',
        '|100>',
        '|101>',
        '|110>',
        '|111>'
    ]
}

GATES = {
    'EMPTY': 0,
    'IDENTITY': 1,
    'X': 2,
    'Y': 3,
    'Z': 4,
    'S': 5,
    'SDG': 6,
    'T': 7,
    'TDG': 8,
    'H': 9,
    'SWAP': 10,
    'CTRL': 11, # "control" part of multi-qubit gate
    'CTRL_LINE': 12 # The Vertical Line between a gate part and a "control" or "swap" part
}

QUANTUM_CIRCUIT_TILE_SIZE = 36
GATE_TILE_WIDTH = 24
GATE_TILE_HIEGHT = 24
WIRE_LINE_WIDTH = 1

QUANTUM_CIRCUIT_MARKER_MOVE_LEFT = 1
QUANTUM_CIRCUIT_MARKER_MOVE_RIGHT = 2
QUANTUM_CIRCUIT_MARKER_MOVE_UP = 3
QUANTUM_CIRCUIT_MARKER_MOVE_DOWN = 4