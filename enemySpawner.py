"""
The enemy spawner is responsible for
interfacing between the Donkey Kong player/sprite
and the Game Manager in order to add the correct type
of barrel to the game. As well as the barrels generating a fire sprite
"""
import barrel
from fire import Fire, FireType
from game import GameManager

class EnemySpawner:
    def __init__(self):
        self.__game = GameManager() # GameManager is a singleton so this works

    # Spawns a barrel based on the type given by Donkey Kong.
    def spawnBarrel(self, barrelType):
        """ Spawns a new barrel """
        if barrelType == 1:
            self.__game.addEnemy(barrel.Barrel(barrel.BarrelType.NORMAL))
        elif barrelType == 2:
            self.__game.addEnemy(barrel.Barrel(barrel.BarrelType.FIRE))
        elif barrelType == 3:
            self.__game.addEnemy(barrel.Barrel(barrel.BarrelType.EXPLOSIVE))
        elif barrelType == 4:
            self.__game.addEnemy(barrel.Barrel(barrel.BarrelType.GOO))

    def spawnFire(self, fireType):
        """ Spawns a fire sprite to TERMINATE Mario once and for all """
        print("before")
        if fireType == 0:
            self.__game.addEnemy(Fire(FireType.FIRE))
            
        


