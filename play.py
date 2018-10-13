"""
This is the file that should be ran when wanting to launch the game 
"""
import pygame
import os
import game as Game
from mario import Mario
from barrel import Barrel
from princess import Princess
from levelManager import LevelManager


game = Game.GameManager()
game.addPlayer(Mario())
game.addObject(Princess())
game.addObject(Barrel())
game.addLevelManager(LevelManager())
game.play()

