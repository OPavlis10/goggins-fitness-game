"""
Tile-based map system for the gym
"""
import pygame
from constants import *


class Tile:
    """Represents a single tile on the map"""

    def __init__(self, tile_type, grid_x, grid_y):
        self.type = tile_type
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.rect = pygame.Rect(grid_x * TILE_SIZE, grid_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

        # Get properties from constants
        props = TILE_PROPERTIES.get(tile_type, TILE_PROPERTIES[TILE_FLOOR])
        self.walkable = props.get("walkable", True)
        self.interactive = props.get("interactive", False)
        self.name = props.get("name", "Unknown")
        self.stat = props.get("stat", None)
        self.xp_reward = props.get("xp", 0)

    def get_world_center(self):
        """Get center position in world coordinates"""
        return (self.rect.centerx, self.rect.centery)


class GameMap:
    """Manages the game map - a gym with various equipment"""

    def __init__(self, sprite_generator):
        self.sprites = sprite_generator

        # Define pool + gym + outdoor layout (25x46 tiles)
        # Legend:
        # 0=floor, 1=wall, 2=bench, 3=squat, 4=treadmill, 5=dumbbell
        # 6=shop, 7=trainer, 8=entrance, 9=mirror, 10=locker
        # 11=pullup bar, 12=lat pulldown, 13=cable machine
        # 14=outdoor door, 15=grass, 16=track, 17=fence, 18=tree
        # 19=pool water, 20=pool edge, 21=pool floor, 22=outdoor pullup
        # 23=outdoor bars, 24=outdoor bench, 25=pool door
        self.layout = [
            # Pool area (rows 0-9)
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21, 1],
            [1, 21,21,21,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,21,21,21, 1],
            [1, 21,21,21,20,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,20,21,21,21, 1],
            [1, 21,21,21,20,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,20,21,21,21, 1],
            [1, 21,21,21,20,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,20,21,21,21, 1],
            [1, 21,21,21,20,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,20,21,21,21, 1],
            [1, 21,21,21,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,21,21,21, 1],
            [1, 21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            # Gym area (rows 10-27)
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 9, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10,10,10, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10,10,10, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 0, 0, 0, 3, 0, 3, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 0, 0, 0, 3, 0, 3, 0, 0, 11, 0, 11, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 12, 0, 12, 0, 0, 0, 0, 0, 0, 0, 13, 0, 13, 0, 0, 0, 0, 0, 1],
            [1, 0, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 4, 0, 4, 0, 1],
            [1, 0, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 4, 0, 4, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 14, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            # Outdoor area with workout playground (rows 28-45)
            [17,17,17,17,17,17,17,17,17,17,17,17,15,17,17,17,17,17,17,17,17,17,17,17,17],
            [17,18,15,15,15,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,15,15,15,18,17],
            [17,15,15,15,16,16,15,15,15,15,15,15,15,15,15,15,15,15,15,16,16,15,15,15,17],
            [17,15,15,16,16,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,16,16,15,15,17],
            [17,15,16,16,15,15,15,15,15,22,15,15,15,15,15,22,15,15,15,15,15,16,16,15,17],
            [17,15,16,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,16,15,17],
            [17,15,16,15,15,15,15,15,15,15,15,23,15,23,15,15,15,15,15,15,15,15,16,15,17],
            [17,15,16,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,16,15,17],
            [17,15,16,15,15,15,15,15,15,15,15,24,15,24,15,15,15,15,15,15,15,15,16,15,17],
            [17,15,16,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,16,15,17],
            [17,15,16,16,15,15,15,15,15,22,15,15,15,15,15,22,15,15,15,15,15,16,16,15,17],
            [17,15,15,16,16,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,16,16,15,15,17],
            [17,15,15,15,16,16,15,15,15,15,15,15,15,15,15,15,15,15,15,16,16,15,15,15,17],
            [17,18,15,15,15,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,15,15,15,18,17],
            [17,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,17],
            [17,15,15,18,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,18,15,15,17],
            [17,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,17],
            [17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17],
        ]

        self.height = len(self.layout)
        self.width = len(self.layout[0])
        self.pixel_width = self.width * TILE_SIZE
        self.pixel_height = self.height * TILE_SIZE

        # Create tile objects
        self.tiles = []
        for y, row in enumerate(self.layout):
            tile_row = []
            for x, tile_type in enumerate(row):
                tile = Tile(tile_type, x, y)
                tile_row.append(tile)
            self.tiles.append(tile_row)

        # Find spawn point (entrance tile or first floor tile)
        self.spawn_point = self._find_spawn_point()

    def _find_spawn_point(self):
        """Find a good spawn point for the player - in front of Goggins"""
        # Look for trainer (Goggins) tile and spawn in front of him
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                if tile.type == TILE_TRAINER:
                    # Spawn two tiles below the trainer (to be clearly in front)
                    spawn_x = tile.rect.centerx
                    spawn_y = tile.rect.centery + (TILE_SIZE * 2)
                    return (spawn_x, spawn_y)

        # Fallback: spawn in center of gym area (grid 12, 21)
        return (12 * TILE_SIZE + TILE_SIZE // 2, 21 * TILE_SIZE + TILE_SIZE // 2)

    def get_tile(self, grid_x, grid_y):
        """Get tile at grid coordinates"""
        if 0 <= grid_x < self.width and 0 <= grid_y < self.height:
            return self.tiles[grid_y][grid_x]
        return None

    def get_tile_at_pixel(self, pixel_x, pixel_y):
        """Get tile at world pixel coordinates"""
        grid_x = int(pixel_x // TILE_SIZE)
        grid_y = int(pixel_y // TILE_SIZE)
        return self.get_tile(grid_x, grid_y)

    def is_walkable(self, pixel_x, pixel_y):
        """Check if a pixel position is walkable"""
        tile = self.get_tile_at_pixel(pixel_x, pixel_y)
        return tile.walkable if tile else False

    def is_position_valid(self, x, y, width, height):
        """Check if a rectangular area is entirely walkable"""
        # Check all four corners
        corners = [
            (x, y),
            (x + width - 1, y),
            (x, y + height - 1),
            (x + width - 1, y + height - 1)
        ]
        return all(self.is_walkable(cx, cy) for cx, cy in corners)

    def get_nearby_interactive(self, pixel_x, pixel_y, radius=INTERACTION_DISTANCE):
        """Get interactive tiles within radius of a position"""
        interactive = []
        center_grid_x = int(pixel_x // TILE_SIZE)
        center_grid_y = int(pixel_y // TILE_SIZE)

        # Check tiles in a 3x3 area around player
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                tile = self.get_tile(center_grid_x + dx, center_grid_y + dy)
                if tile and tile.interactive:
                    # Calculate distance from position to tile center
                    dist = ((pixel_x - tile.rect.centerx) ** 2 +
                            (pixel_y - tile.rect.centery) ** 2) ** 0.5
                    if dist <= radius:
                        interactive.append((tile, dist))

        # Sort by distance
        interactive.sort(key=lambda x: x[1])
        return [tile for tile, dist in interactive]

    def draw(self, surface, camera):
        """Draw visible tiles"""
        offset = camera.get_offset()

        # Calculate visible tile range
        start_x = max(0, offset[0] // TILE_SIZE)
        start_y = max(0, offset[1] // TILE_SIZE)
        end_x = min(self.width, (offset[0] + WINDOW_WIDTH) // TILE_SIZE + 2)
        end_y = min(self.height, (offset[1] + WINDOW_HEIGHT) // TILE_SIZE + 2)

        # Draw only visible tiles
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                tile = self.tiles[y][x]
                sprite = self.sprites.get_tile(tile.type)
                draw_x = tile.rect.x - offset[0]
                draw_y = tile.rect.y - offset[1]
                surface.blit(sprite, (draw_x, draw_y))
