# Game Constants
import pygame

# Window settings
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 60
GAME_TITLE = "Goggins Fitness Game"

# Tile settings
TILE_SIZE = 48
MAP_WIDTH = 25  # tiles
MAP_HEIGHT = 46  # tiles (10 pool + 18 gym + 18 outdoor)

# Stamina settings
BASE_STAMINA = 100
STAMINA_PER_ENDURANCE = 10
SPRINT_SPEED_MULTIPLIER = 1.8
STAMINA_DRAIN_RATE = 25  # per second
STAMINA_REGEN_RATE = 15  # per second
STAMINA_REGEN_DELAY = 0.5

# Swimming settings
SWIM_SPEED_MULTIPLIER = 0.6
SWIM_STAMINA_DRAIN = 10  # per second while swimming

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
BROWN = (139, 69, 19)
DARK_BROWN = (101, 67, 33)
LIGHT_BLUE = (135, 206, 235)
DARK_BLUE = (0, 0, 139)
PURPLE = (128, 0, 128)
SKIN_COLOR = (255, 213, 170)
DARK_SKIN = (210, 170, 130)
BLACK_SKIN = (89, 60, 40)
BLACK_SKIN_DARK = (65, 45, 30)

# Tile types
TILE_FLOOR = 0
TILE_WALL = 1
TILE_BENCH_PRESS = 2
TILE_SQUAT_RACK = 3
TILE_TREADMILL = 4
TILE_DUMBBELL = 5
TILE_SHOP = 6
TILE_TRAINER = 7
TILE_ENTRANCE = 8
TILE_MIRROR = 9
TILE_LOCKER = 10
TILE_PULLUP_BAR = 11
TILE_LAT_PULLDOWN = 12
TILE_CABLE_MACHINE = 13
TILE_OUTDOOR_DOOR = 14
TILE_GRASS = 15
TILE_TRACK = 16
TILE_FENCE = 17
TILE_TREE = 18
TILE_POOL_WATER = 19
TILE_POOL_EDGE = 20
TILE_POOL_FLOOR = 21
TILE_OUTDOOR_PULLUP = 22
TILE_OUTDOOR_BARS = 23
TILE_OUTDOOR_BENCH = 24
TILE_POOL_DOOR = 25

# Tile properties (walkable, interactive, name)
TILE_PROPERTIES = {
    TILE_FLOOR: {"walkable": True, "interactive": False, "name": "Floor"},
    TILE_WALL: {"walkable": False, "interactive": False, "name": "Wall"},
    TILE_BENCH_PRESS: {"walkable": False, "interactive": True, "name": "Bench Press", "stat": "strength", "xp": 15},
    TILE_SQUAT_RACK: {"walkable": False, "interactive": True, "name": "Squat Rack", "stat": "strength", "xp": 20},
    TILE_TREADMILL: {"walkable": False, "interactive": True, "name": "Treadmill", "stat": "endurance", "xp": 15},
    TILE_DUMBBELL: {"walkable": False, "interactive": True, "name": "Dumbbells", "stat": "strength", "xp": 10},
    TILE_SHOP: {"walkable": False, "interactive": True, "name": "Supplement Shop", "stat": None, "xp": 0},
    TILE_TRAINER: {"walkable": False, "interactive": True, "name": "Trainer Goggins", "stat": None, "xp": 0},
    TILE_ENTRANCE: {"walkable": True, "interactive": False, "name": "Entrance"},
    TILE_MIRROR: {"walkable": False, "interactive": True, "name": "Mirror", "stat": None, "xp": 0},
    TILE_LOCKER: {"walkable": False, "interactive": False, "name": "Locker"},
    TILE_PULLUP_BAR: {"walkable": False, "interactive": True, "name": "Pull-up Bar", "stat": "strength", "xp": 18},
    TILE_LAT_PULLDOWN: {"walkable": False, "interactive": True, "name": "Lat Pulldown", "stat": "strength", "xp": 15},
    TILE_CABLE_MACHINE: {"walkable": False, "interactive": True, "name": "Cable Machine", "stat": "strength", "xp": 12},
    TILE_OUTDOOR_DOOR: {"walkable": True, "interactive": False, "name": "Door"},
    TILE_GRASS: {"walkable": True, "interactive": False, "name": "Grass"},
    TILE_TRACK: {"walkable": True, "interactive": False, "name": "Track"},
    TILE_FENCE: {"walkable": False, "interactive": False, "name": "Fence"},
    TILE_TREE: {"walkable": False, "interactive": False, "name": "Tree"},
    TILE_POOL_WATER: {"walkable": True, "interactive": False, "name": "Pool", "is_water": True},
    TILE_POOL_EDGE: {"walkable": True, "interactive": False, "name": "Pool Edge"},
    TILE_POOL_FLOOR: {"walkable": True, "interactive": False, "name": "Pool Floor"},
    TILE_OUTDOOR_PULLUP: {"walkable": False, "interactive": False, "name": "Outdoor Pull-up"},
    TILE_OUTDOOR_BARS: {"walkable": False, "interactive": False, "name": "Parallel Bars"},
    TILE_OUTDOOR_BENCH: {"walkable": False, "interactive": False, "name": "Outdoor Bench"},
    TILE_POOL_DOOR: {"walkable": True, "interactive": False, "name": "Pool Door"},
}

# Player settings
PLAYER_SPEED = 4
PLAYER_SIZE = 40

# Player stats initial values
INITIAL_STATS = {
    "strength": 1,
    "endurance": 1,
    "speed": 1,
    "level": 1,
    "xp": 0,
    "currency": 100
}

# XP required per level (level: xp_needed)
XP_PER_LEVEL = {
    1: 0,
    2: 100,
    3: 250,
    4: 450,
    5: 700,
    6: 1000,
    7: 1400,
    8: 1900,
    9: 2500,
    10: 3200
}

# Muscle level thresholds (based on total strength)
MUSCLE_LEVELS = {
    1: 0,    # Skinny
    2: 5,    # Slim
    3: 12,   # Average
    4: 22,   # Fit
    5: 35,   # Athletic
    6: 50,   # Muscular
    7: 70    # Jacked
}

# Shop items
SHOP_ITEMS = {
    "protein": {
        "name": "Protein Shake",
        "price": 50,
        "effect": "strength_xp_boost",
        "value": 1.5,
        "duration": 180,  # seconds
        "description": "+50% Strength XP for 3 min"
    },
    "preworkout": {
        "name": "Pre-Workout",
        "price": 75,
        "effect": "speed_boost",
        "value": 1.3,
        "duration": 120,
        "description": "+30% Speed for 2 min"
    },
    "creatine": {
        "name": "Creatine",
        "price": 100,
        "effect": "all_xp_boost",
        "value": 1.25,
        "duration": 300,
        "description": "+25% All XP for 5 min"
    },
    "energy_drink": {
        "name": "Energy Drink",
        "price": 30,
        "effect": "instant_xp",
        "value": 25,
        "duration": 0,
        "description": "Instant +25 XP"
    }
}

# UI Settings
UI_FONT_SIZE = 20
UI_TITLE_FONT_SIZE = 28
UI_PADDING = 10
UI_BAR_HEIGHT = 20
UI_BAR_WIDTH = 150

# Interaction distance (in pixels)
INTERACTION_DISTANCE = TILE_SIZE + 10

# Save file path
SAVE_FILE = "save_game.json"
