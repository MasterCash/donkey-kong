"""
Game Manager
"""
import os
import uuid
from enum import Enum
from utils import AbstractMethod, DefaultMethod, Singleton
from inputManager import InputManager
from collisionDetector import CollisionDetector, CollisionTypes, CollectionTypes
from framework import SpriteGroup, Window, Clock, GameLevelManager, Events, Sound, GameCollectible

class GameState(Enum):
    MainMenu = 0
    Playing = 1
    Paused = 2
    DeathScreen = 3

@Singleton
class GameManager:
    """ Class to manage the state of the game """
    def __init__(self, window):
        self._window = window

        self._objects = SpriteGroup()
        self._players = SpriteGroup()
        self._enemies = SpriteGroup()
        self._collectibles = SpriteGroup()

        self._levelManager = None

        self._backgroundMusic = Sound('06_Stage_1_BGM')
        self._backgroundMusic.loop()

        self.state = GameState.Playing

        self._playing = True
        self._victory = False

    def play(self):
        """ Main Game Loop """
        if self._levelManager is None:
           raise Exception("No Level Manager")

        Clock.resetDelta() # Fix large time delta

        # Set the players spawn locations
        for player in self._players:
            player.spawn(60, 540)

        while self._playing:
            Clock.forceFPS(60)

            # Game Routine
            self._checkForDeath()
            self._checkForVictory()
            self._checkForLoss()

            self._handleEvents()
            self._update()
            self._collisionCheck()
            self._draw()

        # Clear everything
        self._players.empty()
        self._collectibles.empty()
        self._enemies.empty()
        self._objects.empty()

        return self._victory

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

    def addCollectible(self, collectible):
        """ Adds a collectible item to the game """
        if not isinstance(collectible, GameCollectible):
            return self

        self._collectibles.add(collectible)
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
        if self.state == GameState.DeathScreen:
            return

        Events.handleEvents()
        InputManager.handleInput()

    def _update(self):
        """ Updates everything """
        if self.state == GameState.DeathScreen:
            return

        self._objects.update()
        self._players.update()
        self._enemies.update()
        self._collectibles.update()
        self._levelManager.update()

    def _collisionCheck(self):
        """ Checks for collisions """
        if self.state == GameState.DeathScreen:
            return

        CollisionDetector.check(self._players, self._levelManager.ladders, CollisionTypes.Ladder)
        CollisionDetector.check(self._players, self._levelManager.platforms, CollisionTypes.Platform)
        CollisionDetector.check(self._players, self._levelManager.immovables, CollisionTypes.Immovable)
        CollisionDetector.check(self._players, self._levelManager.walls, CollisionTypes.Wall )
        CollisionDetector.check(self._players, self._enemies, CollisionTypes.Enemy)

        CollisionDetector.checkCollection(self._collectibles, self._players, CollectionTypes.Player)
        CollisionDetector.checkCollection(self._collectibles, self._enemies, CollectionTypes.Enemy)
        CollisionDetector.check(self._enemies, self._levelManager.ladders, CollisionTypes.Ladder)
        CollisionDetector.check(self._enemies, self._levelManager.platforms, CollisionTypes.Platform)
        CollisionDetector.check(self._enemies, self._levelManager.immovables, CollisionTypes.Immovable)
        CollisionDetector.check(self._enemies, self._levelManager.walls, CollisionTypes.Wall )

    def _draw(self):
        """ Draws everything on the window """
        self._levelManager.draw(self._window)
        self._objects.draw(self._window)
        self._collectibles.draw(self._window)
        self._players.draw(self._window)

        if self.state != GameState.DeathScreen:
            self._enemies.draw(self._window)

        self._window.flip()

    def _checkForDeath(self):
        death = False

        # Check death of a player
        for player in self._players:
            if player.isDying:
                death = True
                break

        # Check death of an enemy
        if death == False:
            for enemy in self._enemies:
                if enemy.isDying:
                    death = True
                    break

        if death:
            self.state = GameState.DeathScreen
            if len(self._players) == 1:
                self._enemies.empty()

                # Remove clearable collectibles
                for collectible in self._collectibles:
                    if collectible.canBeCleared:
                        collectible.kill()
        else:
<<<<<<< HEAD
            self.state = GameState.Playing
=======
            self.state = GameState.Playing

    def _checkForVictory(self):
        self._victory = False

        for player in self._players:
            self._victory = self._levelManager.isLevelCompleted(player)

            if self._victory:
                break

        self._playing = not self._victory

        return self._victory

    def _checkForLoss(self):
        if len(self._players) == 0:
            self._victory = False
            self._playing = False

    def _quit(self, data):
        """ Closes the window """
        self._window.close()
        os._exit(0)
>>>>>>> master
