"""
UI overlay system for displaying stats, quests, and game information
"""
import pygame
from constants import *


class UI:
    """Manages all UI elements"""

    def __init__(self, sprite_generator):
        self.sprites = sprite_generator
        self.font = None
        self.small_font = None
        self.title_font = None

        # UI state
        self.show_interact_prompt = False
        self.interact_target = None

        # Notification system
        self.notifications = []  # [(text, color, timer)]

    def init_fonts(self):
        """Initialize fonts (call after pygame.init)"""
        self.font = pygame.font.Font(None, UI_FONT_SIZE)
        self.small_font = pygame.font.Font(None, 16)
        self.title_font = pygame.font.Font(None, UI_TITLE_FONT_SIZE)

    def add_notification(self, text, color=WHITE, duration=2.0):
        """Add a notification that fades out"""
        self.notifications.append([text, color, duration])

    def update(self, dt):
        """Update UI state"""
        # Update notification timers
        self.notifications = [[t, c, timer - dt] for t, c, timer in self.notifications if timer > 0]

    def set_interact_prompt(self, show, target_name=None):
        """Show or hide interaction prompt"""
        self.show_interact_prompt = show
        self.interact_target = target_name

    def draw(self, surface, player, current_quest=None):
        """Draw all UI elements"""
        self._draw_stats_panel(surface, player)
        self._draw_stamina_bar(surface, player)
        self._draw_currency(surface, player)
        self._draw_buffs(surface, player)
        self._draw_interact_prompt(surface)
        self._draw_notifications(surface)

        if current_quest:
            self._draw_quest_tracker(surface, current_quest)

    def _draw_stats_panel(self, surface, player):
        """Draw player stats panel with modern style"""
        panel_x = UI_PADDING
        panel_y = UI_PADDING
        panel_width = 200
        panel_height = 145

        # Background with gradient effect
        panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        # Dark gradient background
        for i in range(panel_height):
            alpha = 200 - i // 3
            pygame.draw.line(panel, (20, 25, 35, alpha), (0, i), (panel_width, i))
        pygame.draw.rect(panel, (60, 70, 90), (0, 0, panel_width, panel_height), 2, border_radius=10)
        # Accent line at top
        pygame.draw.line(panel, ORANGE, (10, 2), (panel_width - 10, 2), 2)
        surface.blit(panel, (panel_x, panel_y))

        # Level badge
        badge_x = panel_x + 10
        badge_y = panel_y + 8
        pygame.draw.rect(surface, (255, 180, 0), (badge_x, badge_y, 70, 24), border_radius=12)
        pygame.draw.rect(surface, (255, 220, 100), (badge_x + 2, badge_y + 2, 66, 20), border_radius=10)
        level_text = self.font.render(f"LVL {player.stats['level']}", True, (40, 30, 0))
        surface.blit(level_text, (badge_x + 12, badge_y + 4))

        # Muscle level indicator
        muscle_text = self.small_font.render(f"Muscle: {player.muscle_level}/7", True, (180, 180, 200))
        surface.blit(muscle_text, (panel_x + 90, panel_y + 12))

        # XP bar with glow effect
        xp_bar_y = panel_y + 38
        xp_percent = player.stats['xp'] / player.xp_to_next if player.xp_to_next > 0 else 0
        self._draw_fancy_bar(surface, panel_x + 10, xp_bar_y, 180, 14, xp_percent,
                            (140, 80, 200), (180, 120, 255), f"{player.stats['xp']}/{player.xp_to_next} XP")

        # Stats with icons
        stats_y = panel_y + 58
        stats_to_show = [
            ('💪', 'STR', player.stats['strength'], (255, 100, 100), (255, 150, 150)),
            ('🏃', 'END', player.stats['endurance'], (100, 255, 100), (150, 255, 150)),
            ('⚡', 'SPD', player.stats['speed'], (100, 150, 255), (150, 200, 255))
        ]

        for i, (icon, name, value, color, light_color) in enumerate(stats_to_show):
            y = stats_y + i * 28
            # Stat icon circle
            pygame.draw.circle(surface, color, (panel_x + 18, y + 10), 8)
            pygame.draw.circle(surface, light_color, (panel_x + 16, y + 8), 3)

            # Stat name and value
            name_text = self.font.render(name, True, (200, 200, 210))
            surface.blit(name_text, (panel_x + 32, y + 2))

            value_text = self.font.render(str(int(value)), True, WHITE)
            surface.blit(value_text, (panel_x + 70, y + 2))

            # Progress bar
            bar_percent = min(1.0, value / 50)
            pygame.draw.rect(surface, (40, 45, 55), (panel_x + 100, y + 5, 90, 10), border_radius=5)
            if bar_percent > 0:
                pygame.draw.rect(surface, color, (panel_x + 100, y + 5, int(90 * bar_percent), 10), border_radius=5)
            pygame.draw.rect(surface, (80, 90, 100), (panel_x + 100, y + 5, 90, 10), 1, border_radius=5)

    def _draw_fancy_bar(self, surface, x, y, width, height, percent, color, light_color, text=None):
        """Draw a fancy progress bar with gradient"""
        # Background
        pygame.draw.rect(surface, (30, 35, 45), (x, y, width, height), border_radius=7)

        # Fill with gradient
        fill_width = int(width * min(1.0, percent))
        if fill_width > 0:
            for i in range(height):
                blend = i / height
                r = int(color[0] * (1 - blend * 0.3) + light_color[0] * blend * 0.3)
                g = int(color[1] * (1 - blend * 0.3) + light_color[1] * blend * 0.3)
                b = int(color[2] * (1 - blend * 0.3) + light_color[2] * blend * 0.3)
                pygame.draw.line(surface, (r, g, b), (x + 2, y + i), (x + fill_width - 2, y + i))

        # Border
        pygame.draw.rect(surface, (80, 90, 110), (x, y, width, height), 1, border_radius=7)

        # Text
        if text and self.small_font:
            text_surface = self.small_font.render(text, True, WHITE)
            text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
            surface.blit(text_surface, text_rect)

    def _draw_stamina_bar(self, surface, player):
        """Draw stamina bar below stats panel with modern style"""
        bar_x = UI_PADDING
        bar_y = UI_PADDING + 155
        bar_width = 200
        bar_height = 18

        # Calculate stamina percentage
        max_stamina = player._get_max_stamina()
        stamina_percent = player.stamina / max_stamina if max_stamina > 0 else 0

        # Choose colors based on percentage
        if stamina_percent > 0.5:
            bar_color = (50, 220, 100)
            light_color = (100, 255, 150)
        elif stamina_percent > 0.25:
            bar_color = (255, 200, 50)
            light_color = (255, 230, 100)
        else:
            bar_color = (255, 120, 50)
            light_color = (255, 160, 100)

        # Background panel
        bg = pygame.Surface((bar_width + 10, bar_height + 28), pygame.SRCALPHA)
        for i in range(bar_height + 28):
            alpha = 180 - i // 2
            pygame.draw.line(bg, (20, 25, 35, alpha), (0, i), (bar_width + 10, i))
        pygame.draw.rect(bg, (60, 70, 90), (0, 0, bar_width + 10, bar_height + 28), 1, border_radius=8)
        surface.blit(bg, (bar_x - 5, bar_y - 6))

        # Label with icon
        pygame.draw.circle(surface, (100, 200, 255), (bar_x + 8, bar_y + 5), 5)
        label = self.small_font.render("STAMINA", True, (180, 190, 210))
        surface.blit(label, (bar_x + 18, bar_y - 1))

        # Stamina bar
        self._draw_fancy_bar(surface, bar_x, bar_y + 14, bar_width, bar_height - 2,
                            stamina_percent, bar_color, light_color)

        # Status indicator
        status_x = bar_x + bar_width - 70
        if player.is_swimming and player.is_moving:
            # Swimming indicator
            pygame.draw.rect(surface, (40, 120, 200), (status_x, bar_y - 2, 70, 14), border_radius=7)
            swim_text = self.small_font.render("SWIMMING", True, WHITE)
            surface.blit(swim_text, (status_x + 5, bar_y))
        elif player.is_sprinting and player.is_moving:
            # Sprint indicator
            pygame.draw.rect(surface, (255, 180, 0), (status_x, bar_y - 2, 70, 14), border_radius=7)
            sprint_text = self.small_font.render("SPRINTING", True, (40, 30, 0))
            surface.blit(sprint_text, (status_x + 3, bar_y))

    def _draw_progress_bar(self, surface, x, y, width, height, percent, color, text=None):
        """Draw a progress bar"""
        # Background
        pygame.draw.rect(surface, DARK_GRAY, (x, y, width, height), border_radius=4)
        # Fill
        fill_width = int(width * min(1.0, percent))
        if fill_width > 0:
            pygame.draw.rect(surface, color, (x, y, fill_width, height), border_radius=4)
        # Border
        pygame.draw.rect(surface, WHITE, (x, y, width, height), 1, border_radius=4)
        # Text
        if text and self.small_font:
            text_surface = self.small_font.render(text, True, WHITE)
            text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
            surface.blit(text_surface, text_rect)

    def _draw_currency(self, surface, player):
        """Draw currency display with modern style"""
        currency_x = WINDOW_WIDTH - 130
        currency_y = UI_PADDING

        # Background with gradient
        bg = pygame.Surface((120, 36), pygame.SRCALPHA)
        for i in range(36):
            alpha = 200 - i
            pygame.draw.line(bg, (25, 30, 40, alpha), (0, i), (120, i))
        pygame.draw.rect(bg, (80, 90, 100), (0, 0, 120, 36), 1, border_radius=18)
        surface.blit(bg, (currency_x, currency_y))

        # Coin icon with shine
        coin_x = currency_x + 18
        coin_y = currency_y + 18
        pygame.draw.circle(surface, (255, 200, 50), (coin_x, coin_y), 12)
        pygame.draw.circle(surface, (255, 230, 100), (coin_x - 3, coin_y - 3), 4)
        pygame.draw.circle(surface, (200, 150, 30), (coin_x, coin_y), 12, 2)
        # $ symbol
        dollar = self.small_font.render("$", True, (150, 100, 0))
        surface.blit(dollar, (coin_x - 4, coin_y - 6))

        # Amount
        amount_text = self.font.render(f"{player.stats['currency']}", True, (255, 220, 100))
        surface.blit(amount_text, (currency_x + 38, currency_y + 9))

    def _draw_buffs(self, surface, player):
        """Draw active buff indicators"""
        buffs = player.get_active_buffs()
        if not buffs:
            return

        buff_x = WINDOW_WIDTH - 200
        buff_y = UI_PADDING + 40

        for i, (name, value, remaining) in enumerate(buffs):
            y = buff_y + i * 25

            # Background
            bg = pygame.Surface((190, 22), pygame.SRCALPHA)
            pygame.draw.rect(bg, (0, 0, 0, 150), (0, 0, 190, 22), border_radius=4)
            surface.blit(bg, (buff_x, y))

            # Buff name and timer
            buff_display = name.replace('_', ' ').title()
            text = self.small_font.render(f"{buff_display}: {remaining:.0f}s", True, GREEN)
            surface.blit(text, (buff_x + 5, y + 4))

    def _draw_interact_prompt(self, surface):
        """Draw interaction prompt when near equipment"""
        if not self.show_interact_prompt or not self.interact_target:
            return

        # Position at bottom center
        y = WINDOW_HEIGHT - 70

        # Background
        bg_width = 280
        bg_height = 50
        x = (WINDOW_WIDTH - bg_width) // 2

        bg = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
        for i in range(bg_height):
            alpha = 220 - i
            pygame.draw.line(bg, (20, 25, 35, alpha), (0, i), (bg_width, i))
        pygame.draw.rect(bg, (255, 200, 50), (0, 0, bg_width, bg_height), 2, border_radius=25)
        surface.blit(bg, (x, y))

        # Key badge
        key_x = x + 20
        key_y = y + 10
        pygame.draw.rect(surface, (255, 200, 50), (key_x, key_y, 30, 30), border_radius=8)
        pygame.draw.rect(surface, (255, 230, 150), (key_x + 2, key_y + 2, 26, 26), border_radius=6)
        key_text = self.font.render("E", True, (40, 30, 0))
        surface.blit(key_text, (key_x + 9, key_y + 6))

        # Target name
        target_text = self.font.render(self.interact_target, True, WHITE)
        surface.blit(target_text, (x + 60, y + 15))

    def _draw_quest_tracker(self, surface, quest):
        """Draw current quest tracker"""
        tracker_x = UI_PADDING
        tracker_y = WINDOW_HEIGHT - 80

        # Background
        bg = pygame.Surface((250, 60), pygame.SRCALPHA)
        pygame.draw.rect(bg, (0, 0, 0, 180), (0, 0, 250, 60), border_radius=8)
        pygame.draw.rect(bg, ORANGE, (0, 0, 250, 60), 2, border_radius=8)
        surface.blit(bg, (tracker_x, tracker_y))

        # Quest title
        title = self.small_font.render("CURRENT QUEST", True, ORANGE)
        surface.blit(title, (tracker_x + 10, tracker_y + 5))

        # Quest description
        desc = self.font.render(quest.get('name', 'No active quest')[:30], True, WHITE)
        surface.blit(desc, (tracker_x + 10, tracker_y + 22))

        # Progress
        progress = quest.get('progress', 0)
        goal = quest.get('goal', 1)
        progress_text = self.small_font.render(f"Progress: {progress}/{goal}", True, LIGHT_GRAY)
        surface.blit(progress_text, (tracker_x + 10, tracker_y + 42))

    def _draw_notifications(self, surface):
        """Draw floating notifications with style"""
        base_y = WINDOW_HEIGHT // 2 - 50

        for i, (text, color, timer) in enumerate(self.notifications):
            # Fade and slide effect
            alpha = min(255, int(255 * (timer / 2.0)))
            slide_offset = int((2.0 - timer) * 10) if timer < 2.0 else 0
            y = base_y + i * 40 - slide_offset

            # Background pill
            text_surface = self.font.render(text, True, WHITE)
            bg_width = text_surface.get_width() + 30
            bg_height = 32
            x = (WINDOW_WIDTH - bg_width) // 2

            bg = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
            bg.set_alpha(alpha)
            # Handle color as tuple
            r, g, b = color[0], color[1], color[2]
            pygame.draw.rect(bg, (r, g, b), (0, 0, bg_width, bg_height), border_radius=16)
            pygame.draw.rect(bg, (min(255, r+50), min(255, g+50), min(255, b+50)), (0, 0, bg_width, bg_height), 2, border_radius=16)
            surface.blit(bg, (x, y))

            # Text
            text_surface.set_alpha(alpha)
            surface.blit(text_surface, (x + 15, y + 7))

    def draw_menu(self, surface, options, selected_index, title="MENU"):
        """Draw a menu overlay"""
        # Darken background
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))

        # Menu box
        menu_width = 400
        menu_height = 100 + len(options) * 50
        menu_x = (WINDOW_WIDTH - menu_width) // 2
        menu_y = (WINDOW_HEIGHT - menu_height) // 2

        pygame.draw.rect(surface, DARK_GRAY, (menu_x, menu_y, menu_width, menu_height), border_radius=10)
        pygame.draw.rect(surface, WHITE, (menu_x, menu_y, menu_width, menu_height), 3, border_radius=10)

        # Title
        title_surface = self.title_font.render(title, True, ORANGE)
        title_x = menu_x + (menu_width - title_surface.get_width()) // 2
        surface.blit(title_surface, (title_x, menu_y + 20))

        # Options
        for i, option in enumerate(options):
            y = menu_y + 70 + i * 50
            color = YELLOW if i == selected_index else WHITE

            option_surface = self.font.render(option, True, color)
            option_x = menu_x + (menu_width - option_surface.get_width()) // 2
            surface.blit(option_surface, (option_x, y))

            # Selection indicator
            if i == selected_index:
                pygame.draw.polygon(surface, YELLOW,
                    [(option_x - 20, y + 8), (option_x - 10, y + 3), (option_x - 10, y + 13)])
