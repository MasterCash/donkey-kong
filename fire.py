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
    LADDER_TOP = 1,
    LADDER_BOTTOM = 2


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

        self.lastXs = []

        scale = 0.9
        #list spite states
        self._sheet = SpriteSheet('fireball')
        self._sprites = {
            'red_left1' : self._sheet.sprite(0, 2, 26, 30).scale(scale),
            'red_left2' : self._sheet.sprite(46, 0, 30, 32).scale(scale),
            'red_right1' : self._sheet.sprite(94, 2, 26, 30).scale(scale),
            'red_right2' : self._sheet.sprite(140, 0, 30, 32).scale(scale),
        }

        self.spriteManager = SpriteManager(self._sprites)

        self.spriteManager.useSprites([
            'red_right1'
        ], 10)

        self.ticks = 0
        self.ticksSinceLastRoll = 0


    def update(self):
        """ Method used for updating state of a sprite/object """
        try:
            self.__checkForBeingStuck()

            if self._isAtLadder != True and self.state not in (FireState.LADDER_UP, FireState.LADDER_DOWN):
                self.y = self.y + (self._speed * 2) * Clock.timeDelta # Gravity

            self.ticksSinceLastRoll = self.ticksSinceLastRoll + 1

            if self._isAtLadder and self.state not in (FireState.LADDER_UP, FireState.LADDER_DOWN) and self.ticksSinceLastRoll > 120:
                # Decide to go up or down
                self.ticksSinceLastRoll = 0
                if random.randint(1, 100) >= 10:
                    if self.subState == FireSubState.LADDER_BOTTOM:
                        self.state = FireState.LADDER_UP
                        print("up")
                    elif self.substate == FireSubState.LADDER_UP:
                        self.state = FireState.LADDER_DOWN
                        print("Down")

            self._isAtLadder = False
            self.subState = FireSubState.NONE

            if self.ticks > 0:
                self.ticks = self.ticks - 1
                self.subState = FireSubState.NONE

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

        except:
            pass

    def collision(self, collisionType, direction, obj):
        """ Mario collided with something """
        try:
            if collisionType == CollisionTypes.Ladder:
                if self.state != FireState.LADDER_UP and self.state != FireState.LADDER_DOWN and self.subState == FireSubState.NONE:
                    self._isAtLadder = True
                    #self.centerX = obj.centerX
                    if obj.isTopOfLadder:
                        self.subState = FireSubState.LADDER_TOP
                    else:
                        self.subState = FireSubState.LADDER_BOTTOM

            elif collisionType == CollisionTypes.Platform:
                if self._isAtLadder == False:
                    self._isOnGround = True
                    if not obj.isTopOfLadder:
                        self.bottom = obj.top + 1

            elif collisionType == CollisionTypes.Immovable:
                if self.state not in (FireState.LADDER_UP, FireState.LADDER_DOWN) or self.ticks > 0:
                    return

                self.ticks = 60

                if self.state == FireState.LADDER_UP and obj.isTopOfLadder:
                    self.state = FireState.MOVELEFT

                elif self.state == FireState.LADDER_DOWN and obj.isTopOfLadder:
                    self.state = FireState.MOVERIGHT

                if not obj.isTopOfLadder:
                    self.bottom = obj.top

            elif collisionType == CollisionTypes.Wall:
                if obj.isLeftWall:
                    self.left = obj.right
                    self.state = FireState.MOVERIGHT
                else:
                    self.right = obj.left
                    self.state = FireState.MOVELEFT
        except:
            pass

    def getSprite(self):
        """ Returns the current sprite for the game object """
        return self.spriteManager.animate()


    def __checkForBeingStuck(self):
        self.lastXs.append(self.x)

        if len(self.lastXs) == 60:
            needsSaved = True

            toFind = self.lastXs[0]
            for x in self.lastXs:
                if x != toFind:
                    needsSaved = False

            self.lastXs = []

            if needsSaved and self.state not in (FireState.LADDER_UP, FireState.LADDER_DOWN):
                if self.state == FireState.MOVELEFT:
                    self.x = self.x - 20
                else:
                    self.x = self.x + 20
                print(str(self.state))
