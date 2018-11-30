"""
This is the file that should be ran when wanting to launch the game
"""

import os
import game as Game
from mario import Mario
from luigi import Luigi
from barrel import Barrel
from princess import Princess
from levelManager import LevelManager
from donkeyKong import DonkeyKong
from flamingOilContainer import FlamingOilContainer
import menu


def play(window, result):

    game = Game.GameManager(window)
    for player in result.players:
        if player.__name__ == "Mario":
            game.addPlayer(Mario())
        if player.__name__ == "Luigi":
            game.addPlayer(Luigi())
        
    game.addObject(Princess())
    if result.UseAI:
        game.addObject(DonkeyKong().getAI(result.Difficulty))
    else:
        game.addObject(DonkeyKong())
    game.addCollectible(FlamingOilContainer())
    game.addLevelManager(LevelManager())
    game.play()

menu.show(play)

