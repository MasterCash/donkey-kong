"""
Class to control mario
"""
from spriteManager import SpriteManager
from framework import GameObject, Clock, SpriteSheet, Keys, Sound
from inputManager import InputManager
from enum import Enum
from collisionDetector import CollisionTypes, CollisionDirection

class PlayerState(Enum):
    IDLE = 0
    LADDER_DOWN = 1
    MOVELEFT = 2
    MOVERIGHT = 3
    JUMP = 4
    DEAD = 5
    ERROR = 6
    LADDER_IDLE = 7
    LADDER_UP = 8
    DEAD1 = 9
    ON_GROUND = 10


movement = 100.0
jump_height = 30
jump_speed = 300 # Actually 100


class Mario(GameObject):
    def __init__(self):
        super().__init__()

        self._sheet = SpriteSheet('mario')
        self.lives = 900
        self._jumpCount = 15
        self._isJumping = False

        self._sprites = {
            'stand_left': self._sheet.sprite(0, 20, 24, 32),
            'stand_right': self._sheet.sprite(0, 20, 24, 32).flip(),
            'run_left1': self._sheet.sprite(45, 20, 31, 32),
            'run_left2': self._sheet.sprite(94, 21, 30, 32),
            'run_right1': self._sheet.sprite(45, 20, 31, 32).flip(),
            'run_right2': self._sheet.sprite(94, 21, 30, 32).flip(),
            'ladder_up1': self._sheet.sprite(142, 20, 28, 32),
            'ladder_up2': self._sheet.sprite(142, 20, 28, 32).flip(),
            'death1': self._sheet.sprite(716, 20, 32, 32),
            'death2': self._sheet.sprite(764, 20, 32, 32),
            'death3': self._sheet.sprite(764, 20, 32, 32).rotate(90),
            'death4': self._sheet.sprite(764, 20, 32, 32).flip(),
            'death5': self._sheet.sprite(764, 20, 32, 32).rotate(-90),
            'death6': self._sheet.sprite(812, 20, 32, 32)
        }

        self.spriteManager = SpriteManager(self._sprites)

        self.spriteManager.useSprites([
            'stand_right'
        ], 10)

        self.x = 60
        self.y = 550
        self.state = PlayerState.IDLE
        self._isAtLadder = False
        self._isOnGround = False
        self.ticks = 0

        InputManager.subscribe(
            [Keys.LEFT, Keys.RIGHT, Keys.DOWN, Keys.UP, Keys.SPACE],
            self._marioKeyPress
        )

        self._walkingSound = Sound('walking')

    def update(self):
        """ Method used for updating state of a sprite/object """
        if self._isAtLadder != True and not self._isJumping:
            self.y = self.y + (movement * 2) * Clock.timeDelta # Gravity

        self._isAtLadder = False

        if self._isJumping:
            if self._jumpCount >= -15:
                neg = 1
                if self._jumpCount < 0:
                    neg = -1
                self.y = self.y - (self._jumpCount ** 2) * 0.025 * neg
                self._jumpCount = self._jumpCount - 1
            else:
                self._isJumping = False
                self._jumpCount = 15
            self._isOnGround = False

        if self.state == PlayerState.MOVELEFT:
            self.x -= movement * Clock.timeDelta
            self.state = PlayerState.IDLE
            self.spriteManager.useSprites([
                'run_left1',
                'stand_left',
                'run_left2'
            ], 8)
            self._walkingSound.play()
        elif self.state == PlayerState.MOVERIGHT:
            self.x += movement * Clock.timeDelta
            self.state = PlayerState.IDLE
            self.spriteManager.useSprites([
                'run_right1',
                'stand_right',
                'run_right2'
            ], 8)
            self._walkingSound.play()
        elif self.state == PlayerState.LADDER_DOWN:
            self.y += movement * Clock.timeDelta
            self.state = PlayerState.LADDER_IDLE
            self.spriteManager.useSprites([
                'ladder_up1',
                'ladder_up2'
            ], 10)
        elif self.state == PlayerState.LADDER_UP:
            self.y -= movement * Clock.timeDelta
            self.state = PlayerState.LADDER_IDLE
            self.spriteManager.useSprites([
                'ladder_up1',
                'ladder_up2'
            ], 10)
        elif self.state == PlayerState.LADDER_IDLE:
            self.spriteManager.useSprites([
                'ladder_up1'
            ], 10)
        else:
            self.state = PlayerState.IDLE
            if 'stand_left' in self.spriteManager.currentAnimation:
                self.spriteManager.useSprites(['stand_left'], 10)
            else:
                self.spriteManager.useSprites(['stand_right'], 10)

            self._walkingSound.stop()

    def collision(self, collisionType, direction, obj):
        """ Mario collided with something """
        if collisionType == CollisionTypes.Enemy:
            print("You killed Mario!!!!!")
            self.die()

        elif collisionType == CollisionTypes.Ladder:
            self._isAtLadder = True

        elif collisionType == CollisionTypes.Platform:
            if self._isAtLadder == False and not self._isJumping:
                self._isOnGround = True
                self.bottom = obj.top + 1

        elif collisionType == CollisionTypes.Immovable:
            self.state = PlayerState.IDLE
            if not obj.isTopOfLadder:
                self.bottom = obj.top

    def _marioKeyPress(self, key):
        def __str__(self):
            return "MarioKeyPress"

        if (key == Keys.LEFT or key == Keys.A) and self.state not in (PlayerState.LADDER_IDLE, PlayerState.LADDER_DOWN, PlayerState.LADDER_UP):
            self.state = PlayerState.MOVELEFT
        elif (key == Keys.RIGHT or key == Keys.D) and self.state != PlayerState.LADDER_IDLE:
            self.state = PlayerState.MOVERIGHT
        elif key == Keys.DOWN or key == Keys.S:
            if self._isAtLadder:
                self.state = PlayerState.LADDER_DOWN
        elif key == Keys.UP:
            if self._isAtLadder and not self._isJumping:
                self.state = PlayerState.LADDER_UP
        elif key is Keys.SPACE and self.state not in (PlayerState.LADDER_IDLE, PlayerState.LADDER_DOWN, PlayerState.LADDER_UP):
            if not self._isJumping and self._isOnGround:
                self._isJumping = True
        #else:
            #print(key)

    def getSprite(self):
        """ Returns the current sprite for the game object """
        if self.isDying:
            self.ticks = self.ticks + 1
            if self.ticks == 30:
                self.spriteManager.useSprites(['death2', 'death3', 'death4', 'death5'], 10)
            elif self.ticks == 100:
                self.spriteManager.useSprites(['death6'])
            elif self.ticks == 150:
                self.x = 60
                self.y = 540
                self.state = PlayerState.IDLE
                self.isDying = False
                #self.remove()

        return self.spriteManager.animate()

    @GameObject.deathMethod
    def die(self):
        """ Play the death animation """
        self.lives = self.lives - 1
        self.state = PlayerState.DEAD
        self.spriteManager.useSprites(['death1'], 10)
        self.ticks = 0
        self._walkingSound.stop()
