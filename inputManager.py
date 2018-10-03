#################
# Input Manager #
#################
import pygame
from pygame.locals import *

#from enums import PlayerState
from utils import Singleton


@Singleton
class InputManager:
  
    def __init__(self):
        self._keyFuncDict = {}
        self.keysPressed = []

    def listenFor(self, keys, func):
        for key in keys:
            if self._keyFuncDict.get(key, False) is False:
                self._keyFuncDict[key] = [func]
            self._keyFuncDict[key].append(func)
        print("Listen For Called", key, str(func))
    
    def stopListening(self, keys, func):
        for key in keys:
            self._keyFunDic[key].remove(func)
        print("Stop Listening Called")
  
    def check(self):
        pressed = pygame.key.get_pressed()
        for key in self._keyFuncDict:
            if pressed[key]:
                for func in self._keyFuncDict[key]:
                    func(key)

    def checkWithEvents(self):
        for key in self.keysPressed:
            if key in self.keyFuncDict:
                for func in self._keyFuncDict[key]:
                    func(key)
