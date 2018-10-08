#################
# Input Manager #
#################
import pygame
from pygame.locals import *
import queue
#from enums import PlayerState
from utils import Singleton
from eventManager import Events, EventManager
from collections import deque

@Singleton
class InputManager:
  
    def __init__(self):
        self._keyFuncDict = {}
        self.keysPressed = []
        self._keysQueued = deque()
        EventManager.subscribe(Events.KEYDOWN, self.addKey)
        EventManager.subscribe(Events.KEYUP, self.removeKey)
        
    def subscribe(self, keys, func):
        for key in keys:
            if self._keyFuncDict.get(key, False) is False:
                self._keyFuncDict[key] = [func]
            self._keyFuncDict[key].append(func)
        print("Listen For Called", key, str(func))
    
    def unsubscribe(self, keys, func):
        for key in keys:
            self._keyFunDic[key].remove(func)
        print("Stop Listening Called")
  
    def check(self):
        for key in self.keysPressed:
            self._keysQueued.append(key)
        for key in self._keysQueued:
            if key in self._keyFuncDict:
                for func in self._keyFuncDict[key]:
                    func(key)
        self._keysQueued.clear()

    def addKey(self, key):
        if key not in self.keysPressed:
            self.keysPressed.append(key)

    def removeKey(self, key):
        if key in self.keysPressed:
            self.keysPressed.remove(key)
