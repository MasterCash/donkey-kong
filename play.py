"""
This is the file that should be ran when wanting to launch the game 
"""
import pygame
import os
import game as Game
from mario import Mario
from barrel import Barrel


game = Game.GameManager()
game.addPlayer(Mario())
game.addObject(Barrel())
game.play()

