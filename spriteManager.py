from framework import SpriteSheet


class SpriteManager:
    """ Used for animating sprites on a thingy """
    #makes the sprites in sheet
    def __init__(self, sprites):
        self._sprites = sprites
        self.currentAnimation = []
        return
    #converts the dictionary to an ordered array based on animation var
    def useSprites(self, animation, tick = 10):
        if self.currentAnimation == animation:
            return
        self.currentAnimation = animation
        self._currentSpriteName = animation[0]
        self._location = 0
        self._tick = int(tick)
        self._currentSprite = self._sprites[self._currentSpriteName]
        self._spriteArray = []
        self._counter = 0 #counts the number of frames between each animation

        for x in animation:
            self._spriteArray.append(self._sprites[x])
        return

    def animate(self):
        #Animates every 'tick' frames, use 1 to animate every frame, higher values update less often
        self._counter += 1
        if self._counter == self._tick:
            #increments to the next frame of movement in current animation
            if self._location == len(self._spriteArray) - 1:
                self._currentSprite = self._spriteArray[0]
                self._location = 0
            else:
                self._currentSprite = self._spriteArray[self._location+1]
                self._location += 1

            self._counter = 0

        return self._currentSprite

    def currentSprite(self):
        return self._currentSprite