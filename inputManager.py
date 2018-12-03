#################
# Input Manager #
#################
import queue
#from enums import PlayerState
from utils import Singleton
#from eventManager import Events, EventManager
from collections import deque
from framework import Keys, Events

@Singleton
class __InputManagerClass:
    def __init__(self):
        self._keyFuncDict = {}
        self.keysPressed = []
        self._keysQueued = deque()
        Events.subscribe(Events.KEYDOWN, self.addKey)
        Events.subscribe(Events.KEYUP, self.removeKey)

    def subscribe(self, keys, func):
        for keyEnum in keys:
            key = keyEnum.value
            if self._keyFuncDict.get(key, False) is False:
                self._keyFuncDict[key] = []
            self._keyFuncDict[key].append(func)
            #print("Listen For Called", key, str(func))

    def unsubscribe(self, keys, func):
        for keyEnum in keys:
            key = keyEnum.value
            self._keyFuncDict[key].remove(func)
            #print("Stop Listening Called", key, str(func))

    def handleInput(self):
        for key in self.keysPressed:
            self._keysQueued.append(key)

        for key in self._keysQueued:
            if key in self._keyFuncDict:
                for func in self._keyFuncDict[key]:
                    func(Keys(key)) # Convert the value back to an enum with Keys(#)

        self._keysQueued.clear()

    def addKey(self, key):
        if key not in self.keysPressed:
            self.keysPressed.append(key)

    def removeKey(self, key):
        if key in self.keysPressed:
            self.keysPressed.remove(key)

InputManager = __InputManagerClass()