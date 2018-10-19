from framework import GameObject, Clock, SpriteSheet, Keys
from inputManager import InputManager
from spriteManager import SpriteManager
from barrelSpawner import BarrelSpawner

roll_standard_barrel = ['get_barrel', 'holding_standard', 'roll_barrel']

class DonkeyKong(GameObject):
    """ Controls animations for Donkey Kong """
    def __init__(self):
        super().__init__()

        self._spawner = BarrelSpawner()

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

        self.isRollingBarrel = False

    def update(self):
        self._spriteManager.animate()

        self.ticks = self.ticks + 1
        if self.ticks > 90 and self.ticks < 190:
            self._spriteManager.useSprites(['angry1', 'angry2'], 10)
            if self.ticks == 189:
                self.ticks = -90
                self._spriteManager.useSprites(['standing'], 10)
                self._spawner.spawnStandardBarrel()


    def getSprite(self):
        return self._spriteManager.currentSprite()

    def drawExtra(self, screen):
        """ Draw the barrell stack """
        screen.draw(self.__barrelStack, 0, 120)