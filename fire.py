"""
Class for fire
"""
from framework import GameObject, SpriteSheet, Clock
from spriteManager import SpriteManager
from enum import Enum
from collisionDetector import CollisionTypes
import random

# Different type of fires
class FireType(Enum):
    FIRE = 0
    def __str__(self):
        return self.value

class FireState(Enum):
    IDLE = 0
    LADDER_DOWN = 1
    MOVELEFT = 2
    MOVERIGHT = 3
    DEAD = 5
    ERROR = 6
    LADDER_IDLE = 7
    LADDER_UP = 8

class FireSubState(Enum):
    NONE = 0
    ON_GROUND = 10
    ON_GOO = 1
    JUMPING = 2


fire_speed = 80.0


class Fire(GameObject):
    def __init__(self, fireType, x, y):
        super().__init__()

        self._speed = fire_speed
        self.x = x
        self.y = y
        self.state = FireState.MOVERIGHT
        self.subState = FireSubState.NONE
        self._isAtLadder = False
        self._isOnGround = True
        self.ticks = 0

        #list spite states
        self._sheet = SpriteSheet('fireball')
        self._sprites = {
            'red_left1' : self._sheet.sprite(0, 2, 26, 30).scale(.9),
            'red_left2' : self._sheet.sprite(46, 0, 30, 32).scale(.9),
            'red_right1' : self._sheet.sprite(94, 2, 26, 30).scale(.9),
            'red_right2' : self._sheet.sprite(140, 0, 30, 32).scale(.9),
        }

        self.spriteManager = SpriteManager(self._sprites)

        self.spriteManager.useSprites([
            'red_right1'
        ], 10)

        self.ticks = 0


    def update(self):
        """ Method used for updating state of a sprite/object """
        if self._isAtLadder != True:
            self.y = self.y + (self._speed * 2) * Clock.timeDelta # Gravity

        self._isAtLadder = False

        if self.state == FireState.MOVELEFT:
            self.x -= self._speed * Clock.timeDelta
            self.spriteManager.useSprites([
                'red_left1',
                'red_left2'
            ], 8)

        elif self.state == FireState.MOVERIGHT:
            self.x += self._speed * Clock.timeDelta
            self.spriteManager.useSprites([
                'red_right1',
                'red_right2'
            ], 8)

        elif self.state == FireState.LADDER_DOWN:
            self.y += self._speed * Clock.timeDelta

        elif self.state == FireState.LADDER_UP:
            self.y -= self._speed * Clock.timeDelta

    def collision(self, collisionType, direction, obj):
        """ Mario collided with something """
        if collisionType == CollisionTypes.Ladder:
            if not obj.isBroken:
                self._isAtLadder = True

        elif collisionType == CollisionTypes.Platform:
            if self._isAtLadder == False and self.subState != FireSubState.JUMPING:
                self._isOnGround = True
                if not obj.isTopOfLadder:
                    self.bottom = obj.top + 1

        elif collisionType == CollisionTypes.Immovable:
            if self.state == FireState.LADDER_UP:
                self.state = FireState.MOVELEFT
            if not obj.isTopOfLadder and not obj.isBroken:
                self.bottom = obj.top

        elif collisionType == CollisionTypes.Wall:
            if obj.isLeftWall:
                self.left = obj.right
                self.state = FireState.MOVERIGHT
            else:
                self.right = obj.left
                self.state = FireState.MOVELEFT

    def getSprite(self):
        """ Returns the current sprite for the game object """
        return self.spriteManager.animate()