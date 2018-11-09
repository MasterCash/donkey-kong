from framework import GameObject, Clock, SpriteSheet, Keys, Text
from inputManager import InputManager
from spriteManager import SpriteManager
from barrelSpawner import BarrelSpawner
import random
import pygame

roll_standard_barrel = ['get_barrel', 'holding_standard', 'roll_barrel']

class DonkeyKong(GameObject):
    """ Controls animations for Donkey Kong """
    def __init__(self):
        super().__init__()

        self._spawner = BarrelSpawner()
        self._isAI = False

        self._sheet = SpriteSheet('donkey_kong')
        self._sprites = {
            'standing': self._sheet.sprite(0, 8, 80, 64),
            'get_barrel': self._sheet.sprite(96, 8, 87, 64),
            'roll_barrel': self._sheet.sprite(294, 8, 86, 64),
            'angry1': self._sheet.sprite(396, 8, 92, 64),
            'angry2': self._sheet.sprite(504, 8, 92, 64),
            'holding_standard': self._sheet.sprite(970, 8, 80, 64),
            'holding_blue': self._sheet.sprite(1066, 8, 80, 64),
            'holding_explosive': self._sheet.sprite(970, 74, 79, 64),
            'holding_other': self._sheet.sprite(1066, 74, 79, 64)
        }
        self._spriteManager = SpriteManager(self._sprites)
        self._spriteManager.useSprites(['standing'], 10)

        self.__barrelStack = self._sheet.sprite(0, 85, 40, 64)
        self.x = 45
        self.y = 120
        self.ticks = -90

        self._barrelAnimateSpeed = 20

        # Variables related to spawning barrels
        self._isRollingBarrel = False
        self._rollBarrelType = 0
        self._barrelSpawnTimer = 0
        self._countdownTimer = Text('0')
        self._barrelMinTimer = 30
        self._barrelMaxTimer = 120
        self._barrelTimerDecrementer = 5
        self._barrelSpawningSpeedUp = 400
        self._barrelSpeedupTicks = 0

        InputManager.subscribe(
            [Keys.Num_1, Keys.Num_2, Keys.Num_3, Keys.Num_4],
            self._keyPress
        )

    def update(self):
        self._spriteManager.animate()
        self.ticks = self.ticks + 1
        self._barrelSpeedupTicks += 1
        if self._barrelSpawnTimer != 0:
            self._barrelSpawnTimer = self._barrelSpawnTimer - 1

        self.updateAI()
        self.updatePlayer()

        if self.ticks > 90 and self.ticks < 190:
            # Occasionally scream
            self._spriteManager.useSprites(['angry1', 'angry2'], 10)
            if self.ticks == 189:
                self.ticks = -90
                self._spriteManager.useSprites(['standing'], 10)


    def updateAI(self):
        if not self._isAI:
            return
        print("<<<<<<<Donkey Kong>>>>>>>")
        print("spawn timer:" + str(self._barrelSpawnTimer))
        print("speedup time:" + str(self._barrelSpawningSpeedUp))
        print("min timer:" + str(self._barrelMinTimer))
        print("max timer:" + str(self._barrelMaxTimer))
        print("animate speed:" + str(self._barrelAnimateSpeed))
        print("speedup tick:" + str(self._barrelSpeedupTicks))
        print("timer dec:" + str(self._barrelTimerDecrementer))
        if self._barrelSpawnTimer == 0:
            self._rollBarrelType = random.randint(1, 4)
            self._isRollingBarrel = True
            self.ticks = 0
            animation = ['get_barrel', 'standing', 'roll_barrel']
            if self._rollBarrelType == 1:
                animation[1] = 'holding_standard'
            if self._rollBarrelType == 2:
                animation[1] = 'holding_blue'
            if self._rollBarrelType == 3:
                animation[1] = 'holding_explosive'
            if self._rollBarrelType == 4:
                animation[1] = 'holding_other'
            self._spriteManager.useSprites(animation, self._barrelAnimateSpeed)
            self._barrelSpawnTimer = self._barrelAnimateSpeed * 3 + self._barrelAnimateSpeed + 2
        if self._isRollingBarrel:
            # Wait until 40 ticks happen to roll the barrel
            if self.ticks == self._barrelAnimateSpeed * 2 :
                self._barrelSpawnTimer = 0
                self._spawnBarrel()
            elif self.ticks == int(self._barrelAnimateSpeed * 3 + self._barrelAnimateSpeed):
                # Stop rolling animation
                self._isRollingBarrel = False
                self._spriteManager.useSprites(['standing'])
                self.ticks = -1
        if self._barrelSpeedupTicks >= self._barrelSpawningSpeedUp:
            self._barrelSpeedupTicks = 0
            if self._barrelMinTimer - self._barrelTimerDecrementer > 0:
                self._barrelMaxTimer -= self._barrelTimerDecrementer
                self._barrelMinTimer -= self._barrelTimerDecrementer
                if self._barrelAnimateSpeed > self._barrelMinTimer + 10:
                    self._barrelAnimateSpeed /= 2
                    self._barrelAnimateSpeed = int(self._barrelAnimateSpeed)
            elif self._barrelMinTimer > 0:
                self._barrelMaxTimer -= self._barrelMinTimer
                self._barrelMinTimer = 0
            else:
                if self._barrelMaxTimer - self._barrelTimerDecrementer > 0:
                    self._barrelMaxTimer -= self._barrelTimerDecrementer
                elif self._barrelMaxTimer > 0:
                    self._barrelMaxTimer = 0

    def updatePlayer(self):
         if self._isRollingBarrel:
            # Wait until 40 ticks happen to roll the barrel
            if self.ticks == 40 :
                self._spawnBarrel()
            elif self.ticks == 50:
                # Stop rolling animation
                self._isRollingBarrel = False
                self._spriteManager.useSprites(['standing'])
                self.ticks = 0

    def _keyPress(self, key):
        """ Handle Donkey Kong key press """
        if self._isRollingBarrel or self._barrelSpawnTimer != 0:
            return

        self._isRollingBarrel = True
        self.ticks = 0

        animation = ['get_barrel', 'standing', 'roll_barrel']

        if key == Keys.Num_1:
            self._rollBarrelType = 1
            animation[1] = 'holding_standard'
        elif key == Keys.Num_2:
            self._rollBarrelType = 2
            animation[1] = 'holding_blue'
        elif key == Keys.Num_3:
            self._rollBarrelType = 3
            animation[1] = 'holding_explosive'
        elif key == Keys.Num_4:
            self._rollBarrelType = 4
            animation[1] = 'holding_other'

        self._spriteManager.useSprites(animation, 20)

    def _spawnBarrel(self):
        """ Spawns the correct barrel """
        if self._barrelSpawnTimer != 0:
            return

        self._barrelSpawnTimer = random.randint(self._barrelMinTimer, self._barrelMaxTimer) # New random barrel spawn timer
        if self._barrelSpawnTimer == 0:
            self._barrelSpawnTimer += 1
        self._spawner.spawnBarrel(self._rollBarrelType)


    def getSprite(self):
        return self._spriteManager.currentSprite()

    def drawExtra(self, screen):
        """ Draw the barrell stack """
        screen.draw(self.__barrelStack, 0, 120)

        # Display timer if counting down
        if self._barrelSpawnTimer != 0 and not self._isAI:
            self._countdownTimer.setText('%1.1f' % (self._barrelSpawnTimer / Clock.fps))
            screen.draw(self._countdownTimer, 2, 93)

    @staticmethod
    def getAI(diff = 1):
        dk = DonkeyKong()
        if diff <= 0:
            diff = 1
        dk.setAI(diff)
        return dk


    def setAI(self, diff):
        self._barrelMinTimer = 350
        self._barrelMaxTimer = 400
        self._isAI = True
        self._barrelTimerDecrementer *= diff
        self._barrelSpawningSpeedUp -= (diff - 1) * 10
        if self._barrelSpawningSpeedUp < 0:
            self._barrelSpawningSpeedUp = 0
        InputManager.unsubscribe(
            [Keys.Num_1, Keys.Num_2, Keys.Num_3, Keys.Num_4],
            self._keyPress
        )
