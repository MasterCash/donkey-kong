import pygame
from framework import SpriteSheet


class SpriteManager:
    """ Used for animating sprites on a thingy """
    def __init__(self):
        return

    #makes the sprites in sheet
    def addSprites(self, sprites):
        self._sprites = sprites
        self._counter = 0 #counts the number of frames between each animation
        return

    #converts the (unordered) dictionary to an ordered array based on animation var
    def useSprites(self, animation):
        self._currentSpriteName = animation[0]
        self._location = 0
        self._currentSprite = self._sprites[self._currentSpriteName]
        self._spriteArray = []

        for x in animation:
            self._spriteArray.append(self._sprites[x])


    def animate(self, counter):
        #Animates every 'counter' frames, use 1 to animate every frame, higher values update less often
        self._counter += 1
        if self._counter == counter:

            #loc = self._spriteArray.index(self._currentSprite)
            #print(self._location)
            #increments to the next frame of movement in current animation
            if self._location == len(self._spriteArray) - 1:
                self._currentSprite = self._spriteArray[0]
                self._location = 0
            else:
                self._currentSprite = self._spriteArray[self._location+1]
                self._location += 1

            self._counter = 0
        else:
            pass
        return

    def currentSprite(self):
        return self._currentSprite