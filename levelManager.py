import pygame 
import json
from utils import Singleton
from game import GameLevelManager 
from utils import Spritesheet


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite): 
        super().__init__()
        self.image = sprite

        
@Singleton
class LevelManager(GameLevelManager): 
    def __init__(self): 
        GameLevelManager.__init__(self)
        self.__currentLevel = 0

        self.platforms = pygame.sprite.Group()
        
        self._sheet = Spritesheet('level')
        self._platform = self._sheet.sprite_at((0, 1, 32, 16))
        self._ladder = self._sheet.sprite_at((33, 1, 16, 8))

        self._princessSheet = Spritesheet('princess')
        self._princess = self._princessSheet.sprite_at((0, 0, 30, 44))

        # Read levels from the levels file
        with open('assets/levels.json', 'r') as f:
            self._levels = json.load(f)

    def drawLevel(self, screen, width, height): 
        """ Draws all of the sprites for the level design """
        screen.fill((1, 1, 1)) # Background color
        w = 32 # Sprite width
        h = 16 # Sprite height
        
        def drawLadder(x, y): 
            targetY = y - (int((4*h)/8) * 8) + h-2
            for y1 in range(y-6, targetY, -8):
                screen.blit(self._ladder, (x, y1))

        def drawLtoRPlatform(y): 
            lastX = 0
            for x in range(w, width + w, w): 
                screen.blit(self._platform, (x, y))
                y = y - 1
                lastX = x

            # Add ladder to next platform
            x = lastX - 2*w
            drawLadder(x, y)
            return y 

        def drawRtoLPlatform(y): 
            lastX = 0
            for x in range(width - (2 * w), 0 - w, w * -1): 
                screen.blit(self._platform, (x, y))
                y = y - 1
                lastX = x

            # Add ladder to next platform
            x = lastX + 1.5*w
            drawLadder(x, y)
            return y

        # Flat section of first platform
        y = height - 2 * h
        lastX = 0
        for x in range(0, int(width/2), w): 
            screen.blit(self._platform, (x, y))
            lastX = x

        # Angled section of first platform
        for x in range(lastX + w, width, w):
            screen.blit(self._platform, (x, y))
            y = y - 1
            lastX = x

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

        # Top platform 
        y = y - (4 * h) + 2
        for x in range(0 - w, width + w, w): 
            screen.blit(self._platform, (x, y))
        
        # Princess Peach Platform
        y = y - (4 * h)
        for x in range(int(width/2.5), int(width/2.5) + (3 * w), w):
            screen.blit(self._platform, (x, y))
            lastX = x
        
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

    def advanceLevel(self): 
        """ Moves to the next level """
        self.__currentLevel = self.__currentLevel + 1 
        

    def isLevelCompleted(self, player): 
        """ Checks if the level has been completed """
        pass 

    @property 
    def currentLevel(self): 
        """ Returns the current level """
        return self.__currentLevel


