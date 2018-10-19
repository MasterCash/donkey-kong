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

game = Game.GameManager()
game.addPlayer(Mario())
game.addObject(Princess())
game.addObject(DonkeyKong())
game.addEnemy(Barrel())
game.addLevelManager(LevelManager())
game.play()

