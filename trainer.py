"""
Trainer system with Goggins-style motivational messages
"""
import pygame
import random
from constants import *


class Trainer:
    """The motivational trainer inspired by David Goggins"""

    # Motivational messages by category
    MESSAGES = {
        'welcome': [
            "Welcome to the pain cave. Let's get to work!",
            "Another day to become uncommon. Let's go!",
            "Your mind will quit a thousand times before your body does.",
            "Time to callous your mind. No excuses!",
            "The only easy day was yesterday. Get moving!"
        ],
        'success': [
            "That's what I'm talking about! Stay hard!",
            "You just did what 99% of people won't. Keep going!",
            "One more rep for the mind! You're building mental armor!",
            "Excellence is a habit. You're proving that right now!",
            "You didn't come this far to only come this far!",
            "That's growth right there. Embrace the suck!"
        ],
        'level_up': [
            "NEW LEVEL! But remember - levels don't lift themselves!",
            "You just evolved! Now do it again!",
            "Stronger body, stronger mind. Keep stacking wins!",
            "That's what happens when you don't quit!",
            "You're becoming uncommon among uncommon people!"
        ],
        'fail': [
            "Get back up! Failure is just feedback!",
            "You think this is hard? Life is hard. Keep pushing!",
            "That's just round one. Champions get up!",
            "Pain is weakness leaving the body. Embrace it!",
            "You're not done until YOU say you're done!"
        ],
        'idle': [
            "Why are you standing still? The iron won't lift itself!",
            "Comfort is the enemy of progress. MOVE!",
            "You didn't come here to spectate!",
            "Every second you waste is a rep you'll never get back!",
            "Are you a spectator or a participant? DECIDE!"
        ],
        'irl_complete': [
            "You did the work in REAL LIFE! That's the real test!",
            "From the game to the streets! That's a true warrior!",
            "Real world reps hit different. Proud of you!",
            "You're not just playing - you're BECOMING!",
            "That's the real accountability right there!"
        ],
        'streak': [
            "STREAK BONUS! Consistency is the ultimate superpower!",
            "Day after day! This is how champions are made!",
            "That streak shows DISCIPLINE. Keep it going!",
            "Your past self would be proud. Don't let them down!",
            "Momentum is everything. STAY HARD!"
        ],
        'equipment': {
            'Bench Press': "Time to build that chest! Press like your life depends on it!",
            'Squat Rack': "Leg day? Every day is leg day! Get under that bar!",
            'Treadmill': "Running from weakness, running TO strength!",
            'Dumbbells': "Grab those weights! Every rep is a vote for who you want to be!",
            'Mirror': "Look at yourself. That's your competition. Beat THAT person!",
            'Supplement Shop': "Fuel the machine. But remember - supplements don't replace hard work!",
            'Trainer Goggins': "What do you want to know? I've got answers and assignments!"
        }
    }

    def __init__(self):
        self.current_message = None
        self.message_timer = 0
        self.message_duration = 4.0  # seconds
        self.message_queue = []

        # Font for messages
        self.font = None
        self.title_font = None

        # Message display settings
        self.box_padding = 15
        self.box_margin = 20

        # Track player activity
        self.last_activity_time = 0
        self.idle_threshold = 10.0  # seconds before idle message

    def init_fonts(self):
        """Initialize fonts (must be called after pygame.init)"""
        self.font = pygame.font.Font(None, UI_FONT_SIZE)
        self.title_font = pygame.font.Font(None, UI_TITLE_FONT_SIZE)

    def get_message(self, category, equipment_name=None):
        """Get a random message from category"""
        if category == 'equipment' and equipment_name:
            return self.MESSAGES['equipment'].get(equipment_name,
                   f"Use that {equipment_name}! Every rep counts!")

        messages = self.MESSAGES.get(category, self.MESSAGES['success'])
        return random.choice(messages)

    def show_message(self, category, equipment_name=None, duration=None):
        """Display a message from the trainer"""
        message = self.get_message(category, equipment_name)
        self.current_message = message
        self.message_timer = duration if duration else self.message_duration

    def queue_message(self, category, equipment_name=None, duration=None):
        """Add message to queue (for multiple messages)"""
        message = self.get_message(category, equipment_name)
        dur = duration if duration else self.message_duration
        self.message_queue.append((message, dur))

    def update(self, dt, player_moving):
        """Update trainer state"""
        # Update message timer
        if self.message_timer > 0:
            self.message_timer -= dt
            if self.message_timer <= 0:
                self.current_message = None
                # Check queue
                if self.message_queue:
                    msg, dur = self.message_queue.pop(0)
                    self.current_message = msg
                    self.message_timer = dur

        # Track idle time
        if player_moving:
            self.last_activity_time = 0
        else:
            self.last_activity_time += dt
            # Show idle message if player inactive
            if self.last_activity_time >= self.idle_threshold and not self.current_message:
                self.show_message('idle')
                self.last_activity_time = 0  # Reset so we don't spam

    def draw(self, surface):
        """Draw current message if any"""
        if not self.current_message or not self.font:
            return

        # Word wrap the message
        words = self.current_message.split(' ')
        lines = []
        current_line = []
        max_width = WINDOW_WIDTH - self.box_margin * 4

        for word in words:
            test_line = ' '.join(current_line + [word])
            test_surface = self.font.render(test_line, True, WHITE)
            if test_surface.get_width() <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))

        # Calculate box size
        line_height = self.font.get_linesize()
        box_height = len(lines) * line_height + self.box_padding * 2 + 30  # Extra for title
        box_width = max_width + self.box_padding * 2

        # Draw message box at top center
        box_x = (WINDOW_WIDTH - box_width) // 2
        box_y = self.box_margin

        # Background with transparency
        box_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        pygame.draw.rect(box_surface, (0, 0, 0, 220), (0, 0, box_width, box_height), border_radius=10)
        pygame.draw.rect(box_surface, ORANGE, (0, 0, box_width, box_height), 3, border_radius=10)
        surface.blit(box_surface, (box_x, box_y))

        # Draw "COACH SAYS:" title
        title = self.title_font.render("COACH SAYS:", True, ORANGE)
        surface.blit(title, (box_x + self.box_padding, box_y + self.box_padding))

        # Draw message lines
        y_offset = box_y + self.box_padding + 28
        for line in lines:
            text = self.font.render(line, True, WHITE)
            surface.blit(text, (box_x + self.box_padding, y_offset))
            y_offset += line_height

    def on_level_up(self, new_level):
        """Called when player levels up"""
        self.show_message('level_up', duration=5.0)

    def on_quest_complete(self, is_irl=False):
        """Called when quest is completed"""
        if is_irl:
            self.show_message('irl_complete', duration=5.0)
        else:
            self.show_message('success')

    def on_equipment_interact(self, equipment_name):
        """Called when player interacts with equipment"""
        self.show_message('equipment', equipment_name)

    def on_streak(self, streak_days):
        """Called when player maintains a streak"""
        self.show_message('streak', duration=5.0)

    def welcome(self):
        """Show welcome message"""
        self.show_message('welcome', duration=5.0)
