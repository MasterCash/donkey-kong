"""
This is the file that should be ran when wanting to launch the game
"""

import os
import game as Game
from mario import Mario
from barrel import Barrel
from princess import Princess
from levelManager import LevelManager
from donkeyKong import DonkeyKong
from flamingOilContainer import FlamingOilContainer
import menu


def play(window):
    game = Game.GameManager(window)
    game.addPlayer(Mario())
    game.addObject(Princess())
    game.addObject(DonkeyKong())
    game.addCollectible(FlamingOilContainer())
    game.addLevelManager(LevelManager())
    game.play()

menu.show(play)


