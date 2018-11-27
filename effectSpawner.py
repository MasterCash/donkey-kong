
from game import GameManager
from framework import GameObject, SpriteSheet, Clock, GameSprite
from spriteManager import SpriteManager
from utils import Singleton
from random import randint

@Singleton
class EffectSpawner:
    def __init__(self):
        self.__game = GameManager()

    def spawnExplosion(self, barrel):
        rand = randint(10, 30)
        self.__game.addEnemy(Explosion(barrel, rand))
    def spawnGoo(self, platform):
        rand = randint(200, 500)
        self.__game.addEnemy(Goo(platform.nextPlatform, rand))
        self.__game.addEnemy(Goo(platform, rand))
        self.__game.addEnemy(Goo(platform.previousPlatform, rand))


class Explosion(GameObject):
    def __init__(self, barrel, rand):
        GameObject.__init__(self)
        self._sheet = SpriteSheet('explosion')
        self.tick = 0
        self.x = barrel.x
        self._barrel = barrel
        self.y = barrel.y
        self._sprites = {
            'explosion_0': self._sheet.sprite(0,0,3,3),
            'explosion_1': self._sheet.sprite(4,0,10,10),
            'explosion_2': self._sheet.sprite(15,0,15,15),
            'explosion_3': self._sheet.sprite(31,0,20,20),
            'explosion_4': self._sheet.sprite(52,0,25,25),
            'explosion_5': self._sheet.sprite(78,0,35,35),
            'explosion_6': self._sheet.sprite(114,0,45,45),
            'explosion_7': self._sheet.sprite(160,0,75,50),
            'explosion_8': self._sheet.sprite(0,0,0,0)
        }

        self.len = (len(self._sprites))

        self.spriteManager = SpriteManager(self._sprites)
        sprites = []
        for i in range(0,self.len):
            sprites.append('explosion_'+str(i))
        self.spriteManager.useSprites(sprites, rand)
    def update(self):
        self.centerX = self._barrel.centerX
        self.bottom = self._barrel.bottom
        self.y -= 3
        self.spriteManager.animate()
        if self.getSprite() == self._sprites['explosion_'+ str(self.len - 1)]:
            self.kill()
    def getSprite(self):
        return self.spriteManager.currentSprite()


class Goo(GameObject):
    def __init__(self, platform, rand):
        GameObject.__init__(self)
        self._sheet = SpriteSheet('goo')
        self.tick = 0
        self.x = platform.x
        self.y = platform.y
        self.rand = rand
        self._sprites = {
            'Goo_1': self._sheet.sprite(0,1,32,16)
        }
        self.spriteManager = SpriteManager(self._sprites)
        self.spriteManager.useSprites(['Goo_1'])
    def update(self):
        self.spriteManager.animate()
        self.tick += 1
        if self.tick >= self.rand:
            self.kill()

    def getSprite(self):
        return self.spriteManager.currentSprite()