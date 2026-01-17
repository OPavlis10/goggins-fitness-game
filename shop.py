"""
Shop system for buying supplements and items
"""
import pygame
from constants import *


class Shop:
    """In-game shop for supplements and items"""

    def __init__(self):
        self.is_open = False
        self.selected_index = 0
        self.items = list(SHOP_ITEMS.keys())

        # Fonts
        self.font = None
        self.title_font = None
        self.small_font = None

    def init_fonts(self):
        """Initialize fonts (call after pygame.init)"""
        self.font = pygame.font.Font(None, UI_FONT_SIZE)
        self.title_font = pygame.font.Font(None, UI_TITLE_FONT_SIZE)
        self.small_font = pygame.font.Font(None, 16)

    def open(self):
        """Open the shop"""
        self.is_open = True
        self.selected_index = 0

    def close(self):
        """Close the shop"""
        self.is_open = False

    def toggle(self):
        """Toggle shop open/closed"""
        self.is_open = not self.is_open
        if self.is_open:
            self.selected_index = 0

    def handle_input(self, event, player, inventory):
        """Handle shop input, returns (action, message)"""
        if not self.is_open:
            return None, None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.close()
                return 'close', None

            elif event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.items)
                return 'navigate', None

            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.items)
                return 'navigate', None

            elif event.key == pygame.K_RETURN or event.key == pygame.K_e:
                return self._purchase(player, inventory)

        return None, None

    def _purchase(self, player, inventory):
        """Attempt to purchase selected item"""
        if self.selected_index >= len(self.items):
            return 'error', "Invalid selection"

        item_id = self.items[self.selected_index]
        item_data = SHOP_ITEMS.get(item_id)

        if not item_data:
            return 'error', "Item not found"

        price = item_data['price']

        if player.stats['currency'] < price:
            return 'error', f"Not enough money! Need ${price}"

        if inventory.is_full():
            return 'error', "Inventory is full!"

        # Make purchase
        player.spend_currency(price)
        inventory.add_item(item_id)

        return 'purchase', f"Bought {item_data['name']}!"

    def draw(self, surface, player):
        """Draw shop interface"""
        if not self.is_open or not self.font:
            return

        # Darken background
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        # Shop window
        shop_width = 500
        shop_height = 400
        shop_x = (WINDOW_WIDTH - shop_width) // 2
        shop_y = (WINDOW_HEIGHT - shop_height) // 2

        # Background
        pygame.draw.rect(surface, DARK_GRAY,
                        (shop_x, shop_y, shop_width, shop_height), border_radius=10)
        pygame.draw.rect(surface, ORANGE,
                        (shop_x, shop_y, shop_width, shop_height), 3, border_radius=10)

        # Title
        title = self.title_font.render("SUPPLEMENT SHOP", True, ORANGE)
        title_x = shop_x + (shop_width - title.get_width()) // 2
        surface.blit(title, (title_x, shop_y + 15))

        # Player currency
        currency = self.font.render(f"Your Money: ${player.stats['currency']}", True, YELLOW)
        surface.blit(currency, (shop_x + 20, shop_y + 50))

        # Items
        item_y = shop_y + 90
        for i, item_id in enumerate(self.items):
            item_data = SHOP_ITEMS.get(item_id, {})

            # Selection highlight
            if i == self.selected_index:
                pygame.draw.rect(surface, (60, 60, 80),
                               (shop_x + 10, item_y - 5, shop_width - 20, 65),
                               border_radius=5)

            # Item name
            name_color = YELLOW if i == self.selected_index else WHITE
            name = self.font.render(item_data.get('name', item_id), True, name_color)
            surface.blit(name, (shop_x + 20, item_y))

            # Price
            price = item_data.get('price', 0)
            can_afford = player.stats['currency'] >= price
            price_color = GREEN if can_afford else RED
            price_text = self.font.render(f"${price}", True, price_color)
            surface.blit(price_text, (shop_x + shop_width - 80, item_y))

            # Description
            desc = self.small_font.render(item_data.get('description', ''), True, LIGHT_GRAY)
            surface.blit(desc, (shop_x + 30, item_y + 25))

            # Effect indicator
            effect = item_data.get('effect', '')
            if 'boost' in effect:
                duration = item_data.get('duration', 0)
                dur_text = self.small_font.render(f"Duration: {duration}s", True, GRAY)
                surface.blit(dur_text, (shop_x + 30, item_y + 42))

            item_y += 70

        # Instructions
        instructions = self.small_font.render(
            "UP/DOWN: Navigate | ENTER: Buy | ESC: Close", True, GRAY)
        surface.blit(instructions, (shop_x + 20, shop_y + shop_height - 30))


class InventoryUI:
    """UI for viewing and using inventory items"""

    def __init__(self):
        self.is_open = False
        self.selected_index = 0
        self.font = None
        self.title_font = None
        self.small_font = None

    def init_fonts(self):
        """Initialize fonts"""
        self.font = pygame.font.Font(None, UI_FONT_SIZE)
        self.title_font = pygame.font.Font(None, UI_TITLE_FONT_SIZE)
        self.small_font = pygame.font.Font(None, 16)

    def open(self):
        self.is_open = True
        self.selected_index = 0

    def close(self):
        self.is_open = False

    def toggle(self):
        self.is_open = not self.is_open
        if self.is_open:
            self.selected_index = 0

    def handle_input(self, event, player, inventory):
        """Handle inventory input"""
        if not self.is_open:
            return None, None

        items = inventory.get_all_items()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_i:
                self.close()
                return 'close', None

            elif event.key == pygame.K_UP:
                if items:
                    self.selected_index = (self.selected_index - 1) % len(items)
                return 'navigate', None

            elif event.key == pygame.K_DOWN:
                if items:
                    self.selected_index = (self.selected_index + 1) % len(items)
                return 'navigate', None

            elif event.key == pygame.K_RETURN or event.key == pygame.K_e:
                if items and 0 <= self.selected_index < len(items):
                    item = items[self.selected_index]
                    success, msg = inventory.use_item(item.id, player)
                    if success:
                        # Adjust selection if needed
                        items = inventory.get_all_items()
                        if self.selected_index >= len(items):
                            self.selected_index = max(0, len(items) - 1)
                    return 'use' if success else 'error', msg

        return None, None

    def draw(self, surface, inventory):
        """Draw inventory interface"""
        if not self.is_open or not self.font:
            return

        items = inventory.get_all_items()

        # Darken background
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        # Inventory window
        inv_width = 400
        inv_height = 350
        inv_x = (WINDOW_WIDTH - inv_width) // 2
        inv_y = (WINDOW_HEIGHT - inv_height) // 2

        pygame.draw.rect(surface, DARK_GRAY,
                        (inv_x, inv_y, inv_width, inv_height), border_radius=10)
        pygame.draw.rect(surface, GREEN,
                        (inv_x, inv_y, inv_width, inv_height), 3, border_radius=10)

        # Title
        title = self.title_font.render("INVENTORY", True, GREEN)
        title_x = inv_x + (inv_width - title.get_width()) // 2
        surface.blit(title, (title_x, inv_y + 15))

        if not items:
            empty = self.font.render("Inventory is empty", True, GRAY)
            empty_x = inv_x + (inv_width - empty.get_width()) // 2
            surface.blit(empty, (empty_x, inv_y + 100))
        else:
            # Draw items
            item_y = inv_y + 60
            for i, item in enumerate(items):
                # Selection highlight
                if i == self.selected_index:
                    pygame.draw.rect(surface, (60, 80, 60),
                                   (inv_x + 10, item_y - 5, inv_width - 20, 50),
                                   border_radius=5)

                # Item name and quantity
                name_color = YELLOW if i == self.selected_index else WHITE
                name = self.font.render(f"{item.name} x{item.quantity}", True, name_color)
                surface.blit(name, (inv_x + 20, item_y))

                # Description
                desc = self.small_font.render(item.description, True, LIGHT_GRAY)
                surface.blit(desc, (inv_x + 30, item_y + 22))

                item_y += 55

        # Instructions
        instructions = self.small_font.render(
            "UP/DOWN: Navigate | ENTER: Use | I/ESC: Close", True, GRAY)
        surface.blit(instructions, (inv_x + 20, inv_y + inv_height - 30))
