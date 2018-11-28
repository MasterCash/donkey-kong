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

# Fire states
class FireState(Enum):
    MOVE = 0
    ON_LADDER = 1

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
        self._speed = 2
        self._sheet = SpriteSheet('fireball')
        self.type = fireType

        #list spite states
        self._sprites = {
            'red_left1' : self._sheet.sprite(0, 2, 26, 30),
            'red_left2' : self._sheet.sprite(46, 0, 30, 32),
            'red_right1' : self._sheet.sprite(94, 2, 26, 30),
            'red_right2' : self._sheet.sprite(140, 0, 30, 32),
        }

        self.spriteManager = SpriteManager(self._sprites)

        self.spriteManager.useSprites([
            'red_right1'
        ], 10)
        
        # fire starting position, state, and dir
        self.x = 60
        self.y = 550
        self.state = FireState.MOVE
        self.dir = FireDir.RIGHT
        self.tick = 100
        self.isLadder = False
        self.randDir = random.randint(0,1)

    def update(self):
        if not self.isLadder:
            self.y += 1
        else:
            self.tick -= 1
        if self.state == FireState.MOVE:
            # TODO: make fire sprites move randomly
            # random direction after after exit the ladder
            if self.isLadder:
                if self.tick <= 0:
                    self.randDir = random.randint(0,1)
                    self.tick = 20
                print(self.randDir)
                if self.randDir == 0:
                    self.dir = FireDir.RIGHT
                elif self.randDir == 1:
                    self.dir = FireDir.LEFT
                
                self.state = FireState.ON_LADDER
            else:
                if self.dir == FireDir.RIGHT:
                    self.x += self._speed
                    self.setSprites()
                else:
                    self.x -= self._speed
                    self.setSprites()

        elif self.state == FireState.ON_LADDER:
            if not self.isLadder:
                self.state = FireState.MOVE
            else:
                self.y -= 1
                self.getSprite()

        self.spriteManager.animate()

    def setSprites(self):
        if self.state == FireState.MOVE:
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
        elif self.state == FireState.ON_LADDER:
            if self.dir == FireDir.LEFT:
                self.spriteManager.useSprites([
                    'red_left1',
                ], 8)

            elif self.dir == FireDir.RIGHT:
                self.spriteManager.useSprites([
                    'red_right1',
                ], 8)
    def collision(self, collisionType, direction, obj):
        # If we are hitting a platform.
        if collisionType == CollisionTypes.Platform:
            if not self.isLadder:
                self.bottom = obj.top + 1
                
        # IF we are on a ladder, set ladder flag.
        elif collisionType == CollisionTypes.Ladder:
            self.isLadder = True

        # If we hit a Immovable, Boundary for Platforms and Ladders.
        elif collisionType == CollisionTypes.Immovable:
            self.state = FireState.MOVE
            self.isLadder = False
            if not obj.isTopOfLadder:
                self.bottom = obj.top

        # collision with wall
        elif collisionType == CollisionTypes.Wall:
            print("hit wall")
            self.state = FireState.MOVE
            if obj.isLeftWall:
                self.dir = FireDir.RIGHT
            else:
                self.dir = FireDir.LEFT
    def getSprite(self):
        """ Returns the current sprite for the game object """
        return self.spriteManager.currentSprite()
