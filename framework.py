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
from enum import Enum


class Sound(object):
    def __init__(self, file):
        self._file = 'assets/sounds/{0}.wav'.format(file)
        self._sound = pygame.mixer.Sound(self._file)

    def play(self):
        self._sound.play(0)

    def playNTimes(self, n):
        self._sound.play(n)

    def loop(self):
        self._sound.play(-1)

    def stop(self):
        self._sound.stop()

class Text(object):
    def __init__(self, text, fontFamily='Courier New', fontSize=20, color=(255, 255, 255)):
        self._text = str(text)
        self._color = color
        self._font = pygame.font.SysFont(fontFamily, fontSize)

    @property
    def text(self):
        return self._text

    def setText(self, text):
        self._text = str(text)

    @property
    def image(self):
        return self._font.render(self._text, False, self._color)


class Image(object):
    def __init__(self, sheet, x, y, width, height):
        self.rect = pygame.Rect((x, y, width, height))
        self._image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self._image.blit(sheet, (0, 0), self.rect)

    def flip(self):
        """ Flips an image """
        self._image = pygame.transform.flip(self._image, True, False)
        self.rect = self._image.get_rect()
        return self

    def rotate(self, angle):
        """ Rotates an image """
        self._image = pygame.transform.rotate(self._image, -1 * angle)
        self.rect = self._image.get_rect()
        return self

    @property
    def image(self):
        return self._image

    @property
    def width(self):
        """ Width of the sprite """
        return self.rect.size[0]

    @property
    def height(self):
        """ Height of the sprite """
        return self.rect.size[1]

class SpriteSheet(object):
    """ Used for loading sprites from a sprite sheet """
    def __init__(self, filename):
        self.invisible = pygame.image.load('assets/sprites/invisible_sheet.png')
        self.sheet = pygame.image.load('assets/sprites/{0}_sheet.png'.format(filename))

    def sprite(self, x, y, width, height):
        """ Loads image from x, y, x+width, y+height """
        return Image(self.sheet, x, y, width, height)

    def spriteFlipped(self, x, y, width, height):
        """ Returns a sprite, but flipped horizontally """
        return self.sprite(x, y, width, height).flip()

    def invisibleSprite(self, width, height):
        """ Returns invisible sprite"""
        return Image(self.invisible, 0, 0, width, height)

class GameSprite(pygame.sprite.Sprite):
    """ Sprite class that represents a sprite """
    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
        self.image = pygame.Surface([0, 0])
        self.rect = self.image.get_rect()
        self.__isDying = False

    def draw(self, screen):
        """ Draws the object on the screen """
        self.image = self.getSprite()
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        screen.draw(self, self.x, self.y)

    @DefaultMethod
    def getSprite(self):
        """ Returns the active sprite to display """
        return self.image

    @DefaultMethod
    def remove(self):
        """ Remove the sprite """
        self.kill()

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, img):
        if isinstance(img, Image):
            self._image = img.image
        else:
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
        return self.y

    @top.setter
    def top(self, t):
        """ Sets where the top side of the sprite is """
        self.y = t

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

    @property
    def centerX(self):
        return self.x + ((1/2) * self.width)

    @centerX.setter
    def centerX(self, x):
        self.x = x - ((1/2) * self.width)

    @property
    def centerY(self):
        return self.y + ((1/2) * self.height)

    @centerY.setter
    def centerY(self, y):
        self.y = y - ((1/2) * self.height)


def SpriteCollision(sprite, spriteGroup, kill=False):
    """ Checks for collission between a sprite and a sprite group """
    return pygame.sprite.spritecollide(sprite, spriteGroup, kill)


class GameObject(GameSprite):
    """ Everything in the game should extend this class """
    def __init__(self):
        super().__init__()
        self.__id = uuid.uuid4() # Something to uniquely identify every game object
        self.__isDying = False

    @DefaultMethod
    def update(self):
        pass

    @DefaultMethod
    def collectedItem(self, item, collectionType):
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

    @property
    def isDying(self):
        return self.__isDying

    @isDying.setter
    def isDying(self, val):
        self.__isDying = val

    @property
    def lives(self):
        return self.__lives

    @staticmethod
    def DeathMethod(func):
        def wrapper(self, *args, **kwargs):
            self.__isDying = True
            self.__lives = self.__lives - 1
            return func(self, *args, **kwargs)

        return wrapper

    @staticmethod
    def HasLives(numberOfLives):
        def decorator(func):
            def wrapper(self, *args, **kwargs):
                self.__lives = numberOfLives
                return func(self, *args, **kwargs)
            return wrapper
        return decorator


class GameCollectible(GameObject):
    """ Something Collectible, like a hammer or the flaming oil can """
    def __init__(self):
        super().__init__()

    @DefaultMethod
    def onCollect(self, collectedBy, collectionType):
        collectedBy.collectedItem(self)
        self.kill()


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

    @AbstractMethod
    def getSpawnLocations(self):
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

    def __len__(self):
        return len(self._group)


class Screen:
    """ Screen (pygame display) """
    def __init__(self, width, height):
        self._width = width
        self._height = height

        pygame.init()
        self._display = pygame.display.set_mode((width, height))

    def draw(self, sprite, x, y):
        """ Draws a sprite on the screen """
        if hasattr(sprite, 'image'):
            self._display.blit(sprite.image, (x, y))
        else:
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
        self._clock = None
        self._delta = 0.0
        self.fps = 60

    def forceFPS(self, fps):
        """ Forces a certain FPS """
        if (self._clock is None):
            self._clock = pygame.time.Clock()

        self.fps = fps
        t = self._clock.tick(self.fps)
        self._delta = t / 1000.0

    @property
    def timeDelta(self):
        """ Returns the detla time """
        return self._delta

Clock = __ClockClass() # Only instance of the clock class


class Keys(Enum):
    """ Enum wrapper for pygame keys """
    LEFT = pygame.K_LEFT
    RIGHT = pygame.K_RIGHT
    DOWN = pygame.K_DOWN
    UP = pygame.K_UP
    SPACE = pygame.K_SPACE
    W = pygame.K_w
    A = pygame.K_a
    S = pygame.K_s
    D = pygame.K_d
    Num_1 = pygame.K_1
    Num_2 = pygame.K_2
    Num_3 = pygame.K_3
    Num_4 = pygame.K_4
    Num_5 = pygame.K_5
    Num_6 = pygame.K_6


@Singleton
class __EventManagerClass:
    """ Handles events for the framework """
    def __init__(self):
        self._listeners = {}

    def handleEvents(self):
        """ Looks at pygame events and publishes them """
        for event in pygame.event.get():
            eventStr = self.__str(event.type)
            if eventStr == self.QUIT:
                self.publish(eventStr, None)
            elif eventStr == self.KEYDOWN:
                self.publish(eventStr, event.key)
            elif eventStr == self.KEYUP:
                self.publish(eventStr, event.key)

    def subscribe(self, event, func):
        """ Subscribes to event and executes func when event happens """
        if event not in self._listeners:
            self._listeners[event] = [func]
        else:
            self._listeners[event].append(func)

    def publish(self, event, *data):
        """ Dispatches an event and executes subscribers """
        if event in self._listeners:
            for func in self._listeners[event]:
                func(*data)

    def __str(self, k):
        return "event_{0}".format(k)

    """
    Everything below this is an "Enum" value for this class
    """
    @property
    def QUIT(self):
        return self.__str(pygame.QUIT)

    @property
    def KEYDOWN(self):
        return self.__str(pygame.KEYDOWN)

    @property
    def KEYUP(self):
        return self.__str(pygame.KEYUP)

    @property
    def GAMEOVER(self):
        return self.__str("GameOver")

Events = __EventManagerClass()