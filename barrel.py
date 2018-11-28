"""
Class for barrels
"""
import math
import random
from framework import GameObject, SpriteSheet, Clock
from spriteManager import SpriteManager
from enum import Enum
from collisionDetector import CollisionTypes, CollisionDirection
from effectSpawner import EffectSpawner

# Enum to represent the type of code.
class BarrelType(Enum):
    NORMAL = 'normal'
    FIRE = 'fire'
    EXPLOSIVE = 'exp'
    GOO = 'goo'
    def __str__(self):
        return self.value

# Possible Barrel States.
class BarrelState(Enum):
    MOVE = 0
    FALL = 1
    DEAD = 2

# Possible Directions the Barrel is moving.
class BarrelDir(Enum):
    RIGHT = 0
    LEFT = 1

class Barrel(GameObject):
    def __init__(self, barrelType):
        GameObject.__init__(self)
        self._speed = 80
        self._sheet = SpriteSheet('barrel')
        # Type of barrel being handled. Given when Created.
        self.type = barrelType
        # Counter for Barrel actions.
        self.tick = 0
        self.dirChanged = False
        self.hitWall = False
        self._lastPlatform = {}
        self._ladderIgnore = 0
        # List of all sprite states for animations.
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
            'goo_roll1': self._sheet.sprite(112, 66, 24, 20),
            'goo_roll2': self._sheet.sprite(160, 66, 24, 20),
            'goo_roll3': self._sheet.sprite(208, 66, 24, 20),
            'goo_fall1': self._sheet.sprite(290, 66, 40, 20),
            'goo_fall2': self._sheet.sprite(340, 66, 40, 20),
            'goo_fall3': self._sheet.sprite(290, 66, 40, 20).flip(),
            'goo_fall4': self._sheet.sprite(340, 66, 40, 20).flip()
        }

        # This Barrel's Sprite Manager.
        self.spriteManager = SpriteManager(self._sprites)

        # Initial Spawning Position.
        self.x = 127
        self.y = 160

        # Initalizing the state of the Barrel.
        self.state = BarrelState.MOVE
        self.dir = BarrelDir.RIGHT
        # Hasn't Collided with a Ladder yet.
        self.isFalling = False
        # Set the starting tick Value.
        self.setTick()
        self.setSprites()

    # Update, Called each game loop update.
    def update(self):
        """ Method used for updating state of a sprite/object """
        # Decrement the tick count.
        self.tick -= 1
        # Handle any behaviors of the barrel for each type.
        self.handleBehavior()
        # Animate
        self.spriteManager.animate()

        self.move()

    # Set the sprites for each action.
    def setSprites(self):
        if self.state == BarrelState.MOVE:
            if self.dir == BarrelDir.RIGHT:
                self.spriteManager.useSprites([
                    str(self.type) + '_roll1',
                    str(self.type) + '_roll2',
                    str(self.type) + '_roll3'
                    ], self.animationSpeed())
            elif self.dir == BarrelDir.LEFT:
                self.spriteManager.useSprites([
                    str(self.type) + '_roll3',
                    str(self.type) + '_roll2',
                    str(self.type) + '_roll1'
                    ],self.animationSpeed())
        elif self.state == BarrelState.FALL:
            if self.dir == BarrelDir.LEFT:
                self.spriteManager.useSprites([
                    str(self.type) + '_fall1',
                    str(self.type) + '_fall2',
                ], self.animationSpeed())

            elif self.dir == BarrelDir.RIGHT:
                self.spriteManager.useSprites([
                    str(self.type) + '_fall3',
                    str(self.type) + '_fall4',
                ], self.animationSpeed())

    def animationSpeed(self):
        if self.state == BarrelState.MOVE:
            return math.ceil((2000/((1/3*self._speed)**2))+2)
        else:
            return 5


    def move(self):
        if self.state == BarrelState.MOVE:
            # If the barrel is on a ladder.
            if self.isFalling:
                if self._ladderIgnore > 0 and not self.hitWall:
                    self.isFalling = False
                    self._ladderIgnore -= 1
                elif random.randint(1, 100) > 60 and not self.hitWall:
                    self._ladderIgnore = 6
                    self.isFalling = False
                elif self.hitWall:
                    if self.dir == BarrelDir.LEFT:
                        self.dir = BarrelDir.RIGHT
                    elif self.dir == BarrelDir.RIGHT:
                        self.dir = BarrelDir.LEFT
                    self.state = BarrelState.FALL
                else:
                    # Change the direction so that when we stop falling,
                    # we are heading the oposite direction as before.
                    # it is falling down the ladder.
                    if self.dir == BarrelDir.LEFT:
                        self.dir = BarrelDir.RIGHT
                    elif self.dir == BarrelDir.RIGHT:
                        self.dir = BarrelDir.LEFT
                    # Adjust the position to make it so the sprite actually looks like
                    self.x -= 8
                    # Change the state to falling because we are on a ladder.
                    self.hitWall = False
                    self.state = BarrelState.FALL
            # Barrel is moving right, move right.
            self.x += (self._speed if self.dir == BarrelDir.RIGHT else -self._speed) * Clock.timeDelta

        # If Falling.
        elif self.state == BarrelState.FALL:
            # If not on a ladder anymore.
            if not self.isFalling:
                # Change state to move.
                self.state = BarrelState.MOVE
                # self.setSprites()
        self.y += (self._speed * 1.5) * Clock.timeDelta
        if self.dirChanged:
            self.setSprites()
            self.dirChanged = False

    # Collision Handling.
    def collision(self, collisionType, direction, obj):
        """ Checks for collision with another spirte """
        # If we are hitting a platform.
        if collisionType == CollisionTypes.Platform:
            self._lastPlatform = obj
            # And we are not on a ladder, stop falling.
            if not self.isFalling:
                self.bottom = obj.top + 1
        # IF we are on the top of a ladder, set ladder flag.
        elif collisionType == CollisionTypes.Ladder and direction == CollisionDirection.Bottom:
            # IF we were not on a ladder before
            if not self.isFalling:
                # flag the falling and the direction changed flags
                self.dirChanged = True
                self.isFalling = True
        # If we hit a Immovable, Boundary for Platforms.
        elif collisionType == CollisionTypes.Immovable and direction == CollisionDirection.Bottom:
            # Stop moving down.
            self.bottom = obj.top + 1
            # No Longer on a Ladder. update flags if they are not updated.
            if self.isFalling:
                self.dirChanged = True
                self.isFalling = False
        elif collisionType == CollisionTypes.Wall:
            self._ladderIgnore = 0
            self.hitWall = True
            if self.x <= obj.x:
                self.right = obj.left - 1
            else:
                self.left = obj.right + 1
            if not self.isFalling:
                self.dirChanged = True
                self.isFalling = True

    # Handles behavior for each barrel type.
    def handleBehavior(self):
        # If the barrel is of a type that has a timed affect.
        if self.type == BarrelType.EXPLOSIVE or self.type == BarrelType.GOO:
            # check to see if the time is up.
            if self.tick <= 0:
                # Do the action for this barrel.
                self.action()
        return

    # Gets the current sprite of this barrel.
    def getSprite(self):
        """ Returns the current sprite for the game object """
        return self.spriteManager.currentSprite()

    # Sets the tick value to be what it should be based on the barrel type.
    def setTick(self):
        # TODO: make randomize ranges.
        if self.type == BarrelType.EXPLOSIVE:
            self.tick = random.randint(300, 1900)
        elif self.type == BarrelType.GOO:
            self.tick = random.randint(300, 1900)
        else:
            self.tick = 0

    # Action to do for each type of barrel.
    def action(self):
        if self.isFalling:
            self.tick = 1
            return
        # TODO: add explosion AOE
        if self.type == BarrelType.EXPLOSIVE:
            EffectSpawner().spawnExplosion(self)
            self.state = BarrelState.DEAD
            self.kill()
        # TODO: change current platform state.
        elif self.type == BarrelType.GOO:
            EffectSpawner().spawnGoo(self._lastPlatform)
            self.state = BarrelState.DEAD
            self.kill()

    # Called if item collected. Used to despawn barrels when they reach the end.
    def collectedItem(self, collectible, collectionType):
        self.state = BarrelState.DEAD
        self.kill()
        # If fire type, spawn a fire ball.
        if self.type == BarrelType.FIRE:
            print("Fire Spawned")