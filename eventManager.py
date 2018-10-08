import pygame 
from utils import Singleton 
from enum import Enum 

class Events(Enum): 
    QUIT = 0 
    KEYDOWN = 1
    KEYUP = 2


@Singleton 
class __EventManagerClass: 
    """ No need to create new instances of this """
    def __init__(self): 
        self._listeners = {}
    
    def handlePyGameEvents(self): 
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                self.publish(Events.QUIT, None)
            elif event.type == pygame.KEYDOWN: 
                self.publish(Events.KEYDOWN, event.key)
            elif event.type == pygame.KEYUP: 
                self.publish(Events.KEYUP, event.key)
        
    def subscribe(self, event, func): 
        """ Used when wanting to execute a function when an event happens """
        key = self.__strEvent(event)

        if key not in self._listeners: 
            self._listeners[key] = [func]
        else:
            self._listeners[key].append(func)

    def publish(self, event, data): 
        """ Used when an event happens and you need to run subscribed functions """
        key = self.__strEvent(event)

        if key in self._listeners: 
            for func in self._listeners[key]: 
                func(data)

    def __strEvent(self, event): 
        return "event_{0}".format(event)


# Instance of the Event Manager Class
EventManager = __EventManagerClass()