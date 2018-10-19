"""
Game Manager
"""
import os
import uuid
from utils import AbstractMethod, DefaultMethod, Singleton
#from eventManager import Events, EventManager
from inputManager import InputManager
from collisionDetector import CollisionDetector, CollisionTypes
from framework import SpriteGroup, Window, Clock, GameLevelManager, Events

@Singleton
class GameManager:
    """ Class to manage the state of the game """
    def __init__(self):
        self._window = Window(544, 600).setTitle('Donkey Kong').setIcon('assets/icon.png')
        Events.subscribe(Events.QUIT, self._quit)

        self._objects = SpriteGroup()
        self._players = SpriteGroup()
        self._enemies = SpriteGroup()

        self._levelManager = None

    def play(self):
        """ Main Game Loop """
        if self._levelManager is None:
           raise Exception("No Level Manager")

        while True:
            Clock.forceFPS(60)

            # Game Routine
            self._handleEvents()

            self._update()
            self._collisionCheck()
            self._draw()

            self._window.flip()

    def addPlayer(self, player):
        """ Adds a player to the game """
        self._players.add(player)
        return self

    def addObject(self, obj):
        """ Adds an object to the game """
        self._objects.add(obj)
        return self

    def addEnemy(self, enemy):
        """ Adds an enemy to the game """
        self._enemies.add(enemy)
        return self

    def addLevelManager(self, obj):
        """ Sets the thing used for generating levels """
        if not isinstance(obj, GameLevelManager):
            return self

        self._levelManager = obj
        self._levelManager.setWindowInformation(self._window.width, self._window.height)
        return self

    def _handleEvents(self):
        """ Handles events from PyGame """
        Events.handleEvents()
        InputManager.handleInput()

    def _update(self):
        """ Updates everything """
        self._objects.update()
        self._players.update()
        self._enemies.update()
        self._levelManager.update()

    def _collisionCheck(self):
        """ Checks for collisions """
        CollisionDetector.check(self._players, self._levelManager.ladders, CollisionTypes.Ladder)
        CollisionDetector.check(self._players, self._levelManager.platforms, CollisionTypes.Platform)
        CollisionDetector.check(self._players, self._levelManager.immovables, CollisionTypes.Immovable)
        CollisionDetector.check(self._players, self._enemies, CollisionTypes.Enemy)

    def _draw(self):
        """ Draws everything on the window """
        self._levelManager.draw(self._window)
        self._objects.draw(self._window)
        self._players.draw(self._window)
        self._enemies.draw(self._window)

    def _quit(self, data):
        """ Closes the window """
        self._window.close()
        os._exit(0)