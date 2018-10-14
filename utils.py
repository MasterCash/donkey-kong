import pygame
from types import MethodType

def AbstractMethod(method):
    """ Decorator for forcing children to implement a method """
    def default_abstract_method(*args, **kwargs):
        raise NotImplementedError('{0} NEEDS to implement the "{1}" method!'.format(args[0].__class__.__name__, method.__name__))

    default_abstract_method.__name__ = method.__name__
    return default_abstract_method


def DefaultMethod(method):
    """ Decorator for a efault method that children can override (this does absolutely nothing by the way) """
    return method


class Singleton:
    """ Decorator for making a class a singleton instance """
    def __init__(self, decorated):
        self._decorated = decorated
        self._instance = None

    def __call__(self, *args, **kwargs):
        """ Return the singleton instance """
        if self._instance is None:
            self._instance = self._decorated(*args, **kwargs)

        return self._instance

    def Reset(self):
        """ Clears a singleton object, only used in tests """
        self._instance = None