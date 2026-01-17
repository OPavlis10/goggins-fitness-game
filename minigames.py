"""
Mini-games for equipment interactions
"""
import pygame
import random
from constants import *


class MiniGame:
    """Base class for mini-games"""

    def __init__(self, equipment_name):
        self.equipment_name = equipment_name
        self.is_active = False
        self.is_complete = False
        self.success = False
        self.score = 0
        self.max_score = 100

        # Fonts
        self.font = None
        self.title_font = None
        self.small_font = None

    def init_fonts(self):
        """Initialize fonts"""
        self.font = pygame.font.Font(None, UI_FONT_SIZE)
        self.title_font = pygame.font.Font(None, UI_TITLE_FONT_SIZE)
        self.small_font = pygame.font.Font(None, 16)

    def start(self):
        """Start the mini-game"""
        self.is_active = True
        self.is_complete = False
        self.success = False
        self.score = 0

    def update(self, dt, keys):
        """Update mini-game state"""
        pass

    def handle_event(self, event):
        """Handle input events"""
        pass

    def draw(self, surface):
        """Draw mini-game"""
        pass

    def get_xp_reward(self):
        """Calculate XP based on performance"""
        return int(self.score * 0.5)


class RhythmPress(MiniGame):
    """Press keys in rhythm - for bench press and squat"""

    def __init__(self, equipment_name, reps=5):
        super().__init__(equipment_name)
        self.target_reps = reps
        self.current_reps = 0

        # Timing
        self.bar_position = 0  # 0-100
        self.bar_speed = 80  # units per second
        self.bar_direction = 1
        self.target_zone = (40, 60)  # Perfect zone

        # Visual
        self.bar_width = 400
        self.bar_height = 40

        # Feedback
        self.feedback_text = ""
        self.feedback_timer = 0

    def start(self):
        super().start()
        self.current_reps = 0
        self.bar_position = 0
        self.bar_direction = 1
        self.feedback_text = "Press SPACE in the green zone!"
        self.feedback_timer = 2.0

    def update(self, dt, keys):
        if not self.is_active or self.is_complete:
            return

        # Move bar back and forth
        self.bar_position += self.bar_speed * self.bar_direction * dt

        if self.bar_position >= 100:
            self.bar_position = 100
            self.bar_direction = -1
        elif self.bar_position <= 0:
            self.bar_position = 0
            self.bar_direction = 1

        # Update feedback timer
        if self.feedback_timer > 0:
            self.feedback_timer -= dt

    def handle_event(self, event):
        if not self.is_active or self.is_complete:
            return

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self._check_press()

    def _check_press(self):
        """Check if press was in the zone"""
        if self.target_zone[0] <= self.bar_position <= self.target_zone[1]:
            # Perfect!
            self.score += 20
            self.feedback_text = "PERFECT!"
            self.feedback_timer = 0.5
        elif self.target_zone[0] - 15 <= self.bar_position <= self.target_zone[1] + 15:
            # Good
            self.score += 10
            self.feedback_text = "Good!"
            self.feedback_timer = 0.5
        else:
            # Miss
            self.feedback_text = "Miss!"
            self.feedback_timer = 0.5

        self.current_reps += 1

        if self.current_reps >= self.target_reps:
            self.is_complete = True
            self.success = self.score >= self.target_reps * 10
            self.is_active = False

    def draw(self, surface):
        if not self.is_active and not self.is_complete:
            return

        # Darken background
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))

        # Game area
        game_x = (WINDOW_WIDTH - self.bar_width) // 2
        game_y = WINDOW_HEIGHT // 2 - 50

        # Title
        title = self.title_font.render(f"{self.equipment_name} - Rep {self.current_reps + 1}/{self.target_reps}", True, ORANGE)
        title_x = (WINDOW_WIDTH - title.get_width()) // 2
        surface.blit(title, (title_x, game_y - 60))

        # Bar background
        pygame.draw.rect(surface, DARK_GRAY,
                        (game_x, game_y, self.bar_width, self.bar_height),
                        border_radius=5)

        # Target zone
        zone_x = game_x + int(self.bar_width * self.target_zone[0] / 100)
        zone_width = int(self.bar_width * (self.target_zone[1] - self.target_zone[0]) / 100)
        pygame.draw.rect(surface, GREEN,
                        (zone_x, game_y, zone_width, self.bar_height),
                        border_radius=5)

        # Good zone (lighter)
        good_x = game_x + int(self.bar_width * (self.target_zone[0] - 15) / 100)
        good_width = int(self.bar_width * 15 / 100)
        pygame.draw.rect(surface, (100, 150, 100),
                        (good_x, game_y, good_width, self.bar_height),
                        border_radius=5)
        pygame.draw.rect(surface, (100, 150, 100),
                        (zone_x + zone_width, game_y, good_width, self.bar_height),
                        border_radius=5)

        # Moving indicator
        indicator_x = game_x + int(self.bar_width * self.bar_position / 100)
        pygame.draw.rect(surface, YELLOW,
                        (indicator_x - 5, game_y - 5, 10, self.bar_height + 10),
                        border_radius=3)

        # Score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        surface.blit(score_text, (game_x, game_y + 60))

        # Feedback
        if self.feedback_timer > 0:
            feedback_color = GREEN if "PERFECT" in self.feedback_text else (
                YELLOW if "Good" in self.feedback_text else RED)
            feedback = self.title_font.render(self.feedback_text, True, feedback_color)
            feedback_x = (WINDOW_WIDTH - feedback.get_width()) // 2
            surface.blit(feedback, (feedback_x, game_y + 100))

        # Instructions
        instr = self.small_font.render("Press SPACE when the bar is in the green zone!", True, GRAY)
        instr_x = (WINDOW_WIDTH - instr.get_width()) // 2
        surface.blit(instr, (instr_x, game_y + 140))


class HoldSteady(MiniGame):
    """Hold a key steady - for treadmill"""

    def __init__(self, equipment_name, duration=5):
        super().__init__(equipment_name)
        self.duration = duration
        self.time_held = 0
        self.is_holding = False

        # Visual
        self.bar_width = 400
        self.bar_height = 30

    def start(self):
        super().start()
        self.time_held = 0
        self.is_holding = False

    def update(self, dt, keys):
        if not self.is_active or self.is_complete:
            return

        self.is_holding = keys[pygame.K_SPACE]

        if self.is_holding:
            self.time_held += dt
            self.score = int((self.time_held / self.duration) * 100)

            if self.time_held >= self.duration:
                self.is_complete = True
                self.success = True
                self.is_active = False

    def draw(self, surface):
        if not self.is_active and not self.is_complete:
            return

        # Darken background
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))

        game_x = (WINDOW_WIDTH - self.bar_width) // 2
        game_y = WINDOW_HEIGHT // 2 - 30

        # Title
        title = self.title_font.render(f"{self.equipment_name} - Running!", True, ORANGE)
        title_x = (WINDOW_WIDTH - title.get_width()) // 2
        surface.blit(title, (title_x, game_y - 60))

        # Progress bar background
        pygame.draw.rect(surface, DARK_GRAY,
                        (game_x, game_y, self.bar_width, self.bar_height),
                        border_radius=5)

        # Progress fill
        progress = min(1.0, self.time_held / self.duration)
        fill_width = int(self.bar_width * progress)
        color = GREEN if self.is_holding else ORANGE
        if fill_width > 0:
            pygame.draw.rect(surface, color,
                           (game_x, game_y, fill_width, self.bar_height),
                           border_radius=5)

        # Border
        pygame.draw.rect(surface, WHITE,
                        (game_x, game_y, self.bar_width, self.bar_height),
                        2, border_radius=5)

        # Time display
        remaining = max(0, self.duration - self.time_held)
        time_text = self.font.render(f"Time: {remaining:.1f}s", True, WHITE)
        surface.blit(time_text, (game_x, game_y + 50))

        # Status
        status = "HOLD SPACE!" if self.is_holding else "Press and HOLD SPACE!"
        status_color = GREEN if self.is_holding else YELLOW
        status_text = self.title_font.render(status, True, status_color)
        status_x = (WINDOW_WIDTH - status_text.get_width()) // 2
        surface.blit(status_text, (status_x, game_y + 90))


class QuickTimeEvent(MiniGame):
    """Press shown keys quickly - for dumbbells"""

    def __init__(self, equipment_name, key_count=8):
        super().__init__(equipment_name)
        self.key_count = key_count
        self.keys_pressed = 0

        # Current key to press
        self.target_key = None
        self.key_names = {
            pygame.K_w: 'W', pygame.K_a: 'A',
            pygame.K_s: 'S', pygame.K_d: 'D',
            pygame.K_UP: 'UP', pygame.K_DOWN: 'DOWN',
            pygame.K_LEFT: 'LEFT', pygame.K_RIGHT: 'RIGHT'
        }
        self.available_keys = list(self.key_names.keys())

        # Timing
        self.time_limit = 1.5  # seconds per key
        self.time_remaining = 0

    def start(self):
        super().start()
        self.keys_pressed = 0
        self._next_key()

    def _next_key(self):
        """Generate next random key"""
        self.target_key = random.choice(self.available_keys)
        self.time_remaining = self.time_limit

    def update(self, dt, keys):
        if not self.is_active or self.is_complete:
            return

        self.time_remaining -= dt

        if self.time_remaining <= 0:
            # Missed this key
            self._next_key()

    def handle_event(self, event):
        if not self.is_active or self.is_complete:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == self.target_key:
                # Correct key!
                self.score += 15 if self.time_remaining > 1.0 else 10
                self.keys_pressed += 1

                if self.keys_pressed >= self.key_count:
                    self.is_complete = True
                    self.success = True
                    self.is_active = False
                else:
                    self._next_key()

    def draw(self, surface):
        if not self.is_active and not self.is_complete:
            return

        # Darken background
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))

        game_y = WINDOW_HEIGHT // 2 - 50

        # Title
        title = self.title_font.render(
            f"{self.equipment_name} - {self.keys_pressed}/{self.key_count}", True, ORANGE)
        title_x = (WINDOW_WIDTH - title.get_width()) // 2
        surface.blit(title, (title_x, game_y - 60))

        # Show target key
        key_name = self.key_names.get(self.target_key, '?')
        key_text = pygame.font.Font(None, 72).render(key_name, True, YELLOW)
        key_x = (WINDOW_WIDTH - key_text.get_width()) // 2
        surface.blit(key_text, (key_x, game_y))

        # Time bar
        bar_width = 300
        bar_x = (WINDOW_WIDTH - bar_width) // 2
        bar_y = game_y + 80

        pygame.draw.rect(surface, DARK_GRAY,
                        (bar_x, bar_y, bar_width, 20), border_radius=5)

        time_percent = self.time_remaining / self.time_limit
        fill_width = int(bar_width * time_percent)
        color = GREEN if time_percent > 0.5 else (YELLOW if time_percent > 0.25 else RED)
        if fill_width > 0:
            pygame.draw.rect(surface, color,
                           (bar_x, bar_y, fill_width, 20), border_radius=5)

        # Score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        score_x = (WINDOW_WIDTH - score_text.get_width()) // 2
        surface.blit(score_text, (score_x, bar_y + 40))


class MiniGameManager:
    """Manages all mini-games"""

    def __init__(self):
        self.current_game = None
        self.games = {}

        # Create game instances for each equipment type
        self.games['Bench Press'] = RhythmPress('Bench Press', reps=5)
        self.games['Squat Rack'] = RhythmPress('Squat Rack', reps=6)
        self.games['Treadmill'] = HoldSteady('Treadmill', duration=5)
        self.games['Dumbbells'] = QuickTimeEvent('Dumbbells', key_count=8)
        self.games['Pull-up Bar'] = RhythmPress('Pull-up Bar', reps=6)
        self.games['Lat Pulldown'] = RhythmPress('Lat Pulldown', reps=5)
        self.games['Cable Machine'] = QuickTimeEvent('Cable Machine', key_count=10)

    def init_fonts(self):
        """Initialize fonts for all games"""
        for game in self.games.values():
            game.init_fonts()

    def start_game(self, equipment_name):
        """Start mini-game for equipment"""
        if equipment_name in self.games:
            self.current_game = self.games[equipment_name]
            self.current_game.start()
            return True
        return False

    def is_active(self):
        """Check if a mini-game is currently active"""
        return self.current_game is not None and self.current_game.is_active

    def is_complete(self):
        """Check if current game is complete"""
        return self.current_game is not None and self.current_game.is_complete

    def get_result(self):
        """Get result of completed game"""
        if self.current_game and self.current_game.is_complete:
            return {
                'success': self.current_game.success,
                'score': self.current_game.score,
                'xp_reward': self.current_game.get_xp_reward(),
                'equipment': self.current_game.equipment_name
            }
        return None

    def update(self, dt, keys):
        """Update current game"""
        if self.current_game and self.current_game.is_active:
            self.current_game.update(dt, keys)

    def handle_event(self, event):
        """Handle input for current game"""
        if self.current_game and self.current_game.is_active:
            self.current_game.handle_event(event)

    def draw(self, surface):
        """Draw current game"""
        if self.current_game:
            self.current_game.draw(surface)

    def clear(self):
        """Clear current game"""
        self.current_game = None
