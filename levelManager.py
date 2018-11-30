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
        self.isTopOfLadder = False
        self.isBroken = False

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
    def __init__(self, x, y, sprite, broken=False):
        super().__init__()
        self.x = x
        self.y = y
        self.image = sprite
        self.isBroken = broken

class InvisiblePlatform(GameSprite):
    def __init__(self, x, y, sprite, isTopOfLadder = False, isEndOfPlatform=False):
        super().__init__()
        self.x = x
        self.y = y
        self.image = sprite
        self.isTopOfLadder = isTopOfLadder
        self.isBroken = False
        self.isEndOfPlatform = isEndOfPlatform

class InvisibleLadder(GameSprite):
    def __init__(self, x, y, sprite, isTop=False, broken=False):
        super().__init__()
        self.x = x
        self.y = y
        self.image = sprite
        self.isTopOfLadder = isTop
        self.isBroken = broken

class InvisibleWall(GameSprite):
    def __init__(self, x, y, sprite, isLeft):
        super().__init__()
        self.x = x
        self.y = y
        self.image = sprite
        self.isLeftWall = isLeft
        self.isBroken = False


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
        self._invisiblePlatform = self._sheet.invisibleSprite(20, 16)
        self._invisibleTopOfLadder = self._sheet.invisibleSprite(32, 8)
        self._invisibleSideWall = self._sheet.invisibleSprite(1, 600)
        self._winningHeight = 0

        self._windowHeight = 0
        self._windowWidth = 0

    def setWindowInformation(self, width, height):
        """ Set information about the window """
        self._windowWidth = width
        self._windowHeight = height
        self._invisibleSideWall = self._sheet.invisibleSprite(1, height)

        self.buildLevel()

    def update(self):
        """ Update method just like other game objects """
        self.platforms.update()

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
        return [[60, 540], [60, 480]]

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
            self.immovables.add(block.buildImmovable(self._invisiblePlatform, yOffset=2))
            i = i + 1

        self.walls.add(InvisibleWall(0, 0, self._invisibleSideWall, True))
        self.walls.add(InvisibleWall(self._windowWidth, 0, self._invisibleSideWall, False))

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

        self.immovables.add(InvisibleLadder(x, y, self._invisibleLadder, False, not ladder.isCompleteLadder)) # Invisible platform at bottom of the ladder

        if ladder.isCompleteLadder:
            # Full Ladder
            for ladderY in range(y-h, targetY-h, neg(h)):
                self.ladders.add(Ladder(x, ladderY, self._ladder))
        else:
            # Broken Ladder
            self.ladders.add(Ladder(x, y-h, self._ladder, True))
            self.ladders.add(Ladder(x, y-2*h, self._ladder, True))
            self.ladders.add(Ladder(x, targetY, self._ladder, True))

        self.ladders.add(InvisibleLadder(x, targetY-17, self._invisibleLadder, True, not ladder.isCompleteLadder))

        if ladder.isCompleteLadder:
            self.immovables.add(InvisiblePlatform(x-8, targetY - 6*h, self._invisibleTopOfLadder, True)) # Invisible platform at top of the ladder

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
                block = base.addLevelBlock(x)
                if x == 4*w:
                    block.addLadder().makeBroken()

        # Next Platform
        y = y - (5 * h) + 3
        platform = level.addPlatform(y)
        platform.addLevelBlock(width - 2*w)
        for x in range(width - 3*w, neg(w), neg(w)):
            block = platform.addInclinedBlock(x)
            if x == w:
                block.addLadder().alignRight()
            elif x == 8*w:
                block.addLadder().makeBroken()
            elif x == 12*w:
                block.addLadder()
            y = block.y

        # Next Platform
        y = y - (4 * h) + 3
        platform = level.addPlatform(y)
        platform.addLevelBlock(w)
        for x in range(2*w, width, w):
            block = platform.addInclinedBlock(x)
            if x == width - 2*w:
                block.addLadder()
            elif x == width - 10*w:
                block.addLadder()
            y = block.y

        # Next Platform
        y = y - (4 * h) + 3
        platform = level.addPlatform(y)
        platform.addLevelBlock(width - 2*w)
        for x in range(width - 3*w, neg(w), neg(w)):
            block = platform.addInclinedBlock(x)
            if x == w:
                block.addLadder().alignRight()
            elif x == 5*w:
                block.addLadder().makeBroken()
            elif x == 12*w:
                block.addLadder()
            y = block.y

         # Next Platform
        y = y - (4 * h) + 3
        platform = level.addPlatform(y)
        platform.addLevelBlock(w)
        for x in range(2*w, width, w):
            block = platform.addInclinedBlock(x)
            if x == width - 2*w:
                block.addLadder()
            elif x == width - 10*w:
                block.addLadder().makeBroken()
            y = block.y

        # Top Platform
        y = y - (4 * h) + 2
        platform = level.addPlatform(y)
        for x in range(width-2*w, neg(w), neg(w)):
            block = platform.addLevelBlock(x)
            if x == 9*w:
                block.addLadder() # Princess ladder
            if x == 5*w:
                block.addLadder().alignRight(-8)
            if x == 4*w:
                block.addLadder().alignRight(-8)

        # Princess Platform
        y = y - (4 * h)
        platform = level.addPlatform(y)
        for x in range(width - 11*w, width - 7*w, w):
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

    def addLadder(self, offset=0):
        self.ladder = LadderBuilder(self.x + offset, self.y)
        return self.ladder

    def makeStartingBlock(self):
        self.startingBlock = True

    def build(self, sprite):
        return Platform(self.x, self.y, sprite)

    def buildImmovable(self, sprite, offset=0, yOffset=0):
        return InvisiblePlatform(self.x + offset, self.y + yOffset, sprite, False)


class LadderBuilder():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.isCompleteLadder = True

    def alignRight(self, offset=0):
        self.x = self.x + 24 + offset # 24 is width of platform minus half width of ladder
        return self

    def makeBroken(self):
        self.isCompleteLadder = False
