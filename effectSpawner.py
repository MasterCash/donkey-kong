
from game import GameManager
from framework import GameObject, SpriteSheet, Clock, GameSprite
from spriteManager import SpriteManager
from utils import Singleton
from random import randint

@Singleton
class EffectSpawner:
    def __init__(self):
        self.__game = GameManager()

    def spawnExplosion(self, x, y):
        self.__game.addEnemy(Explosion(x, y))
    def spawnGoo(self, x, y, platform):
        self.__game.addEnemy(Goo(x, y, platform))


class Explosion(GameObject):
    def __init__(self, x, y):
        GameObject.__init__(self)
        self._sheet = SpriteSheet('explosion')
        self.tick = 0
        self.x = x
        self.y = y

        self._sprites = {
            'explosion_1': self._sheet.sprite(0,0,0,0),
            'explosion_2': self._sheet.sprite(0,0,0,0)
        }

        self.spriteManager = SpriteManager(self._sprites)

    def update(self):
        self.tick += 1
        if self.tick >= 200:
            self.kill()


class Goo(GameObject):
    def __init__(self, x, y, platform):
        GameObject.__init__(self)
        self._sheet = SpriteSheet('goo')
        self.tick = 0
        self.x = platform.x
        self.y = platform.y
        print(platform.x)
        print(platform.y)
        self._sprites = {
            'Goo_1': self._sheet.sprite(0,1,32,16)
        }
        self.spriteManager = SpriteManager(self._sprites)
        self.spriteManager.useSprites(['Goo_1'])
    def update(self):
        self.spriteManager.animate()
        self.tick += 1
        if self.tick >= randint(200, 400):
            self.kill()

    def getSprite(self):
        return self.spriteManager.currentSprite()