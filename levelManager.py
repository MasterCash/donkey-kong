import json
import random
from utils import Singleton
from game import GameLevelManager
from framework import GameSprite, SpriteGroup, SpriteSheet

def neg(x):
    return -1 * x

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

    def buildLevel2(self):
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

        drawLadder(lastX - (2*w), y+4) # Ladder from first platform

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
        self.ladders.draw(screen)
        self.platforms.draw(screen)
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

    def getSpawnLocations(self):
        """ Returns valid spawn locations for the current level """
        pass

    @property
    def currentLevel(self):
        """ Returns the current level """
        return self.__currentLevel

    def buildLevel(self):
        level = self._generateLevel()

        # i is index in platform list, j is index in block part of level
        i = 0
        for platform in level:
            for block in platform:
                self.platforms.add(block.build(self._platform))
                if block.ladder is not None:
                    self._buildLadder(block, level, i)

            i = i + 1

    def _buildLadder(self, block, levelBuilder, platformIndex):
        """ Builds a ladder at a certain point """
        ladder = block.ladder
        if ladder is None:
            return

        h = self._ladder.height

        y = ladder.y
        x = ladder.x

        if ((platformIndex + 1) >= len(levelBuilder)):
            return

        targetY = -1
        # Find block in next platform with the same x coordinates
        nextPlatform = levelBuilder[platformIndex + 1]
        for otherBlock in nextPlatform:
            if otherBlock.x == block.x:
                targetY = otherBlock.y + self._platform.height
                break

        self.immovables.add(InvisiblePlatform(x, y, self._invisiblePlatform)) # Invisible platform at bottom of the ladder

        if ladder.isCompleteLadder:
            # Full Ladder
            for ladderY in range(y-h, targetY-h, neg(h)):
                self.ladders.add(Ladder(x, ladderY, self._ladder))
        else:
            # Broken Ladder
            pass

        self.ladders.add(InvisibleLadder(x, targetY-2*h, self._invisibleLadder))

        self.immovables.add(InvisiblePlatform(x, targetY - 20, self._invisiblePlatform, True)) # Invisible platform at top of the ladder
    """
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
"""

    def _generateLevel(self):
        """ Construct the actual level """
        height = self._windowHeight
        width = self._windowWidth

        w = self._platform.width
        h = self._platform.height
        level = LevelBuilder()

        # Base platform
        y = height - 2 * h
        base = level.addPlatform(y)
        for x in range(0, width, w):
            if x >= int(width/2):
                block = base.addInclinedBlock(x)
                if (x == width - 2*w):
                    block.addLadder()
            else:
                base.addLevelBlock(x)

        # Next Platform
        y = y - (5 * h) + 3
        platform = level.addPlatform(y)
        platform.addLevelBlock(width - 2*w)
        for x in range(width - 3*w, neg(w), neg(w)):
            block = platform.addInclinedBlock(x)
            if x == w:
                block.addLadder(True)
            y = block.y

        # Next Platform
        y = y - (4 * h) + 3
        platform = level.addPlatform(y)
        platform.addLevelBlock(w)
        for x in range(2*w, width + w, w):
            block = platform.addInclinedBlock(x)
            if x == width - 2*w:
                block.addLadder()
            y = block.y

        # Next Platform
        y = y - (4 * h) + 3
        platform = level.addPlatform(y)
        platform.addLevelBlock(width - 2*w)
        for x in range(width - 3*w, neg(w), neg(w)):
            block = platform.addInclinedBlock(x)
            if x == w:
                block.addLadder(True)
            y = block.y

         # Next Platform
        y = y - (4 * h) + 3
        platform = level.addPlatform(y)
        platform.addLevelBlock(w)
        for x in range(2*w, width + w, w):
            block = platform.addInclinedBlock(x)
            if x == width - 2*w:
                block.addLadder()
            y = block.y

        # Top Platform
        y = y - (4 * h) + 7
        platform = level.addPlatform(y)
        for x in range(0, width - w, w):
            block = platform.addLevelBlock(x)
            if x == width-8*w:
                block.addLadder()
            if x == width-12*w:
                block.addLadder(True)


        # Princess Platform
        y = y - (4 * h)
        platform = level.addPlatform(y)
        for x in range(width - 10*w, width - 7*w, w):
            platform.addLevelBlock(x)


        return level


class LevelBuilder():
    def __init__(self):
        self._platforms = []

    def __iter__(self):
        """ Iterator """
        return iter(self._platforms)

    def __getitem__(self, i):
        return self._platforms[i]

    def __len__(self):
        return len(self._platforms)

    def addPlatform(self, y):
        """ Create a new platform """
        self._platforms.append(PlatformBuilder(y))
        return self._platforms[len(self._platforms) - 1]


class PlatformBuilder():
    def __init__(self, y):
        self._blocks = []
        self.y = y

    def __iter__(self):
        """ Iterator """
        return iter(self._blocks)

    def __getitem__(self, i):
        return self._blocks[i]

    def __len__(self):
        return len(self._blocks)

    def addLevelBlock(self, x):
        """ Block that is not angled """
        self._blocks.append(BlockBuilder(x, self.y))
        i = len(self._blocks) - 1
        return self._blocks[i]

    def addInclinedBlock(self, x):
        """ Block that is angled """
        self.y = self.y - 1
        return self.addLevelBlock(x)


class BlockBuilder():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ladder = None
        self.startingBlock = False

    def addLadder(self, right=False):
        if not right:
            self.ladder = LadderBuilder(self.x, self.y)
        else:
            self.ladder = LadderBuilder(self.x + 24, self.y) # 24 is width of platform minus half width of ladder
        return self.ladder

    def makeStartingBlock(self):
        self.startingBlock = True

    def build(self, sprite):
        return Platform(self.x, self.y, sprite)


class LadderBuilder():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.isCompleteLadder = True

    def makeBroken(self):
        self.isCompleteLadder = False
