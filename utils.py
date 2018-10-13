import pygame 


class Spritesheet(object):
    def __init__(self, filename):
        self.sheet = pygame.image.load('assets/sprites/{0}_sheet.png'.format(filename)).convert()
        self.transparency = self.sheet.get_at((0, 0))

    # Load a specific image from a specific rectangle
    def sprite(self, x, y, width, height):
        "Loads image from x,y,x+width,y+height"
        rect = pygame.Rect((x, y, width, height))
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        image.set_colorkey(self.transparency)
        return image

    # Load a flipped sprite 
    def spriteFlipped(self, x, y, width, height): 
        sprite = self.sprite(x, y, width, height) 
        return pygame.transform.flip(sprite, True, False)


def AbstractMethod(method):
    def default_abstract_method(*args, **kwargs):
        raise NotImplementedError('{0} NEEDS to implement the "{1}" method!'.format(args[0].__class__.__name__, method.__name__))

    default_abstract_method.__name__ = method.__name__    
    return default_abstract_method

def DefaultMethod(method): 
    def default_method(*args, **kwargs): 
        pass 
    default_method.__name__ = method.__name__ 
    return default_method


class Singleton:
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




