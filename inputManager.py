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
        #if pygame.event.peek(KEYDOWN):
        pygame.event.clear(KEYDOWN)
        pressed = pygame.key.get_pressed()
        for key in self._keyFuncDict:
            if pressed[key]:
                for func in self._keyFuncDict[key]:
                    func(key)
      #for key, func in self._keyFuncPairs:
      #   if pressed[key]: 
      #       func(key)

          
