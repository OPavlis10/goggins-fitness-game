"""
Camera system for following the player
"""
import pygame
from constants import *


class Camera:
    """Camera that follows the player and handles viewport"""

    def __init__(self, map_width, map_height):
        self.offset_x = 0
        self.offset_y = 0
        self.map_width = map_width
        self.map_height = map_height

        # Smoothing factor (0 = instant, 1 = no movement)
        self.smoothing = 0.1

    def update(self, target_x, target_y):
        """Update camera to follow target (usually player center)"""
        # Calculate desired offset (center target on screen)
        desired_x = target_x - WINDOW_WIDTH // 2
        desired_y = target_y - WINDOW_HEIGHT // 2

        # Apply smoothing for less jarring movement
        self.offset_x += (desired_x - self.offset_x) * (1 - self.smoothing)
        self.offset_y += (desired_y - self.offset_y) * (1 - self.smoothing)

        # Clamp to map boundaries
        self.offset_x = max(0, min(self.offset_x, self.map_width - WINDOW_WIDTH))
        self.offset_y = max(0, min(self.offset_y, self.map_height - WINDOW_HEIGHT))

        # Handle maps smaller than screen
        if self.map_width < WINDOW_WIDTH:
            self.offset_x = (self.map_width - WINDOW_WIDTH) // 2
        if self.map_height < WINDOW_HEIGHT:
            self.offset_y = (self.map_height - WINDOW_HEIGHT) // 2

    def get_offset(self):
        """Get current camera offset as tuple"""
        return (int(self.offset_x), int(self.offset_y))

    def apply(self, rect):
        """Apply camera offset to a rect, returning new rect for drawing"""
        return pygame.Rect(
            rect.x - self.offset_x,
            rect.y - self.offset_y,
            rect.width,
            rect.height
        )

    def apply_pos(self, x, y):
        """Apply camera offset to a position"""
        return (x - self.offset_x, y - self.offset_y)

    def reverse_apply(self, screen_x, screen_y):
        """Convert screen coordinates to world coordinates"""
        return (screen_x + self.offset_x, screen_y + self.offset_y)

    def is_visible(self, rect):
        """Check if a rect is visible on screen"""
        screen_rect = pygame.Rect(
            self.offset_x,
            self.offset_y,
            WINDOW_WIDTH,
            WINDOW_HEIGHT
        )
        return screen_rect.colliderect(rect)
