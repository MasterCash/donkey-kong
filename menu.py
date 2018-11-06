#from utils import AbstractMethod, DefaultMethod, Singleton
import pygame
import os
from framework import SpriteGroup, Window, Clock, GameLevelManager, Events, Sound, GameCollectible

screen_width=544
screen_height=600
# Text Renderer
def text_format(message, textFont, textSize, textColor):
    newFont=pygame.font.Font(textFont, textSize)
    newText=newFont.render(message, 0, textColor)
 
    return newText
# Main Menu
def menu():
 
    menu=True
    selected="start"
    # Colors
    white=(255, 255, 255)
    black=(0, 0, 0)
    gray=(50, 50, 50)
    red=(255, 0, 0)
    green=(0, 255, 0)
    blue=(0, 0, 255)
    yellow=(255, 255, 0)
 
    # Game Fonts
    font = "Players.ttf"
 
 
    # Game Framerate
    clock = pygame.time.Clock()
    FPS=60
    screen=pygame.display.set_mode((544, 600))
    while menu:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    selected="start"
                elif event.key==pygame.K_DOWN:
                    selected="quit"
                if event.key==pygame.K_RETURN:
                    if selected=="start":
                        print("Start")
                        return
                    if selected=="quit":
                        pygame.quit()
                        quit()
        # Main Menu UI
        screen.fill(black)
        title=text_format("Donkey", font, 90, blue)
        title2=text_format("Kong", font, 90, blue)


        if selected=="start":
            text_start=text_format("START", font, 75, white)
        else:
            text_start = text_format("START", font, 75, gray)
        if selected=="quit":
            text_quit=text_format("QUIT", font, 75, white)
        else:
            text_quit = text_format("QUIT", font, 75, gray)
 
        title_rect=title.get_rect()
        title2_rect=title2.get_rect()
        start_rect=text_start.get_rect()
        quit_rect=text_quit.get_rect()
 
        # Main Menu Text
        screen.blit(title, (screen_width/2 - (title_rect[2]/2), 80))
        screen.blit(title2, (screen_width/2 - (title2_rect[2]/2), 160))
        screen.blit(text_start, (screen_width/2 - (start_rect[2]/2), 300))
        screen.blit(text_quit, (screen_width/2 - (quit_rect[2]/2), 360))
        pygame.display.update()
        clock.tick(60)
        pygame.display.set_caption("Python - Pygame Simple Main Menu Selection")

