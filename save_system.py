"""
Save/Load system for game persistence
"""
import json
import os
from datetime import datetime
from constants import SAVE_FILE


class SaveSystem:
    """Handles saving and loading game state"""

    def __init__(self, save_path=None):
        self.save_path = save_path or SAVE_FILE

    def save_exists(self):
        """Check if a save file exists"""
        return os.path.exists(self.save_path)

    def save_game(self, player, quest_manager, inventory, settings=None):
        """Save game state to file"""
        save_data = {
            'version': '1.0',
            'timestamp': datetime.now().isoformat(),
            'player': player.to_dict(),
            'quests': quest_manager.to_dict(),
            'inventory': inventory.to_dict(),
            'settings': settings or {}
        }

        try:
            with open(self.save_path, 'w') as f:
                json.dump(save_data, f, indent=2)
            return True, "Game saved successfully!"
        except Exception as e:
            return False, f"Failed to save: {str(e)}"

    def load_game(self, player, quest_manager, inventory):
        """Load game state from file"""
        if not self.save_exists():
            return False, "No save file found"

        try:
            with open(self.save_path, 'r') as f:
                save_data = json.load(f)

            # Load player data
            player.from_dict(save_data.get('player', {}))

            # Load quest data
            quest_manager.from_dict(save_data.get('quests', {}))

            # Load inventory
            inventory.from_dict(save_data.get('inventory', {}))

            # Return settings for game to apply
            settings = save_data.get('settings', {})

            return True, "Game loaded successfully!"

        except json.JSONDecodeError:
            return False, "Save file is corrupted"
        except Exception as e:
            return False, f"Failed to load: {str(e)}"

    def delete_save(self):
        """Delete the save file"""
        if self.save_exists():
            try:
                os.remove(self.save_path)
                return True, "Save deleted"
            except Exception as e:
                return False, f"Failed to delete: {str(e)}"
        return False, "No save to delete"

    def get_save_info(self):
        """Get information about the save file"""
        if not self.save_exists():
            return None

        try:
            with open(self.save_path, 'r') as f:
                save_data = json.load(f)

            player_data = save_data.get('player', {})
            stats = player_data.get('stats', {})

            return {
                'timestamp': save_data.get('timestamp', 'Unknown'),
                'level': stats.get('level', 1),
                'strength': stats.get('strength', 1),
                'endurance': stats.get('endurance', 1),
                'currency': stats.get('currency', 0)
            }
        except:
            return None
