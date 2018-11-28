import json
from utils import Singleton
from game import GameLevelManager
#from utils import SpriteSheet
from framework import GameSprite, SpriteGroup, SpriteSheet

class Platform(GameSprite):
    def __init__(self, x, y, sprite):
        super().__init__()
        self.x = x
        self.y = y
        self.image = sprite
        self._next = None
        self._previous = None

    @property
    def nextPlatform(self):
        return self._next

    @nextPlatform.setter
    def nextPlatform(self, next):
        self._next = next

    @property
    def previousPlatform(self):
        return self._previous

    @previousPlatform.setter
    def previousPlatform(self, prev):
        self._previous = prev


class Ladder(GameSprite):
    def __init__(self, x, y, sprite):
        super().__init__()
        self.x = x
        self.y = y
        self.image = sprite

class InvisiblePlatform(GameSprite):
    def __init__(self, x, y, sprite, isTopOfLadder = False):
        super().__init__()
        self.x = x
        self.y = y
        self.image = sprite
        self.isTopOfLadder = isTopOfLadder

class InvisibleLadder(GameSprite):
    def __init__(self, x, y, sprite):
        super().__init__()
        self.x = x
        self.y = y
        self.image = sprite

class InvisibleWall(GameSprite):
    def __init__(self, x, y, sprite, isLeft):
        super().__init__()
        self.x = x
        self.y = y
        self.image = sprite
        self.isLeftWall = isLeft

@Singleton
class LevelManager(GameLevelManager):
    def __init__(self):
        GameLevelManager.__init__(self)
        self.__currentLevel = 0

        self.platforms = SpriteGroup()
        self.ladders = SpriteGroup()
        self.immovables = SpriteGroup()
        self.walls = SpriteGroup()

        self._sheet = SpriteSheet('level')
        self._platform = self._sheet.sprite(0, 1, 32, 16)
        self._ladder = self._sheet.sprite(33, 1, 16, 8)
        self._invisibleLadder = self._sheet.invisibleSprite(16, 8)
        self._invisiblePlatform = self._sheet.invisibleSprite(16, 8)
        self._invisibleSideWall = self._sheet.invisibleSprite(1, 600)
        self._invisibleEdgeWall = self._sheet.invisibleSprite(1,8) # Currently not used

        self._winningHeight = 0

        self._windowHeight = 0
        self._windowWidth = 0

    def setWindowInformation(self, width, height):
        """ Set information about the window """
        self._windowWidth = width
        self._windowHeight = height
        self.buildLevel()

    def update(self):
        """ Update method just like other game objects """
        self.platforms.update()

    def buildLevel(self):
        height = self._windowHeight
        width = self._windowWidth

        w = self._platform.width
        h = self._platform.height

        def drawLadder(x, y):
            targetY = y - (int((4*h)/8) * 8) + h-2
            lastY = 0
            self.immovables.add(InvisiblePlatform(x, y-1, self._invisiblePlatform)) # Invisible platform on bottom of ladder
            for y1 in range(y-9, targetY, -8):
                self.ladders.add(Ladder(x, y1, self._ladder))
                lastY = y1

            # Invisible ladder hitbox on top of the platform
            targetY = lastY - (int((2.5*h)/8) * 8) + h-2
            for y1 in range(lastY - 6, targetY, -8):
                self.ladders.add(InvisibleLadder(x, y1, self._invisibleLadder))

            self.immovables.add(InvisiblePlatform(x, targetY - 32, self._invisiblePlatform, True)) # Invisible platform on top of the ladder

        def drawLtoRPlatform(y):
            platformsThisTime = []

            lastX = 0
            for x in range(w, width + w, w):
                platformsThisTime.append(Platform(x, y, self._platform))
                y = y - 1
                lastX = x

            self.immovables.add(InvisiblePlatform(x-w, y+1, self._invisiblePlatform))

            for i in range(0, len(platformsThisTime)):
                if i > 0:
                    platformsThisTime[i].previousPlatform = platformsThisTime[i-1]
                if i < (len(platformsThisTime) - 1):
                    platformsThisTime[i].nextPlatform = platformsThisTime[i+1]

                self.platforms.add(platformsThisTime[i])

            # Add ladder to next platform
            x = lastX - 2*w
            drawLadder(x, y+3)
            return y

        def drawRtoLPlatform(y):
            platformsThisTime = []

            lastX = 0
            for x in range(width - (2 * w), 0 - w, w * -1):
                platformsThisTime.append(Platform(x, y, self._platform))
                y = y - 1
                lastX = x

            self.immovables.add(InvisiblePlatform(0, y+1, self._invisiblePlatform))

            for i in range(0, len(platformsThisTime)):
                if i > 0:
                    platformsThisTime[i].previousPlatform = platformsThisTime[i-1]
                if i < (len(platformsThisTime) - 1):
                    platformsThisTime[i].nextPlatform = platformsThisTime[i+1]

                self.platforms.add(platformsThisTime[i])

            # Add ladder to next platform
            x = lastX + 1.5*w
            drawLadder(x, y+3)
            return y

        # Flat section of first platform
        y = height - 2 * h
        lastX = 0
        for x in range(0, int(width/2), w):
            self.platforms.add(Platform(x, y, self._platform))
            lastX = x

        # Angled section of first platform
        for x in range(lastX + w, width, w):
            self.platforms.add(Platform(x, y, self._platform))
            y = y - 1
            lastX = x

        self.immovables.add(InvisiblePlatform(lastX, y+1, self._invisiblePlatform))

        drawLadder(lastX - (2*w), y) # Ladder from first platform

        # Draw other platforms
        y = y - (4 * h) + 2
        y = drawRtoLPlatform(y)

        y = y - (4* h) + 2
        y = drawLtoRPlatform(y)

        y = y - (4 * h) + 2
        y = drawRtoLPlatform(y)

        y = y - (4 * h) + 2
        y = drawLtoRPlatform(y)

        # Draw Left Inv. Wall
        self.walls.add(InvisibleWall(0, 0, self._invisibleSideWall, True))
        # Draw Right Inv. Wall
        self.walls.add(InvisibleWall(544, 0, self._invisibleSideWall, False))

        # Top platform
        y = y - (4 * h) + 2
        for x in range(0 - w, width - w, w):
            self.platforms.add(Platform(x, y, self._platform))

        # Princess Peach Platform
        y = y - (4 * h)
        for x in range(int(width/2.5), int(width/2.5) + (3 * w), w):
            self.platforms.add(Platform(x, y, self._platform))
            lastX = x

        self._winningHeight = y # Player must be at the peach platform to win

        # Ladder to Princess Peach
        x = lastX
        drawLadder(x, y + (4 * h) - 2)

        # Next Level ladders
        x = width/4 + w
        drawLadder(x, y + (4 * h) - 2)
        drawLadder(x,  y + h - 2)
        drawLadder(x, y - (2 * h) - 2)
        x = x + w
        drawLadder(x, y + (4 * h) - 2)
        drawLadder(x,  y + h - 2)
        drawLadder(x, y - (2 * h) - 2)

    def draw(self, screen):
        """ Draw method just like other game sprites """
        screen.fill((1, 1, 1)) # Background color
        self.platforms.draw(screen)
        self.ladders.draw(screen)
        self.immovables.draw(screen)
        self.walls.draw(screen)

    def advanceLevel(self):
        """ Moves to the next level """
        self.__currentLevel = self.__currentLevel + 1

    def isLevelCompleted(self, player):
        """ Checks if the level has been completed """
        if player.bottom <= self._winningHeight:
            return True

        return False

    @property
    def currentLevel(self):
        """ Returns the current level """
        return self.__currentLevel


