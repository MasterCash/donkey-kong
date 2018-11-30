"""
Class to control mario
"""
from spriteManager import SpriteManager
from framework import PlayableWithLives, Clock, SpriteSheet, Keys, Sound
from inputManager import InputManager
from enum import Enum
from collisionDetector import CollisionTypes, CollisionDirection

class PlayerState(Enum):
    IDLE = 0
    LADDER_DOWN = 1
    MOVELEFT = 2
    MOVERIGHT = 3
    DEAD = 5
    ERROR = 6
    LADDER_IDLE = 7
    LADDER_UP = 8

class PlayerSubState(Enum):
    NONE = 0
    ON_GROUND = 10
    ON_GOO = 1
    JUMPING = 2

<<<<<<< HEAD
movement = 100.0
jump_height = 16
=======
goo_speed = 50
player_speed = 100.0
jump_height = 15
>>>>>>> master
jump_speed = 300 # Actually 100



class Mario(PlayableWithLives):
    def __init__(self):
        super().__init__()

        self._sheet = SpriteSheet('mario')
<<<<<<< HEAD
        self._jumpCount = jump_height
        self._isJumping = False
=======
        self._speed = player_speed
        self._jumpCount = jump_height
>>>>>>> master

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
            'death6': self._sheet.sprite(812, 20, 32, 32),
            'life': self._sheet.sprite(1629, 31, 14, 16).flip()
        }

        self.spriteManager = SpriteManager(self._sprites)

        self.spriteManager.useSprites([
            'stand_right'
        ], 10)

        self.ticks = 0

        InputManager.subscribe(
            [Keys.LEFT, Keys.RIGHT, Keys.DOWN, Keys.UP, Keys.SPACE, Keys.R],
            self._marioKeyPress
        )

        self._walkingSound = Sound('15_SFX_Walking')

    def update(self):
        """ Method used for updating state of a sprite/object """
        if self._isAtLadder != True and self.subState != PlayerSubState.JUMPING:
            self.y = self.y + (self._speed * 2) * Clock.timeDelta # Gravity

        self._isAtLadder = False

<<<<<<< HEAD
        if self._isJumping:
=======
        if self.subState == PlayerSubState.ON_GOO:
            self._speed = goo_speed
            self.subState = PlayerSubState.NONE
        else:
            self._speed = player_speed

        if self.subState == PlayerSubState.JUMPING:
>>>>>>> master
            if self._jumpCount >= -jump_height:
                neg = 1
                if self._jumpCount < 0:
                    neg = -1
                self.y = self.y - (self._jumpCount ** 2) * 0.025 * neg
                self._jumpCount = self._jumpCount - 1
            else:
<<<<<<< HEAD
                self._isJumping = False
=======
                self.subState = PlayerSubState.NONE
>>>>>>> master
                self._jumpCount = jump_height
            self._isOnGround = False
        else:
            self._jumpCount = jump_height

        if self.state == PlayerState.MOVELEFT:
            self.x -= self._speed * Clock.timeDelta
            self.state = PlayerState.IDLE
            self.spriteManager.useSprites([
                'run_left1',
                'stand_left',
                'run_left2'
            ], 8)
            self._walkingSound.stop()
            self._walkingSound.play()

        elif self.state == PlayerState.MOVERIGHT:
            self.x += self._speed * Clock.timeDelta
            self.state = PlayerState.IDLE
            self.spriteManager.useSprites([
                'run_right1',
                'stand_right',
                'run_right2'
            ], 8)
            self._walkingSound.stop()
            self._walkingSound.play()

        elif self.state == PlayerState.LADDER_DOWN:
            self.y += self._speed * Clock.timeDelta
            self.state = PlayerState.LADDER_IDLE
            self.spriteManager.useSprites([
                'ladder_up1',
                'ladder_up2'
            ], 10)

        elif self.state == PlayerState.LADDER_UP:
            self.y -= self._speed * Clock.timeDelta
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
            if self._isAtLadder == False and self.subState != PlayerSubState.JUMPING:
                self._isOnGround = True
                self.bottom = obj.top + 1

        elif collisionType == CollisionTypes.Immovable:
            self.state = PlayerState.IDLE
            if not obj.isTopOfLadder:
                self.bottom = obj.top

        elif collisionType == CollisionTypes.Wall:
            self.state = PlayerState.IDLE
            if obj.isLeftWall:
                self.left = obj.right
            else:
                self.right = obj.left

    def collectedItem(self, collectible, collectionType):
        """ Mario collecting something """
        if collectible.name == 'Goo':
            self.subState = PlayerSubState.ON_GOO

    def _marioKeyPress(self, key):
        def __str__(self):
            return "MarioKeyPress"

        if key == Keys.R:
            self.die()

        if (key == Keys.LEFT or key == Keys.A) and self.state not in (PlayerState.LADDER_IDLE, PlayerState.LADDER_DOWN, PlayerState.LADDER_UP):
            self.state = PlayerState.MOVELEFT

        elif (key == Keys.RIGHT or key == Keys.D) and self.state != PlayerState.LADDER_IDLE:
            self.state = PlayerState.MOVERIGHT

        elif key == Keys.DOWN or key == Keys.S:
            if self._isAtLadder:
                self.state = PlayerState.LADDER_DOWN

        elif key == Keys.UP:
            if self._isAtLadder and self.subState != PlayerSubState.JUMPING:
                self.state = PlayerState.LADDER_UP

        elif key is Keys.SPACE and self.state not in (PlayerState.LADDER_IDLE, PlayerState.LADDER_DOWN, PlayerState.LADDER_UP):
            if self.subState not in (PlayerSubState.JUMPING, PlayerSubState.ON_GOO) and self._isOnGround:
                self.subState = PlayerSubState.JUMPING

    def getSprite(self):
        """ Returns the current sprite for the game object """
        if self.isDying:
            self.ticks = self.ticks + 1
            if self.ticks == 30:
                self.spriteManager.useSprites(['death2', 'death3', 'death4', 'death5'], 10)
            elif self.ticks == 100:
                self.spriteManager.useSprites(['death6'])
            elif self.ticks == 150:
               self.respawnIfPossible()

        return self.spriteManager.animate()

    def onDeath(self):
        """ Play the death animation """
        self.state = PlayerState.DEAD
        self.spriteManager.useSprites(['death1'], 10)
        self.ticks = 0
        self._walkingSound.stop()

    def drawExtra(self, screen):
        """ Draw the number of lives remaining """
        for i in range(self.lives):
            screen.draw(self._sprites['life'], 10 + (i * 20), 10)

    def onSpawn(self):
        self.state = PlayerState.IDLE
        self.subState = PlayerSubState.NONE
        self._isAtLadder = False
        self._isOnGround = True
        self._jumpCount = jump_height
        self.ticks = 0

