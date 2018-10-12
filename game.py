"""
Game Manager 
"""
import pygame 
import os
import uuid
from utils import AbstractMethod, Singleton 
from eventManager import Events, EventManager
form inputManager import InputManger

@Singleton
class GameManager: 
    """ Class to manage the state of the game """
    def __init__(self): 
        pygame.init()
        self._window = pygame.display.set_mode((720, 720))
        pygame.display.set_caption('Donkey Kong')
        pygame.display.set_icon(pygame.image.load('assets/icon.png'))

        self._clock = pygame.time.Clock()

        self._objects = []
        self._players = []
        self._toRemove = []
        
        EventManager.subscribe(Events.QUIT, self._quit)

    def play(self): 
        """ Main Game Loop """ 
        while True: 
            self._clock.tick(60)
            self._handleEvents() 

            self._window.fill((255, 255, 255)) # White background

            # Update Everything 
            for i, obj in enumerate(self._objects): 
                self._updateGameObject(obj, i)

            for i, player in enumerate(self._players): 
                self._updateGameObject(player, i)

            # TODO: Collision checking, etc...

            # Draw sprites 
            for i, obj in enumerate(self._objects): 
                self._drawGameObject(obj, i)
            
            for i, player in enumerate(self._players): 
                self._drawGameObject(player, i)

            pygame.display.flip() # Show most recent drawn items on the screen


    def addPlayer(self, player): 
        """ Adds a player to the game """ 
        self._players.append(player)

    def addObject(self, obj): 
        """ Adds an object to the game """
        self._objects.append(obj)


    def _handleEvents(self): 
        """ Handles events from PyGame """
        EventManager.handlePyGameEvents()
        InputManager.check()

        # Remove objects
        for index in self._toRemove: 
            if len(self._objects) > index and self._objects[index].shouldBeRemoved: 
                del self._objects[index] 
            elif len(self._players) > index and self._players[index].shouldBeRemoved: 
                del self._players[index] 

        self._toRemove = [] 


    def _updateGameObject(self, obj, i): 
        """ Updates a game object """ 
        if not isinstance(obj, GameObject): 
            return 

        if obj.shouldBeRemoved: 
            self._toRemove.append(i)
            return

        obj.update() 

    def _drawGameObject(self, obj, i): 
        """ Draws a game object """
        if not isinstance(obj, GameObject): 
            return 

        if obj.shouldBeRemoved: 
            self._toRemove.append(i)
            return 
            
        pos = obj.getPositionAndSize()
        sprite = obj.getSprite() 

        self._window.blit(sprite, (pos[0], pos[1]))

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
    def getPositionAndSize(self): 
        pass

    @AbstractMethod 
    def getSprite(self): 
        pass


    def destroy(self): 
        self.__remove = True

    @property 
    def shouldBeRemoved(self): 
        return self.__remove

    @property
    def id(self): 
        return self.__id



