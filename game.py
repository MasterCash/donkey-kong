"""
Game Manager 
"""
import pygame 
import os
import uuid
from utils import AbstractMethod, DefaultMethod, Singleton
from eventManager import Events, EventManager
from types import MethodType
from inputManager import InputManager


@Singleton
class GameManager: 
    """ Class to manage the state of the game """
    def __init__(self): 
        pygame.init()
        self._windowWidth = 544
        self._windowHeight = 600
        self._window = pygame.display.set_mode((self._windowWidth, self._windowHeight))
        pygame.display.set_caption('Donkey Kong')
        pygame.display.set_icon(pygame.image.load('assets/icon.png'))

        self._clock = pygame.time.Clock()

        self._objects = pygame.sprite.Group()
        self._players = pygame.sprite.Group()
        self._toRemove = []
        
        EventManager.subscribe(Events.QUIT, self._quit)

        self._levelManager = None


    def play(self): 
        """ Main Game Loop """ 
        if self._levelManager is None: 
           raise Exception("No Level Manager")

        while True: 
            self._clock.tick(60)
            self._handleEvents() 

            # Update Everything 
            self._objects.update()
            self._players.update()
            self._levelManager.update()

            for player in self._players: 
                hits = pygame.sprite.spritecollide(player, self._levelManager.platforms, False)
                for hit in hits: 
                    player.y = hit.rect.top - (player.rect.size[0]) + 1

            # Draw everything
            self._levelManager.draw(self._window)
            for obj in self._objects: 
                obj.draw(self._window)

            for player in self._players: 
                player.draw(self._window)

            pygame.display.flip() # Show most recent drawn items on the screen

    def addPlayer(self, player): 
        """ Adds a player to the game """ 
        self._players.add(_MakeSprite(player))

    def addObject(self, obj): 
        """ Adds an object to the game """
        self._objects.add(_MakeSprite(obj))

    def addLevelManager(self, obj): 
        """ Sets the thing used for generating levels """
        if isinstance(obj, GameLevelManager):
            self._levelManager = obj
            self._levelManager.setWindowInformation(self._windowWidth, self._windowHeight)

        return 
    
    def _handleEvents(self): 
        """ Handles events from PyGame """
        EventManager.handlePyGameEvents()
        InputManager.check()

    def _quit(self, data): 
        pygame.quit()
        os._exit(0)



def _MakeSprite(obj): 
    """ Method for transforming a sprite object into something that can be drawn """
    # New update method
    obj._update = obj.update 
    def update(self): 
        self._update() 
    obj.update = MethodType(update, obj)

    # New Draw Method 
    def draw(self, screen): 
        self.image = self.getSprite() 
        self.rect = self.image.get_rect() 
        self.rect.x = self.x 
        self.rect.y = self.y 
        
        screen.blit(self.image, (self.rect.x, self.rect.y)) 
        self.drawExtra(screen) 

    obj.draw = MethodType(draw, obj)

    # Initial setup of stuff for drawing
    obj.image = obj.getSprite() 
    obj.rect = obj.image.get_rect() 
    obj.rect.x = obj.x 
    obj.rect.y = obj.y 

    return obj


class GameObject(pygame.sprite.Sprite): 
    """ 
    Class for a generic Game Object
    Defines abstract methods so they have to be implemented 
    """
    def __init__(self): 
        super().__init__()
        self.__id = uuid.uuid4()

    @AbstractMethod 
    def update(self): 
        pass 

    @AbstractMethod 
    def getSprite(self): 
        pass

    @DefaultMethod 
    def drawExtra(self, screen): 
        pass

    @property
    def id(self): 
        return self.__id


class GameLevelManager: 
    """
    'Interface' for a Level Manager 
    """
    def __init__(self): 
        pass

    @AbstractMethod 
    def drawLevel(self, screen): 
        pass 
    
    @AbstractMethod 
    def advanceLevel(self): 
        pass 
        

    