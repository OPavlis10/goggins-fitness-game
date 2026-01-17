"""
Main Game class - ties all components together
"""
import pygame
import sys
from constants import *
from sprites import SpriteGenerator
from map import GameMap
from player import Player
from camera import Camera
from trainer import Trainer
from ui import UI
from quest import QuestManager
from inventory import Inventory
from shop import Shop, InventoryUI
from save_system import SaveSystem
from minigames import MiniGameManager
from npc import NPCManager


class Game:
    """Main game class managing all game systems"""

    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0  # Delta time

        # Game states
        self.state = 'menu'  # menu, playing, paused, shop, inventory, irl_quests, minigame
        self.menu_selection = 0
        self.menu_options = ['New Game', 'Continue', 'Quit']

        # Core systems
        self.sprites = SpriteGenerator()
        self.game_map = None
        self.player = None
        self.camera = None
        self.npc_manager = None
        self.trainer = Trainer()
        self.ui = UI(self.sprites)
        self.quest_manager = QuestManager()
        self.inventory = Inventory()
        self.shop = Shop()
        self.inventory_ui = InventoryUI()
        self.save_system = SaveSystem()
        self.minigame_manager = MiniGameManager()

        # Initialize fonts for all UI components
        self.trainer.init_fonts()
        self.ui.init_fonts()
        self.shop.init_fonts()
        self.inventory_ui.init_fonts()
        self.minigame_manager.init_fonts()

        # Pause menu
        self.pause_selection = 0
        self.pause_options = ['Resume', 'Save Game', 'IRL Quests', 'Quit to Menu']

        # IRL quest UI
        self.irl_selection = 0

        # Result display
        self.result_display = None  # {'text': str, 'timer': float}

        # Check for existing save
        if self.save_system.save_exists():
            self.menu_options = ['New Game', 'Continue', 'Quit']
        else:
            self.menu_options = ['New Game', 'Quit']

    def run(self):
        """Main game loop"""
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000.0  # Convert to seconds
            self.handle_events()
            self.update()
            self.draw()

        self.quit()

    def handle_events(self):
        """Handle all input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            # Delegate to current state handler
            if self.state == 'menu':
                self._handle_menu_event(event)
            elif self.state == 'playing':
                self._handle_playing_event(event)
            elif self.state == 'paused':
                self._handle_pause_event(event)
            elif self.state == 'shop':
                self._handle_shop_event(event)
            elif self.state == 'inventory':
                self._handle_inventory_event(event)
            elif self.state == 'irl_quests':
                self._handle_irl_event(event)
            elif self.state == 'minigame':
                self._handle_minigame_event(event)

    def _handle_menu_event(self, event):
        """Handle menu input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.menu_selection = (self.menu_selection - 1) % len(self.menu_options)
            elif event.key == pygame.K_DOWN:
                self.menu_selection = (self.menu_selection + 1) % len(self.menu_options)
            elif event.key == pygame.K_RETURN:
                self._menu_select()
            elif event.key == pygame.K_ESCAPE:
                self.running = False

    def _menu_select(self):
        """Handle menu selection"""
        option = self.menu_options[self.menu_selection]

        if option == 'New Game':
            self._start_new_game()
        elif option == 'Continue':
            self._load_game()
        elif option == 'Quit':
            self.running = False

    def _start_new_game(self):
        """Start a new game"""
        # Initialize game objects
        self.game_map = GameMap(self.sprites)
        spawn = self.game_map.spawn_point
        self.player = Player(spawn[0], spawn[1], self.sprites)
        self.camera = Camera(self.game_map.pixel_width, self.game_map.pixel_height)

        # Create NPCs (more for bigger map with pool)
        self.npc_manager = NPCManager(self.sprites, self.game_map, count=9)

        # Reset systems
        self.quest_manager = QuestManager()
        self.inventory = Inventory()

        # Welcome message from trainer
        self.trainer.welcome()

        self.state = 'playing'

    def _load_game(self):
        """Load saved game"""
        # Initialize objects first
        self.game_map = GameMap(self.sprites)
        spawn = self.game_map.spawn_point
        self.player = Player(spawn[0], spawn[1], self.sprites)
        self.camera = Camera(self.game_map.pixel_width, self.game_map.pixel_height)

        # Create NPCs (more for bigger map with pool)
        self.npc_manager = NPCManager(self.sprites, self.game_map, count=9)

        # Load data
        success, message = self.save_system.load_game(
            self.player, self.quest_manager, self.inventory)

        if success:
            self.ui.add_notification("Game loaded!", GREEN)
            self.trainer.show_message('welcome')
            self.state = 'playing'
        else:
            self.ui.add_notification(message, RED)

    def _handle_playing_event(self, event):
        """Handle gameplay input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state = 'paused'
                self.pause_selection = 0

            elif event.key == pygame.K_e:
                self._handle_interaction()

            elif event.key == pygame.K_i:
                self.inventory_ui.open()
                self.state = 'inventory'

            elif event.key == pygame.K_TAB:
                # Quick access to IRL quests
                self.irl_selection = 0
                self.state = 'irl_quests'

    def _handle_interaction(self):
        """Handle player interaction with nearby objects"""
        if not self.player or not self.player.can_interact():
            return

        center = self.player.get_center()
        nearby = self.game_map.get_nearby_interactive(center[0], center[1])

        if not nearby:
            return

        tile = nearby[0]
        self.player.set_interact_cooldown()

        # Handle different interaction types
        if tile.type == TILE_SHOP:
            self.shop.open()
            self.state = 'shop'
            self.trainer.on_equipment_interact(tile.name)

        elif tile.type == TILE_TRAINER:
            self.trainer.on_equipment_interact(tile.name)
            # Could open a special trainer menu here

        elif tile.type == TILE_MIRROR:
            # Show player stats in detail
            self.trainer.on_equipment_interact(tile.name)
            self.ui.add_notification(
                f"Muscle Level: {self.player.muscle_level}/7", YELLOW, 3.0)

        elif tile.interactive and tile.stat:
            # Equipment - start mini-game
            if self.minigame_manager.start_game(tile.name):
                self.state = 'minigame'
                self.trainer.on_equipment_interact(tile.name)

    def _handle_pause_event(self, event):
        """Handle pause menu input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state = 'playing'
            elif event.key == pygame.K_UP:
                self.pause_selection = (self.pause_selection - 1) % len(self.pause_options)
            elif event.key == pygame.K_DOWN:
                self.pause_selection = (self.pause_selection + 1) % len(self.pause_options)
            elif event.key == pygame.K_RETURN:
                self._pause_select()

    def _pause_select(self):
        """Handle pause menu selection"""
        option = self.pause_options[self.pause_selection]

        if option == 'Resume':
            self.state = 'playing'
        elif option == 'Save Game':
            success, message = self.save_system.save_game(
                self.player, self.quest_manager, self.inventory)
            self.ui.add_notification(message, GREEN if success else RED)
            self.state = 'playing'
        elif option == 'IRL Quests':
            self.irl_selection = 0
            self.state = 'irl_quests'
        elif option == 'Quit to Menu':
            self.state = 'menu'
            self.menu_selection = 0

    def _handle_shop_event(self, event):
        """Handle shop input"""
        action, message = self.shop.handle_input(event, self.player, self.inventory)

        if action == 'close':
            self.state = 'playing'
        elif action == 'purchase':
            self.ui.add_notification(message, GREEN)
        elif action == 'error':
            self.ui.add_notification(message, RED)

    def _handle_inventory_event(self, event):
        """Handle inventory input"""
        action, message = self.inventory_ui.handle_input(event, self.player, self.inventory)

        if action == 'close':
            self.state = 'playing'
        elif action == 'use':
            self.ui.add_notification(message, GREEN)
        elif action == 'error':
            self.ui.add_notification(message, RED)

    def _handle_irl_event(self, event):
        """Handle IRL quest menu"""
        if event.type == pygame.KEYDOWN:
            irl_quests = self.quest_manager.get_irl_quests()

            if event.key == pygame.K_ESCAPE:
                self.state = 'playing' if self.player else 'paused'

            elif event.key == pygame.K_UP:
                if irl_quests:
                    self.irl_selection = (self.irl_selection - 1) % len(irl_quests)

            elif event.key == pygame.K_DOWN:
                if irl_quests:
                    self.irl_selection = (self.irl_selection + 1) % len(irl_quests)

            elif event.key == pygame.K_RETURN or event.key == pygame.K_e:
                quest = self.quest_manager.complete_irl_quest(self.irl_selection)
                if quest:
                    xp, currency = self.quest_manager.claim_quest_rewards(quest, self.player)
                    self.trainer.on_quest_complete(is_irl=True)

                    # Check for streak bonus
                    if self.quest_manager.current_streak >= 3:
                        self.trainer.queue_message('streak')

                    self.ui.add_notification(
                        f"IRL Quest done! +{xp} XP, +${currency}", GREEN, 3.0)

    def _handle_minigame_event(self, event):
        """Handle mini-game input"""
        self.minigame_manager.handle_event(event)

    def update(self):
        """Update game logic"""
        if self.state == 'playing':
            self._update_playing()
        elif self.state == 'minigame':
            self._update_minigame()

        # Always update UI
        self.ui.update(self.dt)

        # Update result display
        if self.result_display:
            self.result_display['timer'] -= self.dt
            if self.result_display['timer'] <= 0:
                self.result_display = None

    def _update_playing(self):
        """Update gameplay"""
        if not self.player or not self.game_map:
            return

        keys = pygame.key.get_pressed()
        self.player.update(keys, self.game_map, self.dt)

        # Update NPCs
        if self.npc_manager:
            self.npc_manager.update(self.dt, self.game_map)

        # Update camera
        center = self.player.get_center()
        self.camera.update(center[0], center[1])

        # Update trainer
        self.trainer.update(self.dt, self.player.is_moving)

        # Check for nearby interactive objects
        nearby = self.game_map.get_nearby_interactive(center[0], center[1])
        if nearby:
            self.ui.set_interact_prompt(True, nearby[0].name)
        else:
            self.ui.set_interact_prompt(False)

    def _update_minigame(self):
        """Update mini-game"""
        keys = pygame.key.get_pressed()
        self.minigame_manager.update(self.dt, keys)

        # Check if complete
        if self.minigame_manager.is_complete():
            result = self.minigame_manager.get_result()
            if result:
                # Apply rewards
                xp_gained = result['xp_reward']

                # Get equipment stat from tile properties
                equipment = result['equipment']
                for tile_type, props in TILE_PROPERTIES.items():
                    if props.get('name') == equipment:
                        stat = props.get('stat')
                        base_xp = props.get('xp', 0)
                        xp_gained += base_xp

                        # Add XP and check level up
                        if self.player.add_xp(xp_gained):
                            self.trainer.on_level_up(self.player.stats['level'])

                        # Add to stat
                        if stat:
                            self.player.add_stat(stat, 1)

                        # Update quest progress
                        quest = self.quest_manager.on_equipment_use(equipment)
                        if quest:
                            xp, currency = self.quest_manager.claim_quest_rewards(
                                quest, self.player)
                            self.trainer.on_quest_complete()
                            self.ui.add_notification(
                                f"Quest complete! +{xp} XP, +${currency}", GREEN, 3.0)

                        break

                # Currency for completing
                self.player.add_currency(5)

                # Show result
                if result['success']:
                    self.trainer.show_message('success')
                    self.ui.add_notification(
                        f"+{xp_gained} XP, +$5", GREEN)
                else:
                    self.trainer.show_message('fail')
                    self.ui.add_notification(
                        f"+{xp_gained} XP (try harder!)", YELLOW)

            self.minigame_manager.clear()
            self.state = 'playing'

    def draw(self):
        """Draw everything"""
        self.screen.fill(BLACK)

        if self.state == 'menu':
            self._draw_menu()
        elif self.state in ['playing', 'paused', 'shop', 'inventory', 'irl_quests']:
            self._draw_game()

            if self.state == 'paused':
                self._draw_pause_menu()
            elif self.state == 'shop':
                self.shop.draw(self.screen, self.player)
            elif self.state == 'inventory':
                self.inventory_ui.draw(self.screen, self.inventory)
            elif self.state == 'irl_quests':
                self._draw_irl_quests()

        elif self.state == 'minigame':
            self._draw_game()
            self.minigame_manager.draw(self.screen)

        pygame.display.flip()

    def _draw_menu(self):
        """Draw main menu"""
        # Title
        font = pygame.font.Font(None, 64)
        title = font.render(GAME_TITLE.upper(), True, ORANGE)
        title_x = (WINDOW_WIDTH - title.get_width()) // 2
        self.screen.blit(title, (title_x, 100))

        # Subtitle
        sub_font = pygame.font.Font(None, 28)
        subtitle = sub_font.render("Stay Hard. Get Fit. No Excuses.", True, GRAY)
        sub_x = (WINDOW_WIDTH - subtitle.get_width()) // 2
        self.screen.blit(subtitle, (sub_x, 170))

        # Save info if exists
        save_info = self.save_system.get_save_info()
        if save_info and 'Continue' in self.menu_options:
            info_text = sub_font.render(
                f"Save: Level {save_info['level']}, ${save_info['currency']}", True, GREEN)
            info_x = (WINDOW_WIDTH - info_text.get_width()) // 2
            self.screen.blit(info_text, (info_x, 220))

        # Menu options
        menu_font = pygame.font.Font(None, 36)
        y = 300

        for i, option in enumerate(self.menu_options):
            color = YELLOW if i == self.menu_selection else WHITE
            text = menu_font.render(option, True, color)
            text_x = (WINDOW_WIDTH - text.get_width()) // 2

            if i == self.menu_selection:
                # Draw selection indicator
                pygame.draw.polygon(self.screen, YELLOW,
                    [(text_x - 25, y + 10), (text_x - 15, y + 5), (text_x - 15, y + 15)])

            self.screen.blit(text, (text_x, y))
            y += 50

        # Controls hint
        hint_font = pygame.font.Font(None, 20)
        hint = hint_font.render("UP/DOWN: Navigate | ENTER: Select | ESC: Quit", True, GRAY)
        hint_x = (WINDOW_WIDTH - hint.get_width()) // 2
        self.screen.blit(hint, (hint_x, WINDOW_HEIGHT - 50))

    def _draw_game(self):
        """Draw game world"""
        if not self.player or not self.game_map or not self.camera:
            return

        # Draw map
        self.game_map.draw(self.screen, self.camera)

        # Draw NPCs
        if self.npc_manager:
            self.npc_manager.draw(self.screen, self.camera)

        # Draw player
        self.player.draw(self.screen, self.camera)

        # Draw UI overlay
        current_quest = self.quest_manager.get_active_quest()
        self.ui.draw(self.screen, self.player, current_quest)

        # Draw trainer messages
        self.trainer.draw(self.screen)

    def _draw_pause_menu(self):
        """Draw pause menu overlay"""
        self.ui.draw_menu(self.screen, self.pause_options, self.pause_selection, "PAUSED")

    def _draw_irl_quests(self):
        """Draw IRL quests overlay"""
        # Darken background
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        # Window
        win_width = 500
        win_height = 400
        win_x = (WINDOW_WIDTH - win_width) // 2
        win_y = (WINDOW_HEIGHT - win_height) // 2

        pygame.draw.rect(self.screen, DARK_GRAY,
                        (win_x, win_y, win_width, win_height), border_radius=10)
        pygame.draw.rect(self.screen, PURPLE,
                        (win_x, win_y, win_width, win_height), 3, border_radius=10)

        # Title
        title_font = pygame.font.Font(None, 32)
        title = title_font.render("IRL QUESTS - Real Life Challenges!", True, PURPLE)
        title_x = win_x + (win_width - title.get_width()) // 2
        self.screen.blit(title, (title_x, win_y + 15))

        # Streak info
        streak_font = pygame.font.Font(None, 24)
        streak_text = streak_font.render(
            f"Current Streak: {self.quest_manager.current_streak} days | "
            f"Best: {self.quest_manager.best_streak} | "
            f"Bonus: x{self.quest_manager.get_streak_bonus():.2f}",
            True, YELLOW)
        self.screen.blit(streak_text, (win_x + 20, win_y + 50))

        # Quests
        irl_quests = self.quest_manager.get_irl_quests()
        quest_y = win_y + 90
        quest_font = pygame.font.Font(None, 24)
        small_font = pygame.font.Font(None, 18)

        if not irl_quests:
            no_quest = quest_font.render("All IRL quests completed today!", True, GREEN)
            self.screen.blit(no_quest, (win_x + 20, quest_y))
        else:
            for i, quest in enumerate(irl_quests):
                # Selection highlight
                if i == self.irl_selection:
                    pygame.draw.rect(self.screen, (60, 60, 80),
                                   (win_x + 10, quest_y - 5, win_width - 20, 70),
                                   border_radius=5)

                # Quest name
                if quest['completed']:
                    color = GREEN
                    name_text = f"[DONE] {quest['name']}"
                else:
                    color = YELLOW if i == self.irl_selection else WHITE
                    name_text = quest['name']

                name = quest_font.render(name_text, True, color)
                self.screen.blit(name, (win_x + 20, quest_y))

                # Description
                desc = small_font.render(quest['description'], True, LIGHT_GRAY)
                self.screen.blit(desc, (win_x + 30, quest_y + 22))

                # Reward
                reward = small_font.render(
                    f"Reward: {quest['xp_reward']} XP, ${quest['currency_reward']}", True, GREEN)
                self.screen.blit(reward, (win_x + 30, quest_y + 40))

                quest_y += 80

        # Instructions
        instr_font = pygame.font.Font(None, 18)
        instr = instr_font.render(
            "UP/DOWN: Navigate | ENTER: Mark Complete | ESC: Close", True, GRAY)
        self.screen.blit(instr, (win_x + 20, win_y + win_height - 30))

    def quit(self):
        """Clean up and quit"""
        pygame.mixer.quit()
        pygame.quit()
        sys.exit()
