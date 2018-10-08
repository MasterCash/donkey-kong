import pygame 
import json
from utils import Singleton
from game import GameLevelManager 


@Singleton
class LevelManager(GameLevelManager): 
    def __init__(self): 
        GameLevelManager.__init__(self)
        self.__currentLevel = 0

        # Read levels from the levels file
        with open('assets/levels.json', 'r') as f:
            self._levels = json.load(f)

        print(self._levels)

    def drawLevel(self, screen): 
        """ Draws all of the sprites for the level design """
        screen.fill((0, 0, 0)) # Background color

    def advanceLevel(self): 
        """ Moves to the next level """
        self.__currentLevel = self.__currentLevel + 1 

    @property 
    def currentLevel(self): 
        """ Returns the current level """
        return self.__currentLevel

    