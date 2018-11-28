"""
Class for fire
"""
from framework import GameObject, SpriteSheet
from spriteManager import SpriteManager
from enum import Enum
from collisionDetector import CollisionTypes

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

        self.isLadder = False

    def update(self):
        if self.state == FireState.MOVE:

            # TODO: make fire sprites move randomly
            if self.isLadder:
                if self.dir == FireDir.LEFT:
                    self.dir = FireDir.RIGHT
                elif self.dir == FireDir.RIGHT:
                    self.dir = FireDir.LEFT
                
                self.state = FireState.ON_LADDER
            else:
                if self.dir == FireDir.RIGHT:
                    self.x += self._speed
                    self.setSprites()
                else:
                    self.x -= self._speed
                    self.setSprites()
                self.y += 1
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
            # And we are not on a ladder, stop falling.
            if not self.isLadder:
                self.bottom = obj.top + 1
        # IF we are on a ladder, set ladder flag.
        elif collisionType == CollisionTypes.Ladder:
            self.isLadder = True
        # If we hit a Immovable, Boundary for Platforms and Ladders.
        elif collisionType == CollisionTypes.Immovable:
            # Stop moving down.
            self.bottom = obj.top + 1
            # No Longer on a Ladder.
            self.isLadder = False
    def getSprite(self):
        """ Returns the current sprite for the game object """
        return self.spriteManager.currentSprite()
