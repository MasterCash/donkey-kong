import pygame 
from types import MethodType

class Spritesheet(object):
    def __init__(self, filename):
        self.sheet = pygame.image.load('assets/sprites/{0}_sheet.png'.format(filename)).convert()
        self.transparency = self.sheet.get_at((0, 0))

    # Load a specific image from a specific rectangle
    def sprite(self, x, y, width, height):
        """ Loads image from x,y,x+width,y+height """
        rect = pygame.Rect((x, y, width, height))
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        image.set_colorkey(self.transparency)
        return image
    
    def spriteFlipped(self, x, y, width, height): 
        """ Returns a sprite, but flipped horizontally """
        sprite = self.sprite(x, y, width, height) 
        return pygame.transform.flip(sprite, True, False)


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