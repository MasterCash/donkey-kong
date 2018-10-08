"""
This is the file that should be ran when wanting to launch the game 
"""
import pygame
import os
import game as Game
from mario import Mario
from levels import LevelManager


game = Game.GameManager()
game.addPlayer(Mario())
game.addLevelManager(LevelManager())
game.play()

