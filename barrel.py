"""
Class for barrels  
"""
import pygame 
from utils import Spritesheet
from framework import GameObject
from spriteManager import SpriteManager


class Barrel(GameObject): 
    def __init__(self):
        GameObject.__init__(self)
        self.spriteManager = SpriteManager()

        self._sheet = Spritesheet('barrel')
        
        self._sprites = { 
            'fall_1': self._sheet.sprite(290, 0, 40, 20), 
            'fall_2': self._sheet.sprite(340, 0, 40, 20)
        }#I current do not have access to any image software so I can't measure anything
         #so sprites are technically pretty close to accurate but idk 
        self.spriteManager.addSprites(self._sprites)
        # self._currentSprite = self._sprites['run_left2']
        self.spriteManager.useSprites([
            'fall_1',
            'fall_2'
        ])
        self.x = 200
        self.y = 100
        

    def update(self): 
        """ Method used for updating state of a sprite/object """
        #self.x = self.x - 1
        self.y = self.y + 1
        self.spriteManager.animate(10)
        
    def collisionCheck(self, otherObj): 
        """ Checks for collision with another spirte """
        return False

    def getPositionAndSize(self): 
        """ Returns the current position, and dimension of the thing """
        return (self.x, self.y, 0, 0) 

    def getSprite(self): 
        """ Returns the current sprite for the game object """
        return self.spriteManager.currentSprite()
    