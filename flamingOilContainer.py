from framework import GameCollectible, SpriteSheet
from spriteManager import SpriteManager



class FlamingOilContainer(GameCollectible):
    def __init__(self):
        super().__init__()

        self._sheet = SpriteSheet('flaming_oil_can')
        self._sprites = {
            'flame1': self._sheet.sprite(0, 0, 32, 64),
            'flame2': self._sheet.sprite(48, 0, 32, 64),
            'flame3': self._sheet.sprite(96, 0, 32, 64),
            'flame4': self._sheet.sprite(144, 0, 32, 64),
            'no_flame': self._sheet.sprite(192, 0, 32, 64)
        }

        self._burning = ['flame1', 'flame2']
        self._extraBurn = ['flame3', 'flame4', 'flame3', 'flame4']

        self._spriteManager = SpriteManager(self._sprites)
        self._spriteManager.useSprites(self._burning)

        self.x = 10
        self.y = 504


    def onCollect(self, collectedBy, name):
        print("Collected by {0}".format(name))

    def getSprite(self):
        """ Gets the latest sprite """
        self._spriteManager.animate()
        return self._spriteManager.currentSprite()