import pygame

from game import GameObject
from utils import Spritesheet

class BarrelType(enum):
    NORMAL = 0
    EXPLOSIVE = 1
    OIL = 2


@GameObject
class Barrel:
    def __init__(self, bType, x, y):
        GameObject.__init__(self
        self._type = bType
        self._speed = 10
        self.x = x
        self.y = y
        self._sheet = Spritesheet('barrel')

        self._sprites = {
            BarrelType.NORMAL: self._sheet.sprite_at((0,20,24,32))
        }


        self._currentSprite = self._sprites[bType]


    def update(self): 
        """ Method used for updating state of a sprite/object """
        self.x = self.x 
        self.y = self.y
        
    def collisionCheck(self, otherObj): 
        """ Checks for collision with another spirte """
        return False

    def getPositionAndSize(self): 
        """ Returns the current position, and dimension of the thing """
        return (self.x, self.y, 0, 0) 

    def getSprite(self): 
        """ Returns the current sprite for the game object """
        return self._currentSprite

