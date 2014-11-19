#INITIALIZATION
import pygame, math, sys
from pygame.locals import *
screen = pygame.display.set_mode((1024, 768)) 
clock = pygame.time.Clock()

#GLOBAL CONSTANTS
DEFAULT_FPS = 30 #Reasonable estimate for final performance. We don't really need more than 45
LOW_FPS     = 10 #For anywhere where you don't need high FPS, such as menu, texts and such

#STARTUP AND MENU
clock.tick(LOW_FPS)
background = pygame.image.load('menu_background.png')
screen.blit(self.background, (0,0))
game_start = 0
while 1:
    #USER INPUT
    for event in pygame.event.get():
        if not hasattr(event, 'key'): continue
        if event.key  == K_ESCAPE: sys.exit(0)
        elif event.key == K_ENTER: game_start = 1
    # RENDERING
    pygame.display.flip()
    #GAME START
    if game_start == 1: break
#MAIN GAME LOOP
while 1:
clock.tick(HIGH_FPS)
    pass
