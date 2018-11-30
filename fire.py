"""
Class for fire
"""
from framework import GameObject, SpriteSheet, Clock
from spriteManager import SpriteManager
from enum import Enum
from collisionDetector import CollisionTypes
import random
import mario
from luigi import Luigi
from mario import Mario

# Different type of fires
class FireType(Enum):
    FIRE = 0
    def __str__(self):
        return self.value

# Fire directions
class FireDir(Enum):
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3

class Fire(GameObject):
    def __init__(self, fireType):
        GameObject.__init__(self)
        # speed of fire sprite
        self.level = 0
        self._speed = 160
        self._sheet = SpriteSheet('fireball')
        self.type = fireType

        #list spite states
        self._sprites = {
            'red_left1' : self._sheet.sprite(0, 2, 26, 30).scale(.5),
            'red_left2' : self._sheet.sprite(46, 0, 30, 32).scale(.5),
            'red_right1' : self._sheet.sprite(94, 2, 26, 30).scale(.5),
            'red_right2' : self._sheet.sprite(140, 0, 30, 32).scale(.5),
        }

        self.spriteManager = SpriteManager(self._sprites)

        self.spriteManager.useSprites([
            'red_right1'
        ], 10)
        
        # fire starting position, state, and dir
        self.x = 60
        self.y = 550
        self.mov_angle = random.randint(0,100) / 50
        if random.randint(0,100) > 50:
            self.dir = FireDir.RIGHT
        else:
            self.dir = FireDir.LEFT

    def update(self):
        # fire move left or right
        self.y -= (self._speed * self.mov_angle) * Clock.timeDelta
        if self.dir == FireDir.RIGHT:
            self.x += self._speed * Clock.timeDelta
            self.setSprites()
        elif self.dir == FireDir.LEFT:
            self.x -= self._speed * Clock.timeDelta
            self.setSprites()
        elif self.dir == FireDir.UP:
            self.y -= self._speed * Clock.timeDelta
            self.getSprite()
        elif self.dir == FireDir.DOWN:
            self.y += self._speed * Clock.timeDelta
            self.getSprite()
        self.spriteManager.animate()

    def collision(self, collisionType, direction, obj):
        if collisionType == CollisionTypes.Wall:
            if obj.isLeftWall:
                self.dir = FireDir.RIGHT
            else:
                self.dir = FireDir.LEFT

            if abs(self.x) < obj.x:
                self.right = obj.left - 3
            else:
                self.left = obj.right + 3
    
    def setSprites(self):
        if self.dir == FireDir.RIGHT:
            self.spriteManager.useSprites([
                'red_right1',
                'red_right2'
                ], 8)
        elif self.dir == FireDir.LEFT:
            self.spriteManager.useSprites([
                'red_left1',
                'red_left2'
                ], 8)

    def getSprite(self):
        """ Returns the current sprite for the game object """
        return self.spriteManager.currentSprite()