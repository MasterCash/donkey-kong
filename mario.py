"""
Class to control mario 
"""
import pygame 
from utils import Spritesheet
from game import GameObject
from levelManager import LevelManager


class Mario(GameObject): 
    def __init__(self):
        super().__init__()
        self._sheet = Spritesheet('mario')
        
        self._sprites = { 
            'stand_left': self._sheet.sprite_at((0, 20, 24, 32)),
            'run_left1': self._sheet.sprite_at((46, 20, 30, 32)), 
            'run_left2': self._sheet.sprite_at((94, 22, 30, 30))
        }

        self._currentSprite = self._sprites['run_left2']
        self.x = 100
        self.y = 100

    def update(self): 
        """ Method used for updating state of a sprite/object """
        #self.x = self.x + 1
        self.y = self.y + 1

    def collisionCheck(self, otherObj): 
        """ Checks for collision with another spirte """
        return False

    def getSprite(self): 
        """ Returns the current sprite for the game object """
        return self._currentSprite
    