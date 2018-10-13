"""
Class for the princess
"""
import pygame 
from utils import Spritesheet
from game import GameObject

class Princess(GameObject): 
    def __init__(self): 
        super().__init__()
        self._sheet = Spritesheet('princess')

        self._sprites = { 
            'standing': self._sheet.sprite_at((0, 0, 30, 44)), 
            'dance1': self._sheet.sprite_at((50, 0, 30, 44)), 
            'dance2': self._sheet.sprite_at((96, 0, 30, 44)), 
            'help': self._sheet.sprite_at((240, 10, 46, 16))
        }

        self._currentSprite = self._sprites['standing']
        self.x = 217
        self.y = 76
        self.__isScreaming = False

        self.ticks = -180

    def update(self): 
        self.ticks = self.ticks + 1 
        if 60 < self.ticks <= 70 or 100 < self.ticks <= 110: 
            self._currentSprite = self._sprites['dance1']
            self.__isScreaming = True
        elif 80 < self.ticks <= 90 or 120 < self.ticks <= 130: 
            self._currentSprite = self._sprites['dance2']
            self.__isScreaming = True
        else:
            self._currentSprite = self._sprites['standing'] 

        if self.ticks == 130: 
            self.ticks = -180 # ~3 seconds
            self.__isScreaming = False
        
    def collissionCheck(self, otherObject): 
        """ No collissions """
        return False 

    def getPositionAndSize(self): 
        return (self.x, self.y, 30, 44)
    
    def getSprite(self): 
        return self._currentSprite


    def drawExtra(self, screen): 
        """ Used for drawing the help words """
        if self.__isScreaming: 
            screen.blit(self._sprites['help'], (self.x + 35, self.y - 10))