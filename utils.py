import pygame 

class Spritesheet(object):
    def __init__(self, filename):
        self.sheet = pygame.image.load('assets/sprites/{0}_sheet.png'.format(filename)).convert()
        self.transparency = self.sheet.get_at((0, 0))

    # Load a specific image from a specific rectangle
    def sprite_at(self, rectangle):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        image.set_colorkey(self.transparency)
        return image
        
    # Load a whole bunch of images and return them as a list
    def sprites_at(self, rects):
        "Loads multiple images, supply a list of coordinates" 
        return [self.image_at(rect) for rect in rects]

    # Load a whole strip of images
    def load_strip(self, rect, image_count):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups)


def AbstractMethod(method):
    def default_abstract_method(*args, **kwargs):
        raise NotImplementedError('{0} NEEDS to implement the "{1}" method!'.format(args[0].__class__.__name__, method.__name__))

    default_abstract_method.__name__ = method.__name__    
    return default_abstract_method


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


