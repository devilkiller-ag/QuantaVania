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
	9:  {'style': 'enemy', 'type': 'tile', 'menu_type': 'enemy', 'menu_surf': 'graphics/menu/shoot_monster_left.png',  'preview': 'graphics/preview/shoot_monster_left.png',  'graphics': 'graphics/enemies/shoot_monster_left/idle'},
	10: {'style': 'enemy', 'type': 'tile', 'menu_type': 'enemy', 'menu_surf': 'graphics/menu/shoot_monster_right.png', 'preview': 'graphics/preview/shoot_monster_right.png', 'graphics': 'graphics/enemies/shoot_monster_right/idle'},
	
	11: {'style': 'qcomp_fg', 'type': 'object', 'menu_type': 'qcomp fg', 'menu_surf': 'graphics/menu/small_fg.png', 'preview': 'graphics/preview/small_fg.png', 'graphics': 'graphics/terrain/qcomp/small_fg'},
	12: {'style': 'qcomp_fg', 'type': 'object', 'menu_type': 'qcomp fg', 'menu_surf': 'graphics/menu/large_fg.png', 'preview': 'graphics/preview/large_fg.png', 'graphics': 'graphics/terrain/qcomp/large_fg'},
	13: {'style': 'qcomp_fg', 'type': 'object', 'menu_type': 'qcomp fg', 'menu_surf': 'graphics/menu/left_fg.png',  'preview': 'graphics/preview/left_fg.png',  'graphics': 'graphics/terrain/qcomp/left_fg'},
	14: {'style': 'qcomp_fg', 'type': 'object', 'menu_type': 'qcomp fg', 'menu_surf': 'graphics/menu/right_fg.png', 'preview': 'graphics/preview/right_fg.png', 'graphics': 'graphics/terrain/qcomp/right_fg'},

	15: {'style': 'qcomp_bg', 'type': 'object', 'menu_type': 'qcomp bg', 'menu_surf': 'graphics/menu/small_bg.png', 'preview': 'graphics/preview/small_bg.png', 'graphics': 'graphics/terrain/qcomp/small_bg'},
	16: {'style': 'qcomp_bg', 'type': 'object', 'menu_type': 'qcomp bg', 'menu_surf': 'graphics/menu/large_bg.png', 'preview': 'graphics/preview/large_bg.png', 'graphics': 'graphics/terrain/qcomp/large_bg'},
	17: {'style': 'qcomp_bg', 'type': 'object', 'menu_type': 'qcomp bg', 'menu_surf': 'graphics/menu/left_bg.png',  'preview': 'graphics/preview/left_bg.png',  'graphics': 'graphics/terrain/qcomp/left_bg'},
	18: {'style': 'qcomp_bg', 'type': 'object', 'menu_type': 'qcomp bg', 'menu_surf': 'graphics/menu/right_bg.png', 'preview': 'graphics/preview/right_bg.png', 'graphics': 'graphics/terrain/qcomp/right_bg'},
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
SKY_COLOR = '#27005d'
SEA_COLOR = '#92a9ce'
HORIZON_COLOR = '#f5f1de'
HORIZON_TOP_COLOR = '#d1aa9d'
LINE_COLOR = 'black'
BUTTON_BG_COLOR = '#33323d'
BUTTON_LINE_COLOR = '#f5f1de'
STATS_TEXT_COLOR = '#ffffff'
HEALTH_BAR_COLOR = '#7d3a47'
SHIELD_BAR_COLOR = '#4b527e'
QUANTUM_CIRCUIT_BG_COLOR = '#444654'
QUANTUM_CIRCUIT_WIRE_COLOR = '#ffffff'
QUANTUM_GATE_PHASE_COLOR = '#97ad40'
DIALOG_TEXT_COLOR = '#000000'

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

## LEVEL DIALOGUES
LEVEL_DIALOGUES = {
    'level_0': [
        "QuantaVania is an action-adventure 2D platformer game with the potential to evolve into an open-world sandbox game in which players can learn quantum computing from the ground up while playing, design their own game level and share it with others in the quantum community via our web platform, and mine qubits, quantum gates and power-ups. \nOur game will not only allow them to run the game on their local device but also on real quantum computers and simulators from various quantum computing providers like IBM Quantum, IONQ, Rigetti Computing, etc.",
        
        "We intend to teach the player quantum computing as they go through the levels. We'll expose them to qubits in the first level, and then they'll have to find the X-Gate hiding behind any box or monster. As the levels progresses, the player will discover new gates that he may use in the gun circuit. And, at the end of each level, we will introduce to the user each quantum algorithm, from basic to advanced, in the form of a game problem.",
    ],
    'level_1': [
        "This is \nQuantaVania \n Level 2: Dialogue 1!",
        "This is \nQuantaVania \n Level 2: Dialogue 2!",
        "This is \nQuantaVania \n Level 2: Dialogue 3!",
    ],
    'level_2': [
        "This is \nQuantaVania \n Level 3: Dialogue 1!",
        "This is \nQuantaVania \n Level 3: Dialogue 2!",
        "This is \nQuantaVania \n Level 3: Dialogue 3!",
    ],
    'level_3': [
        "This is \nQuantaVania \n Level 4: Dialogue 1!",
        "This is \nQuantaVania \n Level 4: Dialogue 2!",
        "This is \nQuantaVania \n Level 4: Dialogue 3!",
    ],
    'level_4': [
        "This is \nQuantaVania \n Level 5: Dialogue 1!",
        "This is \nQuantaVania \n Level 5: Dialogue 2!",
        "This is \nQuantaVania \n Level 5: Dialogue 3!",
    ],
}

PARAMETER_RANGE = {
    "pr1002.tsp": (4375,2187),
    "pr2392.tsp": (1875,937),
    "rat195.tsp": (100,15)
}