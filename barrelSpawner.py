"""
The barrel spawner is responsible for
interfacing between the Donkey Kong player/sprite
and the Game Manager in order to add the correct type
of barrel to the game
"""
from barrel import Barrel
from game import GameManager

class BarrelSpawner:
    def __init__(self):
        self.__game = GameManager() # GameManager is a singleton so this works


    def spawnStandardBarrel(self):
        """ Spawns a new barrel """
        self.__game.addEnemy(Barrel())
