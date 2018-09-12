"""
This is the file that should be ran when wanting to launch the game 
"""
import pygame
import os
from mario import Mario

targetFPS = 60

# Setup PyGame and game window
pygame.init()
window = pygame.display.set_mode((720, 720))
pygame.display.set_caption('Donkey Kong')
pygame.display.set_icon(pygame.image.load('assets/icon.png'))

clock = pygame.time.Clock()
mario = Mario()

while True:  
    clock.tick(targetFPS) 

    # Handle PyGame events 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            pygame.quit()
            os._exit(0)
    
    window.fill((255, 255, 255)) # Fill background with white

    # Update everything
    mario.update()

    # Draw everything
    mario.draw(window)
    
    print(mario.position) # Print Mario's position (for the demo)
    
    # Flip screen (to display what has been drawn)
    pygame.display.flip()

