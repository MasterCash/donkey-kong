"""
Class to control mario
"""
import pygame
from utils import Spritesheet
#from game import GameObject
from spriteManager import SpriteManager
from framework import GameObject

class Mario(GameObject):
    def __init__(self):
        GameObject.__init__(self)
        self.spriteManager = SpriteManager()

        self._sheet = Spritesheet('mario')

        self._sprites = {
            'stand_left': self._sheet.sprite(0, 20, 24, 32),
            'run_left1': self._sheet.sprite(46, 20, 30, 32),
            'run_left2': self._sheet.sprite(94, 22, 30, 30)
        }

        self.spriteManager.addSprites(self._sprites)

        self.spriteManager.useSprites([
            'run_left2',
            'stand_left',
            'run_left1',
            'run_left1'
        ])
        self.x = 600
        self.y = 400


    def update(self):
        """ Method used for updating state of a sprite/object """
        self.x = self.x - 1
        #self.y = self.y + 1
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
