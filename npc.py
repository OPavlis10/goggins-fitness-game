"""
NPC class - gym members that walk around, stand, and exercise
"""
import pygame
import random
from constants import *


class NPC:
    """A non-player character that wanders the gym"""

    # States
    IDLE = 'idle'
    WALKING = 'walking'
    EXERCISING = 'exercising'

    def __init__(self, x, y, sprite_generator, npc_id=0):
        self.x = x
        self.y = y
        self.sprites = sprite_generator
        self.npc_id = npc_id

        # Size and collision
        self.width = PLAYER_SIZE
        self.height = PLAYER_SIZE
        self.rect = pygame.Rect(x, y, self.width, self.height)

        # Movement
        self.speed = PLAYER_SPEED * 0.6  # Slower than player
        self.direction = random.choice(['up', 'down', 'left', 'right'])

        # State machine
        self.state = self.IDLE
        self.state_timer = random.uniform(1.0, 3.0)

        # Target position for walking
        self.target_x = x
        self.target_y = y

        # Current equipment being used
        self.current_equipment = None

        # Visual variety - different "muscle levels" for NPCs
        self.muscle_level = random.randint(2, 6)

        # Color tint for variety (shirt color index)
        self.color_variant = npc_id % 3

    def update(self, dt, game_map, equipment_tiles):
        """Update NPC state and position"""
        self.state_timer -= dt

        if self.state == self.IDLE:
            self._update_idle(dt, game_map, equipment_tiles)
        elif self.state == self.WALKING:
            self._update_walking(dt, game_map)
        elif self.state == self.EXERCISING:
            self._update_exercising(dt, game_map, equipment_tiles)

        # Update rect
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def _update_idle(self, dt, game_map, equipment_tiles):
        """Standing around, then decide what to do next"""
        if self.state_timer <= 0:
            # Decide next action
            action = random.random()

            if action < 0.6 and equipment_tiles:
                # Go to exercise equipment
                self._pick_equipment_target(equipment_tiles)
                self.state = self.WALKING
            elif action < 0.9:
                # Walk to random spot
                self._pick_random_target(game_map)
                self.state = self.WALKING
            else:
                # Stay idle longer
                self.state_timer = random.uniform(2.0, 5.0)

    def _update_walking(self, dt, game_map):
        """Walking towards target"""
        # Calculate direction to target
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = (dx**2 + dy**2) ** 0.5

        if distance < 5:
            # Reached target
            if self.current_equipment:
                self.state = self.EXERCISING
                self.state_timer = random.uniform(5.0, 15.0)
            else:
                self.state = self.IDLE
                self.state_timer = random.uniform(1.0, 4.0)
            return

        # Normalize and move
        if distance > 0:
            move_x = (dx / distance) * self.speed
            move_y = (dy / distance) * self.speed

            # Update direction for sprite
            if abs(dx) > abs(dy):
                self.direction = 'right' if dx > 0 else 'left'
            else:
                self.direction = 'down' if dy > 0 else 'up'

            # Try to move
            new_x = self.x + move_x
            new_y = self.y + move_y

            if game_map.is_position_valid(new_x, self.y, self.width, self.height):
                self.x = new_x
            if game_map.is_position_valid(self.x, new_y, self.width, self.height):
                self.y = new_y

        # Timeout - pick new target if stuck
        self.state_timer -= dt
        if self.state_timer <= 0:
            self.state = self.IDLE
            self.state_timer = random.uniform(0.5, 1.5)
            self.current_equipment = None

    def _update_exercising(self, dt, game_map, equipment_tiles):
        """Exercising at equipment"""
        if self.state_timer <= 0:
            # Done exercising
            self.current_equipment = None
            self.state = self.IDLE
            self.state_timer = random.uniform(2.0, 4.0)

    def _pick_equipment_target(self, equipment_tiles):
        """Pick a random equipment to use"""
        if not equipment_tiles:
            return

        tile = random.choice(equipment_tiles)
        # Stand next to equipment
        self.target_x = tile.rect.centerx
        self.target_y = tile.rect.centery + TILE_SIZE  # Stand below it
        self.current_equipment = tile
        self.state_timer = 10.0  # Timeout for reaching target

    def _pick_random_target(self, game_map):
        """Pick a random walkable spot in NPC's area"""
        for _ in range(20):  # Try 20 times
            grid_x = random.randint(2, game_map.width - 3)
            # Determine which area NPC is in based on current position
            current_grid_y = int(self.y // TILE_SIZE)
            if current_grid_y < 10:
                # Pool area (rows 1-8)
                grid_y = random.randint(1, 8)
            else:
                # Gym area (rows 10-26)
                grid_y = random.randint(10, 26)

            tile = game_map.get_tile(grid_x, grid_y)
            if tile and tile.walkable:
                self.target_x = tile.rect.centerx
                self.target_y = tile.rect.centery
                self.current_equipment = None
                self.state_timer = 8.0  # Timeout
                return

    def draw(self, surface, camera):
        """Draw NPC"""
        offset = camera.get_offset()
        draw_x = int(self.x - offset[0])
        draw_y = int(self.y - offset[1])

        # Get sprite
        sprite = self.sprites.get_npc(self.muscle_level, self.direction, self.color_variant)
        surface.blit(sprite, (draw_x, draw_y))

        # Draw exercise indicator if exercising
        if self.state == self.EXERCISING:
            # Small animation dots above head
            time_val = pygame.time.get_ticks() / 200
            for i in range(3):
                dot_y = draw_y - 8 - int(abs((time_val + i) % 3 - 1) * 4)
                pygame.draw.circle(surface, YELLOW, (draw_x + 15 + i * 6, dot_y), 2)


class NPCManager:
    """Manages all NPCs in the game"""

    def __init__(self, sprite_generator, game_map, count=5):
        self.sprites = sprite_generator
        self.npcs = []

        # Find equipment tiles for NPCs to use
        self.equipment_tiles = []
        for row in game_map.tiles:
            for tile in row:
                if tile.interactive and tile.stat is not None:
                    self.equipment_tiles.append(tile)

        # Spawn NPCs at random walkable positions
        self._spawn_npcs(game_map, count)

    def _spawn_npcs(self, game_map, count):
        """Spawn NPCs at random positions in gym and pool areas"""
        # Spawn some in gym, some in pool
        gym_count = count * 2 // 3  # 2/3 in gym
        pool_count = count - gym_count  # 1/3 in pool

        spawned = 0
        attempts = 0

        # Spawn gym NPCs (rows 10-26)
        while spawned < gym_count and attempts < 100:
            grid_x = random.randint(3, game_map.width - 4)
            grid_y = random.randint(10, 26)

            tile = game_map.get_tile(grid_x, grid_y)
            if tile and tile.walkable:
                x = tile.rect.centerx - PLAYER_SIZE // 2
                y = tile.rect.centery - PLAYER_SIZE // 2

                npc = NPC(x, y, self.sprites, npc_id=spawned)
                self.npcs.append(npc)
                spawned += 1

            attempts += 1

        # Spawn pool NPCs (rows 1-8)
        attempts = 0
        pool_spawned = 0
        while pool_spawned < pool_count and attempts < 50:
            grid_x = random.randint(2, game_map.width - 3)
            grid_y = random.randint(1, 8)

            tile = game_map.get_tile(grid_x, grid_y)
            if tile and tile.walkable:
                x = tile.rect.centerx - PLAYER_SIZE // 2
                y = tile.rect.centery - PLAYER_SIZE // 2

                npc = NPC(x, y, self.sprites, npc_id=spawned + pool_spawned)
                self.npcs.append(npc)
                pool_spawned += 1

            attempts += 1

    def update(self, dt, game_map):
        """Update all NPCs"""
        for npc in self.npcs:
            npc.update(dt, game_map, self.equipment_tiles)

    def draw(self, surface, camera):
        """Draw all NPCs"""
        for npc in self.npcs:
            npc.draw(surface, camera)
