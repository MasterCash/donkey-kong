"""
Game Manager 
"""
import pygame 
import os
import uuid
from utils import AbstractMethod, DefaultMethod, Singleton, SpriteWrapper
from eventManager import Events, EventManager

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

            # Draw the current level
            self._levelManager.drawLevel(self._window, self._windowWidth, self._windowHeight)

            # Update Everything 
            self._objects.update()
            self._players.update()

            # Draw everything
            for obj in self._objects: 
                obj.draw(self._window)

            for player in self._players: 
                player.draw(self._window)

            pygame.display.flip() # Show most recent drawn items on the screen

    def addPlayer(self, player): 
        """ Adds a player to the game """ 
        self._players.add(SpriteWrapper(player))

    def addObject(self, obj): 
        """ Adds an object to the game """
        self._objects.add(SpriteWrapper(obj))

    def addLevelManager(self, obj): 
        """ Sets the thing used for generating levels """
        if isinstance(obj, GameLevelManager):
            self._levelManager = obj
        return 
    
    def _handleEvents(self): 
        """ Handles events from PyGame """
        EventManager.handlePyGameEvents()

        # Remove objects
        for index in self._toRemove: 
            if len(self._objects) > index and self._objects[index].shouldBeRemoved: 
                del self._objects[index] 
            elif len(self._players) > index and self._players[index].shouldBeRemoved: 
                del self._players[index] 

        self._toRemove = [] 

    def _quit(self, data): 
        pygame.quit()
        os._exit(0)

    
class GameObject: 
    """ 
    Class for a generic Game Object
    Defines abstract methods so they have to be implemented 
    """
    def __init__(self): 
        self.__remove = False
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

    def destroy(self): 
        self.__remove = True

    @property 
    def shouldBeRemoved(self): 
        return self.__remove

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
        

    