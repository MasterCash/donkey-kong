"""
The barrel spawner is responsible for
interfacing between the Donkey Kong player/sprite
and the Game Manager in order to add the correct type
of barrel to the game
"""
from barrel import Barrel, BarrelType
from game import GameManager

class BarrelSpawner:
    def __init__(self):
        self.__game = GameManager() # GameManager is a singleton so this works

    # Spawns a barrel based on the type given by Donkey Kong.
    def spawnBarrel(self, barrelType):
        """ Spawns a new barrel """
        if barrelType == 1:
            self.__game.addEnemy(Barrel(BarrelType.NORMAL))
        elif barrelType == 2:
            self.__game.addEnemy(Barrel(BarrelType.FIRE))
        elif barrelType == 3:
            self.__game.addEnemy(Barrel(BarrelType.EXPLOSIVE))
        elif barrelType == 4:
            self.__game.addEnemy(Barrel(BarrelType.GOO))



