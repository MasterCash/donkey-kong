"""
Class to control mario
"""
import pygame
#from utils import SpriteSheet
from framework import SpriteSheet
#from game import GameObject
from spriteManager import SpriteManager
from framework import GameObject, Clock
from inputManager import InputManager
from enum import Enum
from collisionDetector import CollisionTypes, CollisionDirection

class PlayerState(Enum):
    IDLE = 0
    LADDER = 1
    MOVELEFT = 2
    MOVERIGHT = 3
    JUMP = 4
    DEAD = 5
    ERROR = 6
    LADDER_IDLE = 7


movement = 100.0


class Mario(GameObject):
    def __init__(self):
        super().__init__()
        self.spriteManager = SpriteManager()

        self._sheet = SpriteSheet('mario')

        self._sprites = {
            'stand_left': self._sheet.sprite(0, 20, 24, 32).flip(),
            'run_left1': self._sheet.sprite(46, 20, 30, 32).flip(),
            'run_left2': self._sheet.sprite(94, 22, 30, 30).flip()
        }

        self.spriteManager.addSprites(self._sprites)

        self.spriteManager.useSprites([
            'run_left2',
            'stand_left',
            'run_left1',
            'run_left1'
        ])
        self.x = 300
        self.y = 300
        self.state = PlayerState.IDLE
        self._isAtLadder = False

        InputManager.subscribe(
            [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_SPACE, pygame.K_DOWN],
            self._marioKeyPress
        )

    def update(self):

        """ Method used for updating state of a sprite/object """
        #self.x = self.x - 1
        if self._isAtLadder != True:
            self.y = self.y + 1

        self._isAtLadder = False

        if self.state == PlayerState.MOVELEFT:
            self.x -= movement * Clock.timeDelta
            self.state = PlayerState.IDLE
        elif self.state == PlayerState.MOVERIGHT:
            self.x += movement * Clock.timeDelta
            self.state = PlayerState.IDLE
        elif self.state == PlayerState.LADDER:
            self.y += movement * Clock.timeDelta
            self.state = PlayerState.LADDER_IDLE
        elif self.state == PlayerState.LADDER_IDLE:
            pass
        else:
            self.state = PlayerState.IDLE

        self.spriteManager.animate(10)

    def collision(self, collisionType, direction, obj):
        """ Mario collided with something """
        if collisionType == CollisionTypes.Enemy:
            print("You killed Mario!!!!!")
            self.die()

        elif collisionType == CollisionTypes.Ladder:
            self._isAtLadder = True

        elif collisionType == CollisionTypes.Platform:
            if self._isAtLadder == False:
                self.y = obj.y - self.height + 1


    def _marioKeyPress(self, key):
        def __str__(self):
          return "MarioKeyPress"
        if key == pygame.K_LEFT or key == pygame.K_a:
            self.state = PlayerState.MOVELEFT
        elif key == pygame.K_RIGHT or key == pygame.K_d:
            self.state = PlayerState.MOVERIGHT
        elif key == pygame.K_DOWN or key == pygame.K_s:
            print("key down")
            if self._isAtLadder:
                self.state = PlayerState.LADDER
        elif key is pygame.K_SPACE:
            print("Mario Jumped")
        else:
            print(key)


    def getSprite(self):
        """ Returns the current sprite for the game object """
        return self.spriteManager.currentSprite()
