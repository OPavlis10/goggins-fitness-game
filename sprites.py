"""
Sprite Generator - Creates pixel art sprites programmatically using Pygame
"""
import pygame
from constants import *


class SpriteGenerator:
    """Generates all game sprites as pygame Surfaces"""

    def __init__(self):
        self.tile_sprites = {}
        self.player_sprites = {}  # {muscle_level: {direction: surface}}
        self.npc_sprites = {}  # {muscle_level: {direction: {color_variant: surface}}}
        self.ui_sprites = {}
        self._generate_all()

    def _generate_all(self):
        """Generate all sprites"""
        self._generate_tile_sprites()
        self._generate_player_sprites()
        self._generate_npc_sprites()
        self._generate_ui_sprites()

    def _generate_tile_sprites(self):
        """Generate tile sprites for the map"""
        # Floor - gray tiles with subtle pattern
        floor = pygame.Surface((TILE_SIZE, TILE_SIZE))
        floor.fill(LIGHT_GRAY)
        pygame.draw.rect(floor, GRAY, (0, 0, TILE_SIZE, TILE_SIZE), 1)
        # Add subtle texture
        for i in range(0, TILE_SIZE, 8):
            pygame.draw.line(floor, (180, 180, 180), (i, 0), (i, TILE_SIZE), 1)
            pygame.draw.line(floor, (180, 180, 180), (0, i), (TILE_SIZE, i), 1)
        self.tile_sprites[TILE_FLOOR] = floor

        # Wall - dark brick pattern
        wall = pygame.Surface((TILE_SIZE, TILE_SIZE))
        wall.fill(DARK_BROWN)
        # Brick pattern
        brick_h = TILE_SIZE // 4
        brick_w = TILE_SIZE // 2
        for row in range(4):
            offset = brick_w // 2 if row % 2 else 0
            for col in range(-1, 3):
                x = col * brick_w + offset
                y = row * brick_h
                pygame.draw.rect(wall, BROWN, (x + 1, y + 1, brick_w - 2, brick_h - 2))
        self.tile_sprites[TILE_WALL] = wall

        # Bench Press - blue bench with barbell
        bench = pygame.Surface((TILE_SIZE, TILE_SIZE))
        bench.fill(LIGHT_GRAY)
        pygame.draw.rect(bench, GRAY, (0, 0, TILE_SIZE, TILE_SIZE), 1)
        # Bench
        pygame.draw.rect(bench, DARK_BLUE, (8, 16, TILE_SIZE - 16, 16))
        # Barbell
        pygame.draw.rect(bench, DARK_GRAY, (4, 20, TILE_SIZE - 8, 4))
        # Weights
        pygame.draw.circle(bench, BLACK, (8, 22), 6)
        pygame.draw.circle(bench, BLACK, (TILE_SIZE - 8, 22), 6)
        self.tile_sprites[TILE_BENCH_PRESS] = bench

        # Squat Rack - metal rack with bar
        squat = pygame.Surface((TILE_SIZE, TILE_SIZE))
        squat.fill(LIGHT_GRAY)
        pygame.draw.rect(squat, GRAY, (0, 0, TILE_SIZE, TILE_SIZE), 1)
        # Uprights
        pygame.draw.rect(squat, DARK_GRAY, (8, 4, 6, 40))
        pygame.draw.rect(squat, DARK_GRAY, (TILE_SIZE - 14, 4, 6, 40))
        # Bar
        pygame.draw.rect(squat, GRAY, (6, 14, TILE_SIZE - 12, 4))
        # Weights
        pygame.draw.rect(squat, BLACK, (2, 10, 6, 12))
        pygame.draw.rect(squat, BLACK, (TILE_SIZE - 8, 10, 6, 12))
        self.tile_sprites[TILE_SQUAT_RACK] = squat

        # Treadmill - running machine
        treadmill = pygame.Surface((TILE_SIZE, TILE_SIZE))
        treadmill.fill(LIGHT_GRAY)
        pygame.draw.rect(treadmill, GRAY, (0, 0, TILE_SIZE, TILE_SIZE), 1)
        # Base
        pygame.draw.rect(treadmill, DARK_GRAY, (6, 20, TILE_SIZE - 12, 24))
        # Belt
        pygame.draw.rect(treadmill, BLACK, (8, 24, TILE_SIZE - 16, 16))
        # Belt lines
        for i in range(3):
            pygame.draw.line(treadmill, DARK_GRAY, (12 + i*10, 26), (12 + i*10, 38), 2)
        # Console
        pygame.draw.rect(treadmill, RED, (14, 6, 20, 12))
        pygame.draw.rect(treadmill, GREEN, (18, 10, 4, 4))
        self.tile_sprites[TILE_TREADMILL] = treadmill

        # Dumbbells - rack with weights
        dumbbell = pygame.Surface((TILE_SIZE, TILE_SIZE))
        dumbbell.fill(LIGHT_GRAY)
        pygame.draw.rect(dumbbell, GRAY, (0, 0, TILE_SIZE, TILE_SIZE), 1)
        # Rack
        pygame.draw.rect(dumbbell, DARK_GRAY, (4, 8, TILE_SIZE - 8, 32))
        # Dumbbells on rack
        colors = [BLACK, DARK_GRAY, BLUE]
        for i, color in enumerate(colors):
            y = 12 + i * 10
            pygame.draw.circle(dumbbell, color, (12, y), 4)
            pygame.draw.rect(dumbbell, GRAY, (14, y - 2, 16, 4))
            pygame.draw.circle(dumbbell, color, (TILE_SIZE - 12, y), 4)
        self.tile_sprites[TILE_DUMBBELL] = dumbbell

        # Shop - supplement store counter
        shop = pygame.Surface((TILE_SIZE, TILE_SIZE))
        shop.fill(LIGHT_GRAY)
        pygame.draw.rect(shop, GRAY, (0, 0, TILE_SIZE, TILE_SIZE), 1)
        # Counter
        pygame.draw.rect(shop, BROWN, (4, 16, TILE_SIZE - 8, 28))
        pygame.draw.rect(shop, DARK_BROWN, (4, 16, TILE_SIZE - 8, 4))
        # Bottles/products
        pygame.draw.rect(shop, RED, (10, 8, 8, 12))
        pygame.draw.rect(shop, GREEN, (22, 8, 8, 12))
        pygame.draw.rect(shop, BLUE, (34, 8, 8, 12))
        # $ sign
        pygame.draw.circle(shop, YELLOW, (TILE_SIZE // 2, 32), 8)
        self.tile_sprites[TILE_SHOP] = shop

        # Trainer - David Goggins (muscular dark-skinned NPC)
        trainer = pygame.Surface((TILE_SIZE, TILE_SIZE))
        trainer.fill(LIGHT_GRAY)
        pygame.draw.rect(trainer, GRAY, (0, 0, TILE_SIZE, TILE_SIZE), 1)

        center_x = TILE_SIZE // 2
        # Head - dark skin
        pygame.draw.circle(trainer, BLACK_SKIN, (center_x, 10), 6)
        # Bald head shine
        pygame.draw.circle(trainer, BLACK_SKIN_DARK, (center_x - 2, 8), 2)
        # Eyes - intense look
        pygame.draw.circle(trainer, WHITE, (center_x - 2, 10), 1)
        pygame.draw.circle(trainer, WHITE, (center_x + 2, 10), 1)

        # Muscular body - black tank top
        body_width = 20
        pygame.draw.rect(trainer, BLACK, (center_x - body_width//2, 16, body_width, 16))

        # Muscular arms - dark skin
        arm_thickness = 6
        pygame.draw.rect(trainer, BLACK_SKIN, (center_x - 14, 17, arm_thickness, 14))
        pygame.draw.rect(trainer, BLACK_SKIN, (center_x + 8, 17, arm_thickness, 14))
        # Bicep definition
        pygame.draw.circle(trainer, BLACK_SKIN_DARK, (center_x - 11, 22), 3)
        pygame.draw.circle(trainer, BLACK_SKIN_DARK, (center_x + 11, 22), 3)

        # Shorts
        pygame.draw.rect(trainer, DARK_GRAY, (center_x - 8, 32, 16, 8))

        # Legs - dark skin
        pygame.draw.rect(trainer, BLACK_SKIN, (center_x - 7, 40, 5, 6))
        pygame.draw.rect(trainer, BLACK_SKIN, (center_x + 2, 40, 5, 6))

        self.tile_sprites[TILE_TRAINER] = trainer

        # Entrance - door
        entrance = pygame.Surface((TILE_SIZE, TILE_SIZE))
        entrance.fill(LIGHT_GRAY)
        pygame.draw.rect(entrance, DARK_BROWN, (8, 0, TILE_SIZE - 16, TILE_SIZE))
        pygame.draw.rect(entrance, BROWN, (12, 4, TILE_SIZE - 24, TILE_SIZE - 8))
        # Door handle
        pygame.draw.circle(entrance, YELLOW, (TILE_SIZE - 16, TILE_SIZE // 2), 3)
        self.tile_sprites[TILE_ENTRANCE] = entrance

        # Mirror
        mirror = pygame.Surface((TILE_SIZE, TILE_SIZE))
        mirror.fill(LIGHT_GRAY)
        pygame.draw.rect(mirror, GRAY, (0, 0, TILE_SIZE, TILE_SIZE), 1)
        # Mirror frame
        pygame.draw.rect(mirror, BROWN, (4, 4, TILE_SIZE - 8, TILE_SIZE - 8), 3)
        # Mirror surface
        pygame.draw.rect(mirror, LIGHT_BLUE, (8, 8, TILE_SIZE - 16, TILE_SIZE - 16))
        # Reflection lines
        pygame.draw.line(mirror, WHITE, (12, 12), (20, 20), 2)
        pygame.draw.line(mirror, WHITE, (12, 16), (16, 20), 2)
        self.tile_sprites[TILE_MIRROR] = mirror

        # Locker
        locker = pygame.Surface((TILE_SIZE, TILE_SIZE))
        locker.fill(LIGHT_GRAY)
        pygame.draw.rect(locker, GRAY, (0, 0, TILE_SIZE, TILE_SIZE), 1)
        # Locker body
        pygame.draw.rect(locker, DARK_BLUE, (6, 4, TILE_SIZE - 12, TILE_SIZE - 8))
        pygame.draw.rect(locker, BLUE, (8, 6, TILE_SIZE - 16, TILE_SIZE - 12))
        # Locker line (door seam)
        pygame.draw.line(locker, DARK_BLUE, (TILE_SIZE // 2, 6), (TILE_SIZE // 2, TILE_SIZE - 6), 2)
        # Handles
        pygame.draw.rect(locker, GRAY, (TILE_SIZE // 2 - 6, 20, 4, 8))
        pygame.draw.rect(locker, GRAY, (TILE_SIZE // 2 + 2, 20, 4, 8))
        self.tile_sprites[TILE_LOCKER] = locker

        # Pull-up Bar - two uprights with horizontal bar
        pullup = pygame.Surface((TILE_SIZE, TILE_SIZE))
        pullup.fill(LIGHT_GRAY)
        pygame.draw.rect(pullup, GRAY, (0, 0, TILE_SIZE, TILE_SIZE), 1)
        # Left upright
        pygame.draw.rect(pullup, DARK_GRAY, (8, 6, 6, 36))
        # Right upright
        pygame.draw.rect(pullup, DARK_GRAY, (TILE_SIZE - 14, 6, 6, 36))
        # Horizontal bar
        pygame.draw.rect(pullup, GRAY, (8, 8, TILE_SIZE - 16, 4))
        # Bar grip texture
        for i in range(3):
            pygame.draw.line(pullup, BLACK, (14 + i * 8, 8), (14 + i * 8, 12), 1)
        self.tile_sprites[TILE_PULLUP_BAR] = pullup

        # Lat Pulldown - machine with pulley and seat
        lat = pygame.Surface((TILE_SIZE, TILE_SIZE))
        lat.fill(LIGHT_GRAY)
        pygame.draw.rect(lat, GRAY, (0, 0, TILE_SIZE, TILE_SIZE), 1)
        # Weight stack
        pygame.draw.rect(lat, DARK_GRAY, (4, 4, 12, 32))
        for i in range(6):
            pygame.draw.rect(lat, BLACK, (5, 6 + i * 5, 10, 3))
        # Frame
        pygame.draw.rect(lat, DARK_GRAY, (16, 4, 4, 8))
        # Cable
        pygame.draw.line(lat, GRAY, (18, 12), (TILE_SIZE - 10, 12), 2)
        # Pulley
        pygame.draw.circle(lat, GRAY, (TILE_SIZE - 10, 12), 4)
        pygame.draw.circle(lat, BLACK, (TILE_SIZE - 10, 12), 4, 1)
        # Bar handle
        pygame.draw.rect(lat, GRAY, (TILE_SIZE - 20, 18, 16, 3))
        # Seat
        pygame.draw.rect(lat, DARK_BLUE, (20, 32, 20, 10))
        self.tile_sprites[TILE_LAT_PULLDOWN] = lat

        # Cable Machine - tower with cables and handle
        cable = pygame.Surface((TILE_SIZE, TILE_SIZE))
        cable.fill(LIGHT_GRAY)
        pygame.draw.rect(cable, GRAY, (0, 0, TILE_SIZE, TILE_SIZE), 1)
        # Main tower
        pygame.draw.rect(cable, DARK_GRAY, (8, 4, TILE_SIZE - 16, 36))
        # Weight stack inside
        for i in range(5):
            pygame.draw.rect(cable, BLACK, (12, 8 + i * 6, TILE_SIZE - 24, 4))
        # Pulley wheels
        pygame.draw.circle(cable, GRAY, (TILE_SIZE // 2, 8), 4)
        pygame.draw.circle(cable, GRAY, (TILE_SIZE // 2, TILE_SIZE - 10), 4)
        # Cable
        pygame.draw.line(cable, YELLOW, (TILE_SIZE // 2, 12), (TILE_SIZE // 2, TILE_SIZE - 14), 2)
        # Handle
        pygame.draw.rect(cable, GRAY, (TILE_SIZE // 2 - 8, TILE_SIZE - 14, 16, 4))
        self.tile_sprites[TILE_CABLE_MACHINE] = cable

        # Outdoor Door - brown door with window
        outdoor_door = pygame.Surface((TILE_SIZE, TILE_SIZE))
        outdoor_door.fill(LIGHT_GRAY)
        pygame.draw.rect(outdoor_door, GRAY, (0, 0, TILE_SIZE, TILE_SIZE), 1)
        # Door frame
        pygame.draw.rect(outdoor_door, DARK_BROWN, (6, 0, TILE_SIZE - 12, TILE_SIZE))
        # Door
        pygame.draw.rect(outdoor_door, BROWN, (8, 2, TILE_SIZE - 16, TILE_SIZE - 4))
        # Window
        pygame.draw.rect(outdoor_door, LIGHT_BLUE, (14, 8, 20, 16))
        pygame.draw.rect(outdoor_door, DARK_BROWN, (14, 8, 20, 16), 2)
        # Cross pattern
        pygame.draw.line(outdoor_door, DARK_BROWN, (24, 8), (24, 24), 2)
        pygame.draw.line(outdoor_door, DARK_BROWN, (14, 16), (34, 16), 2)
        # Handle
        pygame.draw.circle(outdoor_door, YELLOW, (TILE_SIZE - 14, TILE_SIZE // 2 + 4), 3)
        self.tile_sprites[TILE_OUTDOOR_DOOR] = outdoor_door

        # Grass - green with texture
        grass = pygame.Surface((TILE_SIZE, TILE_SIZE))
        grass.fill((60, 140, 60))  # Base green
        # Grass texture
        import random
        random.seed(42)  # Consistent pattern
        for _ in range(20):
            x = random.randint(0, TILE_SIZE - 2)
            y = random.randint(0, TILE_SIZE - 2)
            shade = random.randint(-20, 20)
            pygame.draw.line(grass, (60 + shade, 140 + shade, 60 + shade), (x, y), (x, y + 3), 1)
        pygame.draw.rect(grass, (50, 120, 50), (0, 0, TILE_SIZE, TILE_SIZE), 1)
        self.tile_sprites[TILE_GRASS] = grass

        # Track - red/brown running track with white lines
        track = pygame.Surface((TILE_SIZE, TILE_SIZE))
        track.fill((180, 90, 70))  # Terracotta color
        # Lane lines
        pygame.draw.line(track, WHITE, (0, 8), (TILE_SIZE, 8), 2)
        pygame.draw.line(track, WHITE, (0, TILE_SIZE - 8), (TILE_SIZE, TILE_SIZE - 8), 2)
        # Subtle texture
        for i in range(0, TILE_SIZE, 6):
            pygame.draw.line(track, (160, 80, 60), (i, 0), (i, TILE_SIZE), 1)
        self.tile_sprites[TILE_TRACK] = track

        # Fence - metal fence
        fence = pygame.Surface((TILE_SIZE, TILE_SIZE))
        fence.fill((60, 140, 60))  # Grass background
        # Fence posts
        pygame.draw.rect(fence, DARK_GRAY, (4, 8, 4, 32))
        pygame.draw.rect(fence, DARK_GRAY, (TILE_SIZE - 8, 8, 4, 32))
        # Horizontal bars
        pygame.draw.line(fence, GRAY, (0, 14), (TILE_SIZE, 14), 3)
        pygame.draw.line(fence, GRAY, (0, 28), (TILE_SIZE, 28), 3)
        # Chain link pattern
        for i in range(0, TILE_SIZE, 8):
            pygame.draw.line(fence, (100, 100, 100), (i, 10), (i + 4, 32), 1)
            pygame.draw.line(fence, (100, 100, 100), (i + 4, 10), (i, 32), 1)
        self.tile_sprites[TILE_FENCE] = fence

        # Tree - trunk with green canopy
        tree = pygame.Surface((TILE_SIZE, TILE_SIZE))
        tree.fill((60, 140, 60))  # Grass background
        # Trunk
        pygame.draw.rect(tree, DARK_BROWN, (TILE_SIZE // 2 - 4, 24, 8, 20))
        pygame.draw.rect(tree, BROWN, (TILE_SIZE // 2 - 3, 26, 4, 16))
        # Canopy (layered circles)
        pygame.draw.circle(tree, (30, 100, 30), (TILE_SIZE // 2 - 6, 18), 10)
        pygame.draw.circle(tree, (30, 100, 30), (TILE_SIZE // 2 + 6, 18), 10)
        pygame.draw.circle(tree, (40, 120, 40), (TILE_SIZE // 2, 12), 12)
        pygame.draw.circle(tree, (50, 130, 50), (TILE_SIZE // 2, 14), 8)
        self.tile_sprites[TILE_TREE] = tree

        # Pool Water - blue with wave pattern
        pool_water = pygame.Surface((TILE_SIZE, TILE_SIZE))
        pool_water.fill((40, 120, 200))  # Pool blue
        # Wave pattern
        for i in range(0, TILE_SIZE, 8):
            pygame.draw.arc(pool_water, (80, 160, 220), (i - 4, 8, 16, 10), 0, 3.14, 2)
            pygame.draw.arc(pool_water, (80, 160, 220), (i - 4, 24, 16, 10), 0, 3.14, 2)
            pygame.draw.arc(pool_water, (80, 160, 220), (i - 4, 40, 16, 10), 0, 3.14, 2)
        self.tile_sprites[TILE_POOL_WATER] = pool_water

        # Pool Edge - white tile border
        pool_edge = pygame.Surface((TILE_SIZE, TILE_SIZE))
        pool_edge.fill((220, 220, 230))  # Light pool tile
        pygame.draw.rect(pool_edge, (200, 200, 210), (0, 0, TILE_SIZE, TILE_SIZE), 2)
        # Tile pattern
        pygame.draw.line(pool_edge, (190, 190, 200), (TILE_SIZE//2, 0), (TILE_SIZE//2, TILE_SIZE), 1)
        pygame.draw.line(pool_edge, (190, 190, 200), (0, TILE_SIZE//2), (TILE_SIZE, TILE_SIZE//2), 1)
        self.tile_sprites[TILE_POOL_EDGE] = pool_edge

        # Pool Floor - light blue tiles
        pool_floor = pygame.Surface((TILE_SIZE, TILE_SIZE))
        pool_floor.fill((180, 210, 230))  # Light blue
        pygame.draw.rect(pool_floor, (160, 190, 210), (0, 0, TILE_SIZE, TILE_SIZE), 1)
        # Tile pattern
        for i in range(0, TILE_SIZE, 12):
            pygame.draw.line(pool_floor, (170, 200, 220), (i, 0), (i, TILE_SIZE), 1)
            pygame.draw.line(pool_floor, (170, 200, 220), (0, i), (TILE_SIZE, i), 1)
        self.tile_sprites[TILE_POOL_FLOOR] = pool_floor

        # Pool Door - glass door with blue tint
        pool_door = pygame.Surface((TILE_SIZE, TILE_SIZE))
        pool_door.fill(LIGHT_GRAY)
        pygame.draw.rect(pool_door, GRAY, (0, 0, TILE_SIZE, TILE_SIZE), 1)
        # Door frame
        pygame.draw.rect(pool_door, (100, 100, 110), (6, 0, TILE_SIZE - 12, TILE_SIZE))
        # Glass door
        pygame.draw.rect(pool_door, (150, 200, 230), (8, 2, TILE_SIZE - 16, TILE_SIZE - 4))
        # Handle
        pygame.draw.rect(pool_door, GRAY, (TILE_SIZE - 14, TILE_SIZE // 2 - 4, 4, 8))
        self.tile_sprites[TILE_POOL_DOOR] = pool_door

        # Outdoor Pull-up bar - metal frame on grass
        outdoor_pullup = pygame.Surface((TILE_SIZE, TILE_SIZE))
        outdoor_pullup.fill((60, 140, 60))  # Grass
        pygame.draw.rect(outdoor_pullup, (50, 120, 50), (0, 0, TILE_SIZE, TILE_SIZE), 1)
        # Metal posts
        pygame.draw.rect(outdoor_pullup, (80, 80, 90), (6, 10, 5, 34))
        pygame.draw.rect(outdoor_pullup, (80, 80, 90), (TILE_SIZE - 11, 10, 5, 34))
        # Top bar
        pygame.draw.rect(outdoor_pullup, (100, 100, 110), (6, 10, TILE_SIZE - 12, 4))
        self.tile_sprites[TILE_OUTDOOR_PULLUP] = outdoor_pullup

        # Parallel Bars - two horizontal bars
        outdoor_bars = pygame.Surface((TILE_SIZE, TILE_SIZE))
        outdoor_bars.fill((60, 140, 60))  # Grass
        pygame.draw.rect(outdoor_bars, (50, 120, 50), (0, 0, TILE_SIZE, TILE_SIZE), 1)
        # Support posts
        pygame.draw.rect(outdoor_bars, (80, 80, 90), (4, 18, 4, 26))
        pygame.draw.rect(outdoor_bars, (80, 80, 90), (TILE_SIZE - 8, 18, 4, 26))
        pygame.draw.rect(outdoor_bars, (80, 80, 90), (4, 28, 4, 16))
        pygame.draw.rect(outdoor_bars, (80, 80, 90), (TILE_SIZE - 8, 28, 4, 16))
        # Parallel bars
        pygame.draw.rect(outdoor_bars, (100, 100, 110), (4, 16, TILE_SIZE - 8, 4))
        pygame.draw.rect(outdoor_bars, (100, 100, 110), (4, 26, TILE_SIZE - 8, 4))
        self.tile_sprites[TILE_OUTDOOR_BARS] = outdoor_bars

        # Outdoor Bench - simple wooden bench
        outdoor_bench = pygame.Surface((TILE_SIZE, TILE_SIZE))
        outdoor_bench.fill((60, 140, 60))  # Grass
        pygame.draw.rect(outdoor_bench, (50, 120, 50), (0, 0, TILE_SIZE, TILE_SIZE), 1)
        # Bench seat
        pygame.draw.rect(outdoor_bench, BROWN, (4, 20, TILE_SIZE - 8, 8))
        pygame.draw.rect(outdoor_bench, DARK_BROWN, (4, 20, TILE_SIZE - 8, 2))
        # Legs
        pygame.draw.rect(outdoor_bench, DARK_BROWN, (8, 28, 4, 14))
        pygame.draw.rect(outdoor_bench, DARK_BROWN, (TILE_SIZE - 12, 28, 4, 14))
        self.tile_sprites[TILE_OUTDOOR_BENCH] = outdoor_bench

    def _generate_player_sprites(self):
        """Generate player sprites for all muscle levels and directions"""
        directions = ['down', 'up', 'left', 'right']

        for level in range(1, 8):
            self.player_sprites[level] = {}
            for direction in directions:
                self.player_sprites[level][direction] = self._create_player_sprite(level, direction)

    def _create_player_sprite(self, muscle_level, direction):
        """Create a single player sprite"""
        size = PLAYER_SIZE
        sprite = pygame.Surface((size, size), pygame.SRCALPHA)

        # Body proportions based on muscle level
        # Level 1 = skinny, Level 7 = very muscular
        body_width = 12 + muscle_level * 2
        shoulder_width = 14 + muscle_level * 3
        arm_thickness = 3 + muscle_level

        center_x = size // 2
        center_y = size // 2

        # Head
        head_size = 10
        head_y = 6
        pygame.draw.circle(sprite, SKIN_COLOR, (center_x, head_y), head_size // 2)

        # Hair (short, dark)
        pygame.draw.arc(sprite, DARK_GRAY, (center_x - 5, 2, 10, 8), 0, 3.14, 3)

        # Body/torso (tank top)
        body_top = head_y + head_size // 2
        body_height = 16

        # Tank top
        tank_color = RED if muscle_level < 4 else DARK_BLUE
        pygame.draw.rect(sprite, tank_color,
                        (center_x - body_width // 2, body_top, body_width, body_height))

        # Shoulders (skin showing for tank top look)
        if direction in ['down', 'up']:
            # Arms to the side
            arm_y = body_top + 2
            # Left arm
            pygame.draw.rect(sprite, SKIN_COLOR,
                           (center_x - shoulder_width // 2, arm_y, arm_thickness, 12))
            # Right arm
            pygame.draw.rect(sprite, SKIN_COLOR,
                           (center_x + shoulder_width // 2 - arm_thickness, arm_y, arm_thickness, 12))

            # Muscle definition for higher levels
            if muscle_level >= 4:
                # Bicep bulge
                pygame.draw.circle(sprite, DARK_SKIN,
                                 (center_x - shoulder_width // 2 + arm_thickness // 2, arm_y + 4),
                                 arm_thickness // 2)
                pygame.draw.circle(sprite, DARK_SKIN,
                                 (center_x + shoulder_width // 2 - arm_thickness // 2, arm_y + 4),
                                 arm_thickness // 2)

        # Legs (shorts)
        shorts_color = BLACK
        leg_top = body_top + body_height
        leg_width = body_width // 2 - 1
        leg_height = 10

        # Left leg
        pygame.draw.rect(sprite, shorts_color,
                        (center_x - body_width // 2 + 1, leg_top, leg_width, leg_height))
        # Right leg
        pygame.draw.rect(sprite, shorts_color,
                        (center_x + 1, leg_top, leg_width, leg_height))

        # Skin below shorts (calves)
        pygame.draw.rect(sprite, SKIN_COLOR,
                        (center_x - body_width // 2 + 2, leg_top + leg_height - 2, leg_width - 2, 4))
        pygame.draw.rect(sprite, SKIN_COLOR,
                        (center_x + 2, leg_top + leg_height - 2, leg_width - 2, 4))

        # Face features based on direction
        if direction == 'down':
            # Eyes
            pygame.draw.circle(sprite, BLACK, (center_x - 2, head_y), 1)
            pygame.draw.circle(sprite, BLACK, (center_x + 2, head_y), 1)
            # Determined expression (straight mouth)
            pygame.draw.line(sprite, DARK_GRAY, (center_x - 2, head_y + 3), (center_x + 2, head_y + 3), 1)
        elif direction == 'up':
            # Back of head
            pygame.draw.arc(sprite, DARK_GRAY, (center_x - 4, 3, 8, 6), 0, 3.14, 2)
        elif direction == 'left':
            # Side profile
            pygame.draw.circle(sprite, BLACK, (center_x - 2, head_y), 1)  # Eye
            pygame.draw.line(sprite, DARK_GRAY, (center_x - 3, head_y + 2), (center_x - 1, head_y + 3), 1)
        elif direction == 'right':
            pygame.draw.circle(sprite, BLACK, (center_x + 2, head_y), 1)  # Eye
            pygame.draw.line(sprite, DARK_GRAY, (center_x + 1, head_y + 2), (center_x + 3, head_y + 3), 1)

        return sprite

    def _generate_npc_sprites(self):
        """Generate NPC sprites with different color variants"""
        directions = ['down', 'up', 'left', 'right']
        # Different shirt colors for NPCs
        shirt_colors = [
            (34, 139, 34),   # Green
            (70, 130, 180),  # Steel blue
            (148, 0, 211),   # Purple
        ]

        for level in range(1, 8):
            self.npc_sprites[level] = {}
            for direction in directions:
                self.npc_sprites[level][direction] = {}
                for variant, shirt_color in enumerate(shirt_colors):
                    self.npc_sprites[level][direction][variant] = self._create_npc_sprite(
                        level, direction, shirt_color)

    def _create_npc_sprite(self, muscle_level, direction, shirt_color):
        """Create a single NPC sprite with given shirt color"""
        size = PLAYER_SIZE
        sprite = pygame.Surface((size, size), pygame.SRCALPHA)

        # Body proportions based on muscle level
        body_width = 12 + muscle_level * 2
        shoulder_width = 14 + muscle_level * 3
        arm_thickness = 3 + muscle_level

        center_x = size // 2
        center_y = size // 2

        # Head
        head_size = 10
        head_y = 6
        pygame.draw.circle(sprite, SKIN_COLOR, (center_x, head_y), head_size // 2)

        # Hair (varied styles)
        pygame.draw.arc(sprite, DARK_GRAY, (center_x - 5, 2, 10, 8), 0, 3.14, 3)

        # Body/torso with shirt color
        body_top = head_y + head_size // 2
        body_height = 16

        pygame.draw.rect(sprite, shirt_color,
                        (center_x - body_width // 2, body_top, body_width, body_height))

        # Arms
        if direction in ['down', 'up']:
            arm_y = body_top + 2
            pygame.draw.rect(sprite, SKIN_COLOR,
                           (center_x - shoulder_width // 2, arm_y, arm_thickness, 12))
            pygame.draw.rect(sprite, SKIN_COLOR,
                           (center_x + shoulder_width // 2 - arm_thickness, arm_y, arm_thickness, 12))

            if muscle_level >= 4:
                pygame.draw.circle(sprite, DARK_SKIN,
                                 (center_x - shoulder_width // 2 + arm_thickness // 2, arm_y + 4),
                                 arm_thickness // 2)
                pygame.draw.circle(sprite, DARK_SKIN,
                                 (center_x + shoulder_width // 2 - arm_thickness // 2, arm_y + 4),
                                 arm_thickness // 2)

        # Legs
        shorts_color = DARK_GRAY
        leg_top = body_top + body_height
        leg_width = body_width // 2 - 1
        leg_height = 10

        pygame.draw.rect(sprite, shorts_color,
                        (center_x - body_width // 2 + 1, leg_top, leg_width, leg_height))
        pygame.draw.rect(sprite, shorts_color,
                        (center_x + 1, leg_top, leg_width, leg_height))

        # Calves
        pygame.draw.rect(sprite, SKIN_COLOR,
                        (center_x - body_width // 2 + 2, leg_top + leg_height - 2, leg_width - 2, 4))
        pygame.draw.rect(sprite, SKIN_COLOR,
                        (center_x + 2, leg_top + leg_height - 2, leg_width - 2, 4))

        # Face based on direction
        if direction == 'down':
            pygame.draw.circle(sprite, BLACK, (center_x - 2, head_y), 1)
            pygame.draw.circle(sprite, BLACK, (center_x + 2, head_y), 1)
            pygame.draw.line(sprite, DARK_GRAY, (center_x - 2, head_y + 3), (center_x + 2, head_y + 3), 1)
        elif direction == 'up':
            pygame.draw.arc(sprite, DARK_GRAY, (center_x - 4, 3, 8, 6), 0, 3.14, 2)
        elif direction == 'left':
            pygame.draw.circle(sprite, BLACK, (center_x - 2, head_y), 1)
            pygame.draw.line(sprite, DARK_GRAY, (center_x - 3, head_y + 2), (center_x - 1, head_y + 3), 1)
        elif direction == 'right':
            pygame.draw.circle(sprite, BLACK, (center_x + 2, head_y), 1)
            pygame.draw.line(sprite, DARK_GRAY, (center_x + 1, head_y + 2), (center_x + 3, head_y + 3), 1)

        return sprite

    def _generate_ui_sprites(self):
        """Generate UI element sprites"""
        # Interaction indicator (E key)
        indicator = pygame.Surface((30, 20), pygame.SRCALPHA)
        pygame.draw.rect(indicator, (0, 0, 0, 180), (0, 0, 30, 20), border_radius=4)
        pygame.draw.rect(indicator, WHITE, (0, 0, 30, 20), 2, border_radius=4)
        self.ui_sprites['interact_key'] = indicator

        # Health/stat bar background
        bar_bg = pygame.Surface((UI_BAR_WIDTH, UI_BAR_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(bar_bg, (0, 0, 0, 150), (0, 0, UI_BAR_WIDTH, UI_BAR_HEIGHT), border_radius=3)
        self.ui_sprites['bar_bg'] = bar_bg

        # Stat icons
        for stat, color in [('strength', RED), ('endurance', GREEN), ('speed', BLUE)]:
            icon = pygame.Surface((16, 16), pygame.SRCALPHA)
            pygame.draw.circle(icon, color, (8, 8), 7)
            pygame.draw.circle(icon, WHITE, (8, 8), 7, 1)
            self.ui_sprites[f'{stat}_icon'] = icon

    def get_tile(self, tile_type):
        """Get a tile sprite by type"""
        return self.tile_sprites.get(tile_type, self.tile_sprites[TILE_FLOOR])

    def get_player(self, muscle_level, direction):
        """Get player sprite for given muscle level and direction"""
        level = max(1, min(7, muscle_level))
        return self.player_sprites[level].get(direction, self.player_sprites[level]['down'])

    def get_npc(self, muscle_level, direction, color_variant=0):
        """Get NPC sprite for given muscle level, direction, and color variant"""
        level = max(1, min(7, muscle_level))
        variant = color_variant % 3
        return self.npc_sprites[level][direction].get(variant, self.npc_sprites[level]['down'][0])

    def get_ui(self, name):
        """Get UI sprite by name"""
        return self.ui_sprites.get(name)
