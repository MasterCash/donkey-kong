"""
Class for managing and handling collisions
"""
from utils import Singleton
from enum import Enum
from framework import SpriteGroup, SpriteCollision

class CollisionTypes(Enum):
    Ladder = 0
    Platform = 1
    Enemy = 2

class CollisionDirection(Enum):
    Left = 0
    Right = 1
    Top = 2
    Bottom = 3


@Singleton
class __CollisionDetectorClass:
    def __init__(self):
        pass

    def check(self, obj1, objectGroup, collisionType):
        """ Checks if a single sprite collides with a sprite group """
        if isinstance(obj1, SpriteGroup):
            for obj in obj1:
                self.check(obj, objectGroup, collisionType)
            return

        hits = SpriteCollision(obj1, objectGroup)
        for hit in hits:
            direction = self._detectDirection(obj1, hit)
            obj1.collision(collisionType, direction, hit)

    def _detectDirection(self, obj1, obj2):
        """ Gets the direction of the collision """
        rect1 = obj1.rect
        rect2 = obj2.rect

        if rect1.midtop[1] > rect2.midtop[1]:
            return CollisionDirection.Top
        elif rect1.midleft[0] > rect2.midleft[0]:
            return CollisionDirection.Left
        elif rect1.midright[0] < rect2.midright[0]:
            return CollisionDirection.Right
        else:
            return CollisionDirection.Bottom

CollisionDetector = __CollisionDetectorClass()