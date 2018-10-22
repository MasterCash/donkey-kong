"""
Class for barrels
"""
#from utils import SpriteSheet
from framework import GameObject, SpriteSheet
from spriteManager import SpriteManager
from enum import Enum
from collisionDetector import CollisionTypes

class BarrelType(Enum):
    NORMAL = 'normal'
    FIRE = 'fire'
    EXPLOSIVE = 'exp'
    OIL = 'oil'
    def __str__(self):
        return self.value

class BarrelState(Enum):
    MOVE = 0
    FALL = 1
class BarrelDir(Enum):
    RIGHT = 0
    LEFT = 1

class Barrel(GameObject): 
    def __init__(self, barrelType):
        GameObject.__init__(self)
        self._speed = 10
        self._sheet = SpriteSheet('barrel')
        self.type = barrelType

        self._sprites = {
            'normal_roll1': self._sheet.sprite(112, 0, 24, 20),
            'normal_roll2': self._sheet.sprite(160, 0, 24, 20),
            'normal_roll3': self._sheet.sprite(208, 0, 24, 20),
            'normal_fall1': self._sheet.sprite(290, 0, 40, 20), 
            'normal_fall2': self._sheet.sprite(340, 0, 40, 20),
            'normal_fall3': self._sheet.sprite(290, 0, 40, 20).flip(), 
            'normal_fall4': self._sheet.sprite(340, 0, 40, 20).flip(),
            'fire_roll1': self._sheet.sprite(112, 22, 24, 20),
            'fire_roll2': self._sheet.sprite(160, 22, 24, 20),
            'fire_roll3': self._sheet.sprite(208, 22, 24, 20),
            'fire_fall1': self._sheet.sprite(290, 22, 40, 20), 
            'fire_fall2': self._sheet.sprite(340, 22, 40, 20),
            'fire_fall3': self._sheet.sprite(290, 22, 40, 20).flip(), 
            'fire_fall4': self._sheet.sprite(340, 22, 40, 20).flip(),
            'exp_roll1': self._sheet.sprite(112, 44, 24, 20),
            'exp_roll2': self._sheet.sprite(160, 44, 24, 20),
            'exp_roll3': self._sheet.sprite(208, 44, 24, 20),
            'exp_fall1': self._sheet.sprite(290, 44, 40, 20), 
            'exp_fall2': self._sheet.sprite(340, 44, 40, 20),
            'exp_fall3': self._sheet.sprite(290, 44, 40, 20).flip(), 
            'exp_fall4': self._sheet.sprite(340, 44, 40, 20).flip(),
            'oil_roll1': self._sheet.sprite(112, 66, 24, 20),
            'oil_roll2': self._sheet.sprite(160, 66, 24, 20),
            'oil_roll3': self._sheet.sprite(208, 66, 24, 20),
            'oil_fall1': self._sheet.sprite(290, 66, 40, 20), 
            'oil_fall2': self._sheet.sprite(340, 66, 40, 20),
            'oil_fall3': self._sheet.sprite(290, 66, 40, 20).flip(),
            'oil_fall4': self._sheet.sprite(340, 66, 40, 20).flip()
        }
        self.spriteManager = SpriteManager(self._sprites)

        self.spriteManager.useSprites([
            str(self.type) + '_fall1',
            str(self.type) + '_fall2'
        ], 10)

        self.x = 320
        self.y = 130
        
        self.state = BarrelState.FALL
        self.dir = BarrelDir.RIGHT
        self.isLadder = False

    def update(self):
        """ Method used for updating state of a sprite/object """
        self.handleBehavior()
        if self.state == BarrelState.MOVE:
            if self.isLadder:
                if self.dir == BarrelDir.LEFT:
                    self.x -= self._sprites[str(self.type) + '_fall1'].height
                    self.dir = BarrelDir.RIGHT
                elif self.dir == BarrelDir.RIGHT:
                    self.x += 5
                    self.dir = BarrelDir.LEFT
                    
                
                self.state = BarrelState.FALL
            elif self.dir == BarrelDir.RIGHT:
                self.x += 1
                self.setSprites()
            else: 
                self.x -= 1
                self.setSprites()
            self.y += 1
        elif self.state == BarrelState.FALL:
            if not self.isLadder:
                self.state = BarrelState.MOVE
            else:
                self.y += 1
                self.setSprites()
        self.spriteManager.animate()
    def setSprites(self):
        if self.state == BarrelState.MOVE:
            if self.dir == BarrelDir.RIGHT:
                self.spriteManager.useSprites([
                    str(self.type) + '_roll1',
                    str(self.type) + '_roll2',
                    str(self.type) + '_roll3'
                    ], 10)
            elif self.dir == BarrelDir.LEFT:
                self.spriteManager.useSprites([
                    str(self.type) + '_roll3',
                    str(self.type) + '_roll2',
                    str(self.type) + '_roll1'
                    ], 10)
        elif self.state == BarrelState.FALL:
            if self.dir == BarrelDir.LEFT:
                self.spriteManager.useSprites([
                    str(self.type) + '_fall1',
                    str(self.type) + '_fall2',
                ], 10)

            elif self.dir == BarrelDir.RIGHT:
                self.spriteManager.useSprites([
                    str(self.type) + '_fall3',
                    str(self.type) + '_fall4',
                ], 10)
            

    def collision(self, collisionType, direction, obj):
        """ Checks for collision with another spirte """
        if collisionType == CollisionTypes.Platform:
            if not self.isLadder:
                self.bottom = obj.top + 1
        elif collisionType == CollisionTypes.Ladder:
            self.isLadder = True
        elif collisionType == CollisionTypes.Immovable:
            self.bottom = obj.top + 1
            self.isLadder = False
        # Add detecting hitting the fire barrel

    def getPositionAndSize(self):
        """ Returns the current position, and dimension of the thing """
        return (self.x, self.y, 0, 0)

    def handleBehavior(self):
        return

    def getSprite(self):
        """ Returns the current sprite for the game object """
        return self.spriteManager.currentSprite()
