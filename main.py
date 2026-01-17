#!/usr/bin/env python3
"""
Goggins Fitness Game
====================
A 2D motivational fitness game with top-down GTA 1/2 style view.

Features:
- Top-down gym exploration with tile-based movement
- David Goggins-inspired motivational trainer
- In-game quests with equipment mini-games
- Real-life (IRL) fitness quests with streak bonuses
- Supplement shop and inventory system
- Save/load game progress
- Multiple muscle level sprites based on progression

Controls:
- WASD/Arrow Keys: Move
- SHIFT: Sprint
- E: Interact with equipment
- I: Open inventory
- TAB: View IRL quests
- ESC: Pause menu

Run with: python main.py
Requires: pygame (pip install pygame)
"""

import sys
import asyncio

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import pygame
        return True
    except ImportError:
        print("Error: pygame is not installed!")
        print("Install it with: pip install pygame")
        return False

async def main():
    """Main entry point"""
    if not check_dependencies():
        sys.exit(1)

    from game import Game

    print("Starting Goggins Fitness Game...")
    print("Stay hard!")

    game = Game()
    await game.run()

if __name__ == "__main__":
    asyncio.run(main())
