"""
Inventory system for managing player items
"""
from constants import SHOP_ITEMS


class InventoryItem:
    """Represents an item in inventory"""

    def __init__(self, item_id, quantity=1):
        self.id = item_id
        self.quantity = quantity

        # Get item data from constants
        item_data = SHOP_ITEMS.get(item_id, {})
        self.name = item_data.get('name', 'Unknown Item')
        self.effect = item_data.get('effect', None)
        self.value = item_data.get('value', 0)
        self.duration = item_data.get('duration', 0)
        self.description = item_data.get('description', '')

    def use(self, player):
        """Use the item on player, returns True if consumed"""
        if self.quantity <= 0:
            return False

        if self.effect == 'instant_xp':
            player.add_xp(int(self.value))
            self.quantity -= 1
            return True

        elif self.effect in ['strength_xp_boost', 'speed_boost', 'all_xp_boost']:
            player.apply_buff(self.effect, self.value, self.duration)
            self.quantity -= 1
            return True

        return False

    def to_dict(self):
        """Convert to dictionary for saving"""
        return {
            'id': self.id,
            'quantity': self.quantity
        }


class Inventory:
    """Manages player's inventory"""

    def __init__(self, max_slots=20):
        self.items = {}  # {item_id: InventoryItem}
        self.max_slots = max_slots

    def add_item(self, item_id, quantity=1):
        """Add item to inventory"""
        if item_id in self.items:
            self.items[item_id].quantity += quantity
        else:
            if len(self.items) >= self.max_slots:
                return False  # Inventory full
            self.items[item_id] = InventoryItem(item_id, quantity)
        return True

    def remove_item(self, item_id, quantity=1):
        """Remove item from inventory"""
        if item_id not in self.items:
            return False

        item = self.items[item_id]
        if item.quantity < quantity:
            return False

        item.quantity -= quantity
        if item.quantity <= 0:
            del self.items[item_id]
        return True

    def use_item(self, item_id, player):
        """Use an item on the player"""
        if item_id not in self.items:
            return False, "Item not in inventory"

        item = self.items[item_id]
        if item.use(player):
            if item.quantity <= 0:
                del self.items[item_id]
            return True, f"Used {item.name}"
        return False, "Cannot use this item"

    def get_item(self, item_id):
        """Get item by ID"""
        return self.items.get(item_id)

    def get_quantity(self, item_id):
        """Get quantity of an item"""
        item = self.items.get(item_id)
        return item.quantity if item else 0

    def get_all_items(self):
        """Get list of all items"""
        return list(self.items.values())

    def is_full(self):
        """Check if inventory is full"""
        return len(self.items) >= self.max_slots

    def to_dict(self):
        """Convert to dictionary for saving"""
        return {
            'items': [item.to_dict() for item in self.items.values()]
        }

    def from_dict(self, data):
        """Load from dictionary"""
        self.items = {}
        for item_data in data.get('items', []):
            item = InventoryItem(item_data['id'], item_data['quantity'])
            self.items[item.id] = item
