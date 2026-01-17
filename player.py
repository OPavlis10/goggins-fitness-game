"""
Player class with stats, movement, and sprite support
"""
import pygame
from constants import *


class Player:
    """Represents the player character"""

    def __init__(self, x, y, sprite_generator):
        self.x = x
        self.y = y
        self.sprites = sprite_generator

        # Size and collision
        self.width = PLAYER_SIZE
        self.height = PLAYER_SIZE
        self.rect = pygame.Rect(x, y, self.width, self.height)

        # Movement
        self.speed = PLAYER_SPEED
        self.vel_x = 0
        self.vel_y = 0
        self.direction = 'down'

        # Stats
        self.stats = INITIAL_STATS.copy()
        self.xp_to_next = XP_PER_LEVEL.get(2, 100)

        # Muscle level (1-7, determines sprite appearance)
        self.muscle_level = 1

        # Active buffs: {effect_name: (value, end_time)}
        self.buffs = {}

        # Interaction cooldown
        self.interact_cooldown = 0

        # Animation
        self.animation_timer = 0
        self.is_moving = False

        # Stamina system
        self.stamina = self._get_max_stamina()
        self.is_sprinting = False
        self.stamina_regen_timer = 0

        # Swimming
        self.is_swimming = False
        self.swim_xp_timer = 0

    def update(self, keys, game_map, dt):
        """Update player state"""
        # Update cooldowns
        if self.interact_cooldown > 0:
            self.interact_cooldown -= dt

        # Update buffs
        current_time = pygame.time.get_ticks() / 1000
        expired = [k for k, v in self.buffs.items() if v[1] < current_time]
        for k in expired:
            del self.buffs[k]

        # Handle movement input
        self.vel_x = 0
        self.vel_y = 0
        self.is_moving = False

        # Check if in water
        center = self.get_center()
        tile = game_map.get_tile_at_pixel(center[0], center[1])
        self.is_swimming = tile and TILE_PROPERTIES.get(tile.type, {}).get('is_water', False)

        # Handle sprinting (not while swimming)
        wants_to_sprint = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        self.is_sprinting = wants_to_sprint and self.stamina > 0 and not self.is_swimming

        # Get effective speed (with buffs and sprint)
        effective_speed = self.speed
        if 'speed_boost' in self.buffs:
            effective_speed *= self.buffs['speed_boost'][0]
        if self.is_sprinting:
            effective_speed *= SPRINT_SPEED_MULTIPLIER
        if self.is_swimming:
            effective_speed *= SWIM_SPEED_MULTIPLIER

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.vel_y = -effective_speed
            self.direction = 'up'
            self.is_moving = True
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.vel_y = effective_speed
            self.direction = 'down'
            self.is_moving = True
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vel_x = -effective_speed
            self.direction = 'left'
            self.is_moving = True
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vel_x = effective_speed
            self.direction = 'right'
            self.is_moving = True

        # Normalize diagonal movement
        if self.vel_x != 0 and self.vel_y != 0:
            self.vel_x *= 0.7071
            self.vel_y *= 0.7071

        # Apply movement with collision
        self._move(game_map)

        # Update stamina
        self._update_stamina(dt, game_map)

        # Update animation
        if self.is_moving:
            self.animation_timer += dt
        else:
            self.animation_timer = 0

    def _move(self, game_map):
        """Move player with collision detection"""
        # Try horizontal movement
        if self.vel_x != 0:
            new_x = self.x + self.vel_x
            if game_map.is_position_valid(new_x, self.y, self.width, self.height):
                self.x = new_x

        # Try vertical movement
        if self.vel_y != 0:
            new_y = self.y + self.vel_y
            if game_map.is_position_valid(self.x, new_y, self.width, self.height):
                self.y = new_y

        # Update rect
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def get_center(self):
        """Get center position"""
        return (self.x + self.width // 2, self.y + self.height // 2)

    def add_xp(self, amount):
        """Add XP with buff multipliers, returns True if leveled up"""
        # Apply XP multipliers
        if 'strength_xp_boost' in self.buffs:
            amount = int(amount * self.buffs['strength_xp_boost'][0])
        if 'all_xp_boost' in self.buffs:
            amount = int(amount * self.buffs['all_xp_boost'][0])

        self.stats['xp'] += amount
        leveled_up = False

        # Check for level up
        while self.stats['xp'] >= self.xp_to_next:
            self.stats['xp'] -= self.xp_to_next
            self.stats['level'] += 1
            self.xp_to_next = XP_PER_LEVEL.get(self.stats['level'] + 1, int(self.xp_to_next * 1.5))
            leveled_up = True

        if leveled_up:
            self._update_muscle_level()

        return leveled_up

    def add_stat(self, stat_name, amount):
        """Add to a specific stat"""
        if stat_name in self.stats:
            self.stats[stat_name] += amount

            # Speed stat affects movement
            if stat_name == 'speed':
                self.speed = PLAYER_SPEED + self.stats['speed'] * 0.2

            # Strength affects muscle level
            if stat_name == 'strength':
                self._update_muscle_level()

    def _update_muscle_level(self):
        """Update muscle level based on strength stat"""
        strength = self.stats.get('strength', 1)
        for level in sorted(MUSCLE_LEVELS.keys(), reverse=True):
            if strength >= MUSCLE_LEVELS[level]:
                self.muscle_level = level
                break

    def _get_max_stamina(self):
        """Calculate max stamina based on endurance and level"""
        endurance = self.stats.get('endurance', 1)
        level = self.stats.get('level', 1)
        return BASE_STAMINA + endurance * STAMINA_PER_ENDURANCE + level * 5

    def _update_stamina(self, dt, game_map=None):
        """Update stamina based on sprinting/swimming state"""
        max_stamina = self._get_max_stamina()

        if self.is_sprinting and self.is_moving:
            # Drain stamina while sprinting
            self.stamina -= STAMINA_DRAIN_RATE * dt
            self.stamina_regen_timer = STAMINA_REGEN_DELAY
            if self.stamina <= 0:
                self.stamina = 0
                self.is_sprinting = False
        elif self.is_swimming and self.is_moving:
            # Drain stamina while swimming (slower)
            self.stamina -= SWIM_STAMINA_DRAIN * dt
            self.stamina_regen_timer = STAMINA_REGEN_DELAY
            if self.stamina <= 0:
                self.stamina = 0
            # Gain endurance XP while swimming
            self.swim_xp_timer += dt
            if self.swim_xp_timer >= 2.0:  # Every 2 seconds
                self.swim_xp_timer = 0
                self.add_xp(2)
                self.add_stat('endurance', 0.1)
        else:
            # Regenerate stamina when not active
            if self.stamina_regen_timer > 0:
                self.stamina_regen_timer -= dt
            else:
                self.stamina = min(max_stamina, self.stamina + STAMINA_REGEN_RATE * dt)

    def add_currency(self, amount):
        """Add currency"""
        self.stats['currency'] += amount

    def spend_currency(self, amount):
        """Spend currency, returns True if successful"""
        if self.stats['currency'] >= amount:
            self.stats['currency'] -= amount
            return True
        return False

    def apply_buff(self, effect_name, value, duration):
        """Apply a temporary buff"""
        end_time = pygame.time.get_ticks() / 1000 + duration
        self.buffs[effect_name] = (value, end_time)

    def can_interact(self):
        """Check if player can interact"""
        return self.interact_cooldown <= 0

    def set_interact_cooldown(self, seconds=0.5):
        """Set interaction cooldown"""
        self.interact_cooldown = seconds

    def get_active_buffs(self):
        """Get list of active buffs with remaining time"""
        current_time = pygame.time.get_ticks() / 1000
        return [(name, value, end - current_time)
                for name, (value, end) in self.buffs.items()
                if end > current_time]

    def draw(self, surface, camera):
        """Draw player with sprite"""
        offset = camera.get_offset()
        draw_x = int(self.x - offset[0])
        draw_y = int(self.y - offset[1])

        # Get appropriate sprite
        sprite = self.sprites.get_player(self.muscle_level, self.direction)

        if self.is_swimming:
            # Swimming effect - only show top half and add water ripples
            swim_sprite = sprite.copy()
            # Add blue tint to lower half
            water_overlay = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE // 2), pygame.SRCALPHA)
            water_overlay.fill((40, 120, 200, 150))
            swim_sprite.blit(water_overlay, (0, PLAYER_SIZE // 2))

            surface.blit(swim_sprite, (draw_x, draw_y))

            # Draw ripple effect
            time_val = pygame.time.get_ticks() / 150
            for i in range(3):
                ripple_x = draw_x + 5 + i * 12 + int(2 * ((time_val + i) % 2 - 1))
                ripple_y = draw_y + PLAYER_SIZE // 2 + 4
                pygame.draw.ellipse(surface, (100, 180, 255, 150),
                                   (ripple_x, ripple_y, 8, 4), 1)
        else:
            surface.blit(sprite, (draw_x, draw_y))

    def to_dict(self):
        """Convert player state to dictionary for saving"""
        return {
            'x': self.x,
            'y': self.y,
            'stats': self.stats.copy(),
            'muscle_level': self.muscle_level,
            'direction': self.direction,
            'stamina': self.stamina
        }

    def from_dict(self, data):
        """Load player state from dictionary"""
        self.x = data.get('x', self.x)
        self.y = data.get('y', self.y)
        self.stats = data.get('stats', INITIAL_STATS.copy())
        self.muscle_level = data.get('muscle_level', 1)
        self.direction = data.get('direction', 'down')
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        self.xp_to_next = XP_PER_LEVEL.get(self.stats['level'] + 1, 100)
        self.speed = PLAYER_SPEED + self.stats.get('speed', 1) * 0.2
        self.stamina = data.get('stamina', self._get_max_stamina())
