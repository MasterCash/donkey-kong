"""
This file has everything for our game framework, 
essentially it is one big wrapper around PyGame, 
the goal of this is to make it more portable to
switch to other game frameworks if needed since 
all you need to do is implement the generic interfaces
that everything else uses
"""
import pygame 
import uuid
from utils import AbstractMethod, DefaultMethod, Singleton

class GameSprite(pygame.sprite.Sprite):
    """ Sprite class that represents a sprite """ 
    def __init__(self): 
        super().__init__()
        self.x = 0
        self.y = 0
        self.image = pygame.Surface((0, 0)) 
    
    def draw(self, screen): 
        """ Draws the object on the screen """
        self.image = self.getSprite() 
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y 

        screen.draw(self.image, self.x, self.y)

    @DefaultMethod 
    def getSprite(self): 
        """ Returns the active sprite to display """
        return self.image

    @DefaultMethod 
    def die(self): 
        """ Removes the sprite """
        self.kill()

    @property 
    def image(self): 
        return self._image 

    @image.setter
    def image(self, img): 
        self._image = img 
        self.rect = self._image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    @property 
    def width(self): 
        """ Width of the sprite """
        return self.rect.size[0] 

    @property 
    def height(self):
        """ Height of the sprite """ 
        return self.rect.size[1]

    @property 
    def top(self): 
        """ Top of the sprite """
        return self.x 

    @top.setter 
    def top(self, t): 
        """ Sets where the top side of the sprite is """
        self.x = t
    
    @property 
    def bottom(self): 
        """ Bottom of the sprite """
        return self.y + self.height 

    @bottom.setter 
    def bottom(self, b): 
        """ Sets the bottom position of the sprite """
        self.y = b - self.height 
    
    @property 
    def right(self): 
        """ Right side of the sprite """
        return self.x + self.width

    @right.setter
    def right(self, r): 
        """ Sets where the right side of the sprite is """
        self.x = r - self.width 
    
    @property 
    def left(self): 
        """ Left side of the sprite """
        return self.x 

    @left.setter 
    def left(self, l): 
        """ Sets where the left side of the sprite is """
        self.x = l


class GameObject(GameSprite): 
    """ Everything in the game should extend this class """
    def __init__(self): 
        super().__init__()
        self.__id = uuid.uuid4() # Something to uniquely identify every game object

    @AbstractMethod
    def update(self): 
        pass

    @DefaultMethod 
    def drawExtra(self, screen): 
        pass 

    @DefaultMethod 
    def collision(self, collisionType, direction, obj): 
        pass 
    
    def draw(self, screen): 
        """ Draws the object on the screen """
        super(GameObject, self).draw(screen)
        self.drawExtra(screen)

    @property 
    def id(self): 
        return self.__id 


class GameLevelManager: 
    """
    'Interface' for a Level Manager 
    """
    def __init__(self): 
        pass 

    @AbstractMethod 
    def drawLevel(self, screen): 
        pass 

    @AbstractMethod 
    def advanceLevel(self): 
        pass 


class SpriteGroup: 
    """ Group of Sprites (Wrapper around pygame sprite group) """
    def __init__(self): 
        self._group = pygame.sprite.Group()
    
    def add(self, sprite): 
        """ Adds a sprite to the group """
        if not isinstance(sprite, GameSprite): 
            raise TypeError("Can only add instances of GameSprite to a Sprite Group") 
        
        return self._group.add(sprite) 
    
    def remove(self, sprite): 
        """ Removes a sprite """
        return self._group.remove(sprite)

    def has(self, sprite): 
        """ Checks if a sprite exists in the group """
        return self._group.has(sprite) 

    def empty(self): 
        """ Clears the list """
        return self._group.empty() 

    def sprites(self): 
        """ Returns all of the sprites """
        return self._group.sprites() 

    def draw(self, screen): 
        """ Draws all of the sprites """
        for sprite in self._group: 
            sprite.draw(screen) 

    def update(self, *args): 
        """ Updates all of the sprites """
        for sprite in self._group: 
            sprite.update(*args)

    def __iter__(self): 
        """ Iterator """
        return iter(self.sprites())
    
    def __contains__(self, sprite):
        """ Contains operator """ 
        return self.has(sprite)


class Screen: 
    """ Screen (pygame display) """
    def __init__(self, width, height): 
        self._width = width
        self._height = height

        pygame.init()
        self._display = pygame.display.set_mode((width, height))

    def draw(self, sprite, x, y): 
        """ Draws a sprite on the screen """
        self._display.blit(sprite, (x, y))

    def fill(self, color): 
        """ Fills the screen with a color """
        self._display.fill(color)

    @property 
    def pygameScreen(self): 
        return self._display 

    @property 
    def width(self): 
        return self._width 
    
    @property 
    def height(self): 
        return self._height 


class Window: 
    """ Wrapper around the PyGame GUI """
    def __init__(self, width, height): 
        self._screen = Screen(width, height)

    def close(self): 
        """ Closes the window """
        pygame.quit()
    
    def setTitle(self, title): 
        """ Sets the window title """
        pygame.display.set_caption(title) 
        return self 

    def setIcon(self, icon):
        """ Sets the window icon """
        pygame.display.set_icon(pygame.image.load(icon))
        return self 

    def flip(self): 
        """ Displays everything that has been drawn """
        pygame.display.flip()

    def draw(self, sprite, x, y): 
        """ Draws a sprite on the screen """
        self._screen.draw(sprite, x, y)

    def fill(self, color): 
        """ Fills the screen with a color """
        self._screen.fill(color)

    @property
    def size(self): 
        """ Returns dimensions of the window """
        return (self.width, self.height)

    @property 
    def width(self): 
        """ Width of the window """
        return self._screen.width

    @property 
    def height(self): 
        """ Height of the window """
        return self._screen.height

    @property
    def screen(self): 
        """ Returns screen for drawing """
        return self._screen


@Singleton 
class __ClockClass: 
    def __init__(self): 
        self._clock = pygame.time.Clock()
        self._delta = 0.0

    def forceFPS(self, fps): 
        """ Forces a certain FPS """
        t = self._clock.tick(fps)
        self._delta = t / 1000.0

    @property
    def timeDelta(self): 
        """ Returns the detla time """
        return self._delta

Clock = __ClockClass() # Only instance of the clock class