"""
Quest system for in-game and IRL quests
"""
import pygame
from datetime import datetime, date
from constants import *


class Quest:
    """Represents a single quest"""

    def __init__(self, quest_id, name, description, quest_type, goal,
                 xp_reward=0, currency_reward=0, stat_reward=None):
        self.id = quest_id
        self.name = name
        self.description = description
        self.type = quest_type  # 'use_equipment', 'visit', 'level_up', 'irl'
        self.goal = goal  # Target count or value
        self.progress = 0
        self.completed = False

        # Rewards
        self.xp_reward = xp_reward
        self.currency_reward = currency_reward
        self.stat_reward = stat_reward  # {'stat_name': amount}

        # For IRL quests
        self.is_irl = quest_type == 'irl'

    def update_progress(self, amount=1):
        """Update quest progress"""
        if not self.completed:
            self.progress += amount
            if self.progress >= self.goal:
                self.progress = self.goal
                self.completed = True
                return True  # Quest completed
        return False

    def reset(self):
        """Reset quest progress (for daily quests)"""
        self.progress = 0
        self.completed = False

    def to_dict(self):
        """Convert to dictionary for saving"""
        return {
            'id': self.id,
            'progress': self.progress,
            'completed': self.completed
        }

    def from_dict(self, data):
        """Load from dictionary"""
        self.progress = data.get('progress', 0)
        self.completed = data.get('completed', False)

    def get_display_dict(self):
        """Get quest info for UI display"""
        return {
            'name': self.name,
            'description': self.description,
            'progress': self.progress,
            'goal': self.goal,
            'completed': self.completed,
            'xp_reward': self.xp_reward,
            'currency_reward': self.currency_reward,
            'is_irl': self.is_irl
        }


class QuestManager:
    """Manages all quests and IRL streak system"""

    # Predefined quests
    QUEST_TEMPLATES = {
        # In-game quests
        'bench_beginner': {
            'name': 'Bench Press Beginner',
            'description': 'Use the bench press 3 times',
            'type': 'use_equipment',
            'target_equipment': 'Bench Press',
            'goal': 3,
            'xp_reward': 50,
            'currency_reward': 25
        },
        'squat_starter': {
            'name': 'Squat Starter',
            'description': 'Use the squat rack 3 times',
            'type': 'use_equipment',
            'target_equipment': 'Squat Rack',
            'goal': 3,
            'xp_reward': 50,
            'currency_reward': 25
        },
        'cardio_king': {
            'name': 'Cardio King',
            'description': 'Use the treadmill 5 times',
            'type': 'use_equipment',
            'target_equipment': 'Treadmill',
            'goal': 5,
            'xp_reward': 75,
            'currency_reward': 30
        },
        'dumbbell_dedication': {
            'name': 'Dumbbell Dedication',
            'description': 'Use dumbbells 5 times',
            'type': 'use_equipment',
            'target_equipment': 'Dumbbells',
            'goal': 5,
            'xp_reward': 60,
            'currency_reward': 25
        },
        'gym_tour': {
            'name': 'Gym Tour',
            'description': 'Visit all equipment types',
            'type': 'visit_all',
            'goal': 4,  # 4 equipment types
            'xp_reward': 100,
            'currency_reward': 50
        },
        'level_5': {
            'name': 'Rising Star',
            'description': 'Reach level 5',
            'type': 'level_up',
            'goal': 5,
            'xp_reward': 0,  # Level up is its own reward
            'currency_reward': 100
        },
        'strength_10': {
            'name': 'Getting Strong',
            'description': 'Reach 10 Strength',
            'type': 'stat_goal',
            'target_stat': 'strength',
            'goal': 10,
            'xp_reward': 150,
            'currency_reward': 75
        }
    }

    # IRL Quest templates (daily)
    IRL_QUEST_TEMPLATES = {
        'pushups_50': {
            'name': '50 Push-ups',
            'description': 'Do 50 push-ups today (real life)',
            'type': 'irl',
            'goal': 1,
            'xp_reward': 100,
            'currency_reward': 50
        },
        'run_2k': {
            'name': '2km Run',
            'description': 'Run at least 2km today',
            'type': 'irl',
            'goal': 1,
            'xp_reward': 150,
            'currency_reward': 75
        },
        'gym_visit': {
            'name': 'Gym Visit',
            'description': 'Go to the gym today',
            'type': 'irl',
            'goal': 1,
            'xp_reward': 200,
            'currency_reward': 100
        },
        'no_junk': {
            'name': 'Clean Eating',
            'description': 'No junk food today',
            'type': 'irl',
            'goal': 1,
            'xp_reward': 75,
            'currency_reward': 40
        },
        'water_8': {
            'name': 'Hydration Hero',
            'description': 'Drink 8 glasses of water today',
            'type': 'irl',
            'goal': 1,
            'xp_reward': 50,
            'currency_reward': 25
        },
        'early_wake': {
            'name': 'Early Bird',
            'description': 'Wake up before 7 AM',
            'type': 'irl',
            'goal': 1,
            'xp_reward': 75,
            'currency_reward': 35
        }
    }

    def __init__(self):
        self.active_quests = []
        self.completed_quest_ids = set()
        self.irl_quests = []

        # Streak tracking
        self.current_streak = 0
        self.best_streak = 0
        self.last_irl_date = None

        # Equipment usage tracking (for visit_all quest)
        self.visited_equipment = set()

        # Initialize quests
        self._init_quests()

    def _init_quests(self):
        """Initialize starting quests"""
        # Add first few quests
        self._add_quest_from_template('bench_beginner')
        self._add_quest_from_template('gym_tour')

        # Add daily IRL quests
        self._refresh_irl_quests()

    def _add_quest_from_template(self, template_id):
        """Create quest from template"""
        if template_id in self.completed_quest_ids:
            return None

        template = self.QUEST_TEMPLATES.get(template_id)
        if not template:
            return None

        quest = Quest(
            quest_id=template_id,
            name=template['name'],
            description=template['description'],
            quest_type=template['type'],
            goal=template['goal'],
            xp_reward=template['xp_reward'],
            currency_reward=template['currency_reward']
        )
        self.active_quests.append(quest)
        return quest

    def _refresh_irl_quests(self):
        """Refresh daily IRL quests"""
        self.irl_quests = []

        # Add 3 random IRL quests for the day
        import random
        irl_ids = list(self.IRL_QUEST_TEMPLATES.keys())
        selected = random.sample(irl_ids, min(3, len(irl_ids)))

        for template_id in selected:
            template = self.IRL_QUEST_TEMPLATES[template_id]
            quest = Quest(
                quest_id=template_id,
                name=template['name'],
                description=template['description'],
                quest_type='irl',
                goal=template['goal'],
                xp_reward=template['xp_reward'],
                currency_reward=template['currency_reward']
            )
            self.irl_quests.append(quest)

    def get_active_quest(self):
        """Get the current active quest for display"""
        for quest in self.active_quests:
            if not quest.completed:
                return quest.get_display_dict()
        return None

    def get_all_active_quests(self):
        """Get all active quests"""
        return [q.get_display_dict() for q in self.active_quests if not q.completed]

    def get_irl_quests(self):
        """Get all IRL quests"""
        return [q.get_display_dict() for q in self.irl_quests]

    def on_equipment_use(self, equipment_name):
        """Called when player uses equipment"""
        self.visited_equipment.add(equipment_name)

        for quest in self.active_quests:
            if quest.completed:
                continue

            # Check equipment use quests
            template = self.QUEST_TEMPLATES.get(quest.id, {})
            if (quest.type == 'use_equipment' and
                template.get('target_equipment') == equipment_name):
                if quest.update_progress():
                    return quest  # Return completed quest

            # Check visit_all quest
            if quest.type == 'visit_all':
                quest.progress = len(self.visited_equipment)
                if quest.progress >= quest.goal:
                    quest.completed = True
                    return quest

        return None

    def on_level_up(self, new_level):
        """Called when player levels up"""
        for quest in self.active_quests:
            if quest.type == 'level_up' and not quest.completed:
                if new_level >= quest.goal:
                    quest.completed = True
                    return quest
        return None

    def on_stat_change(self, stat_name, new_value):
        """Called when a stat changes"""
        for quest in self.active_quests:
            if quest.type == 'stat_goal' and not quest.completed:
                template = self.QUEST_TEMPLATES.get(quest.id, {})
                if template.get('target_stat') == stat_name:
                    quest.progress = new_value
                    if new_value >= quest.goal:
                        quest.completed = True
                        return quest
        return None

    def complete_irl_quest(self, quest_index):
        """Mark an IRL quest as complete"""
        if 0 <= quest_index < len(self.irl_quests):
            quest = self.irl_quests[quest_index]
            if not quest.completed:
                quest.completed = True
                self._update_streak()
                return quest
        return None

    def _update_streak(self):
        """Update IRL streak"""
        today = date.today()

        if self.last_irl_date is None:
            self.current_streak = 1
        elif self.last_irl_date == today:
            pass  # Already counted today
        elif (today - self.last_irl_date).days == 1:
            self.current_streak += 1
        else:
            self.current_streak = 1  # Streak broken

        self.last_irl_date = today
        self.best_streak = max(self.best_streak, self.current_streak)

    def get_streak_bonus(self):
        """Get XP/currency multiplier based on streak"""
        if self.current_streak >= 30:
            return 2.0
        elif self.current_streak >= 14:
            return 1.75
        elif self.current_streak >= 7:
            return 1.5
        elif self.current_streak >= 3:
            return 1.25
        return 1.0

    def claim_quest_rewards(self, quest, player):
        """Apply quest rewards to player"""
        multiplier = self.get_streak_bonus() if quest.is_irl else 1.0

        xp = int(quest.xp_reward * multiplier)
        currency = int(quest.currency_reward * multiplier)

        player.add_xp(xp)
        player.add_currency(currency)

        # Mark as completed
        if not quest.is_irl:
            self.completed_quest_ids.add(quest.id)
            self.active_quests.remove(quest)
            self._unlock_next_quest()

        return xp, currency

    def _unlock_next_quest(self):
        """Unlock next quest based on progression"""
        # Simple unlock chain
        if len(self.completed_quest_ids) == 1:
            self._add_quest_from_template('squat_starter')
        elif len(self.completed_quest_ids) == 2:
            self._add_quest_from_template('cardio_king')
        elif len(self.completed_quest_ids) == 3:
            self._add_quest_from_template('dumbbell_dedication')
        elif len(self.completed_quest_ids) == 4:
            self._add_quest_from_template('level_5')
        elif len(self.completed_quest_ids) == 5:
            self._add_quest_from_template('strength_10')

    def to_dict(self):
        """Convert to dictionary for saving"""
        return {
            'active_quests': [q.to_dict() for q in self.active_quests],
            'completed_ids': list(self.completed_quest_ids),
            'irl_quests': [q.to_dict() for q in self.irl_quests],
            'current_streak': self.current_streak,
            'best_streak': self.best_streak,
            'last_irl_date': self.last_irl_date.isoformat() if self.last_irl_date else None,
            'visited_equipment': list(self.visited_equipment)
        }

    def from_dict(self, data):
        """Load from dictionary"""
        self.completed_quest_ids = set(data.get('completed_ids', []))
        self.current_streak = data.get('current_streak', 0)
        self.best_streak = data.get('best_streak', 0)
        self.visited_equipment = set(data.get('visited_equipment', []))

        last_date = data.get('last_irl_date')
        if last_date:
            self.last_irl_date = date.fromisoformat(last_date)

        # Restore active quests
        self.active_quests = []
        for q_data in data.get('active_quests', []):
            quest = self._add_quest_from_template(q_data['id'])
            if quest:
                quest.from_dict(q_data)

        # Check if we need to refresh IRL quests (new day)
        today = date.today()
        if self.last_irl_date != today:
            self._refresh_irl_quests()
        else:
            # Restore IRL quest progress
            self.irl_quests = []
            for q_data in data.get('irl_quests', []):
                template = self.IRL_QUEST_TEMPLATES.get(q_data['id'])
                if template:
                    quest = Quest(
                        quest_id=q_data['id'],
                        name=template['name'],
                        description=template['description'],
                        quest_type='irl',
                        goal=template['goal'],
                        xp_reward=template['xp_reward'],
                        currency_reward=template['currency_reward']
                    )
                    quest.from_dict(q_data)
                    self.irl_quests.append(quest)
