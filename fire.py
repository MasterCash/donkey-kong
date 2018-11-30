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
    FALLING = 1
    AT_LADDER = 2

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
        self._speed = 80
        self._sheet = SpriteSheet('fireball')
        self.type = fireType

        #list spite states
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
        
        # fire starting position, state, and dir
        self.x = 250
        self.y = 300
        self.isFalling = False
        #self.x = 60
        #self.y = 550
        self.top_level = 170
        self.state = FireState.MOVE
        self.dir = FireDir.RIGHT
        self.dir_tick = 100
        self.isLadder = False
        self.randDir = 0
        self.isTop = False
        self.hitWall = False

    def update(self):
        self.dir_tick -= 1
        if self.dir_tick <= 0:
            self.randDir = random.randint(0,1)
            self.dir_tick = 100
        
        # set direction 
        if self.randDir == 0:
            self.dir = FireDir.RIGHT
        else:
            self.dir = FireDir.LEFT

        # if not at ladder, apply gravity
        if not self.isLadder:
            self.y += (self._speed * 1.5) * Clock.timeDelta
            self.state = FireState.MOVE
        else:
            self.state = FireState.AT_LADDER

        # fire move left or right
        if self.state == FireState.MOVE and self.hitWall == False:
            if self.dir == FireDir.RIGHT:
                self.x += self._speed * Clock.timeDelta
                self.setSprites()
            elif self.dir == FireDir.LEFT:
                self.x -= self._speed * Clock.timeDelta
                self.setSprites()
        # go up ladder when see it
        if self.y > 160:
            self.dir = FireDir.UP
        if self.state == FireState.AT_LADDER and self.dir == FireDir.UP:
                self.y -= 1
                self.getSprite()
        print(self.y)
        self.spriteManager.animate()

    def collision(self, collisionType, direction, obj):
        # If we are hitting a platform.
        if collisionType == CollisionTypes.Platform:
            self.state = FireState.MOVE
            self.hitWall = False
            if not self.isLadder:
                self.bottom = obj.top + 1
                
        # IF we are on a ladder, set ladder flag.
        elif collisionType == CollisionTypes.Ladder:
            # won't go up ladder if at top level
            if not self.isTop:
                self.isLadder = True

        # If we hit a Immovable, Boundary for Platforms and Ladders.
        elif collisionType == CollisionTypes.Immovable:
            if not obj.isTopOfLadder:
                self.bottom = obj.top
                self.isLadder = True
                self.isTop = False
            else:
                self.isTop = True
                self.isLadder = False

        # collision with wall
        elif collisionType == CollisionTypes.Wall:
            self.hitWall = True
            self.isLadder = False
            if obj.isLeftWall:
                self.randDir = 0
            else:
                self.randDir = 1

            if abs(self.x) < obj.x:
                self.right = obj.left - 3
            else:
                self.left = obj.right + 3
    
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

    def getSprite(self):
        """ Returns the current sprite for the game object """
        return self.spriteManager.currentSprite()
