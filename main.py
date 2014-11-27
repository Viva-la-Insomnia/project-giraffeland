#INITIALIZATION
import pygame, math, sys
from pygame.locals import *
screen = pygame.display.set_mode((1024, 768), FULLSCREEN)
pygame.display.set_caption('Project-Giraffeland')
clock = pygame.time.Clock()

#GLOBAL CONSTANTS
DEFAULT_FPS = 40 #Reasonable estimate for final performance. We don't really need more than 45

#INTRO		
intro_logo = pygame.image.load('graphics/intro_logo.png').convert()
intro_background = pygame.image.load('graphics/intro_background.png').convert()

for i in range(128) : #LOGO FADEIN
	clock.tick(32)
	screen.blit(intro_background, (0,0))
	intro_logo.set_alpha(2*i)
	screen.blit(intro_logo, (200, 200))
	pygame.display.flip()
for i in range(128) : #PAUSE
	clock.tick(32)

#STARTUP AND MENU
class CursorSprite(pygame.sprite.Sprite):
	def __init__(self, image, position):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(image).convert_alpha()
		self.rect = self.image.get_rect()
		self.position = position
	def update(self):
		self.rect.center = self.position

background = pygame.image.load('graphics/menu_background.png').convert()
menu_background1 = pygame.image.load('graphics/menu_background1.png').convert()
menu_background2 = pygame.image.load('graphics/menu_background2.png').convert()
menu_background3 = pygame.image.load('graphics/menu_background3.png').convert()

screen.blit(background, (0,0))
recta = screen.get_rect()
cursor = CursorSprite('graphics/cursor.png', recta.center)
cursor_group = pygame.sprite.RenderPlain(cursor) #Sprites are always managed in groups, no matter if there is one or over 9k
game_start = 0
pygame.mouse.set_visible(0)

MENU0_BOX1 = Rect(196, 444, 553, 60)
MENU0_BOX2 = Rect(196, 564, 553, 60)
MENU0_BOX3 = Rect(196, 621, 553, 60)

MENU1_BOX1 = Rect(382, 462, 274, 60)
MENU1_BOX2 = Rect(472, 219, 158, 63)

MENU2_BOX1 = Rect(382, 462, 274, 60)

MENU3_BOX1 = Rect(382, 462, 274, 60)

menuMode = 0

while 1: #Menu loop
	clock.tick(DEFAULT_FPS)

	if menuMode == 0 :
		#USER INPUT
		for event in pygame.event.get() :
			if event.type == pygame.KEYDOWN :
				if event.key == pygame.K_ESCAPE : sys.exit(0)
			elif event.type == pygame.MOUSEMOTION :
				cursor.position = event.pos
			elif event.type == pygame.MOUSEBUTTONDOWN :
				if MENU0_BOX1.collidepoint(event.pos) == True : menuMode = 1
				elif MENU0_BOX2.collidepoint(event.pos) == True : menuMode = 2
				elif MENU0_BOX3.collidepoint(event.pos) == True : menuMode = 3
		# RENDERING
		screen.blit(background, (0,0))

	elif menuMode == 1 :
		#USER INPUT
		for event in pygame.event.get() :
			if event.type == pygame.KEYDOWN :
				if event.key == pygame.K_ESCAPE : sys.exit(0)
			elif event.type == pygame.MOUSEMOTION :
				cursor.position = event.pos
			elif event.type == pygame.MOUSEBUTTONDOWN :
				if MENU1_BOX1.collidepoint(event.pos) == True : menuMode = 0
				elif MENU1_BOX2.collidepoint(event.pos) == True : game_start = 1
		# RENDERING
		screen.blit(menu_background1, (0,0))
	
	elif menuMode == 2 :
		#USER INPUT
		for event in pygame.event.get() :
			if event.type == pygame.KEYDOWN :
				if event.key == pygame.K_ESCAPE : sys.exit(0)
			elif event.type == pygame.MOUSEMOTION :
				cursor.position = event.pos
			elif event.type == pygame.MOUSEBUTTONDOWN :
				if MENU2_BOX1.collidepoint(event.pos) == True : menuMode = 0
		# RENDERING
		screen.blit(menu_background2, (0,0))
	
	elif menuMode == 3 :
		#USER INPUT
		for event in pygame.event.get() :
			if event.type == pygame.KEYDOWN :
				if event.key == pygame.K_ESCAPE : sys.exit(0)
			elif event.type == pygame.MOUSEMOTION :
				cursor.position = event.pos
			elif event.type == pygame.MOUSEBUTTONDOWN :
				if MENU3_BOX1.collidepoint(event.pos) == True : menuMode = 0
		# RENDERING
		screen.blit(menu_background3, (0,0))

	cursor_group.update()
	cursor_group.draw(screen)
	pygame.display.flip()
	#GAME START
	if game_start == 1: break

#CLASSES, METHODS, STUFF
class PlayerSprite(pygame.sprite.Sprite):
	TERMINAL_VELOCITY = 100
	MASS = 80

	def __init__(self, image, position):
		pygame.sprite.Sprite.__init__(self)
		self.src_image = pygame.image.load(image)
		self.position = position
		self.velocityX = 0
		self.velocityY = 0
		self.accelerationX = 0
		self.accelerationY = 0
		self.rect = self.image.get_rect()
		self.rect.center = self.position

	def applyGravity(self): #Physics for you
		self.accelerationY -= GRAVITYCONSTANT*deltaT*self.MASS

	def update(self):
		positionX, positionY = self.position
		self.velocityX += self.accelerationX*deltaT
		if self.velocityX > self.TERMINAL_VELOCITY: self.velocityX = self.TERMINAL_VELOCITY
		elif self.velocityX < -self.TERMINAL_VELOCITY: self.velocityX = -self.TERMINAL_VELOCITY
		positionX += self.velocityX*deltaT
		self.velocityY += self.accelerationY*deltaT
		self.applyGravity()
		if self.velocityY > self.TERMINAL_VELOCITY: self.velocityY = self.TERMINAL_VELOCITY
		elif self.velocityY < -self.TERMINAL_VELOCITY: self.velocityY = -self.TERMINAL_VELOCITY
		positionY += self.velocityY*deltaT
		self.position = (positionX, positionY)
		self.rect.center = self.position

#CONSTANTS
GRAVITYCONSTANT = 10;

#GAME STARTUP
pygame.draw.rect(screen, (0,0,0), (0,0, 2000, 1800), 0) #Fill screen with black
pygame.display.flip()

#MAIN GAME LOOP
while 1:
	deltaT = clock.tick(DEFAULT_FPS) # Returns time(milliseconds) passed after previous call of tick()
	#USER INPUT
	for event in pygame.event.get() :
			if event.type == pygame.KEYDOWN :
				if event.key == pygame.K_ESCAPE :
					#LOAD INGAME MENU TEXTURES
					ingame_menu_background = pygame.image.load('graphics/ingame_menu_background.png').convert()
					INGAME_MENU0_BOX1 = Rect(174, 320, 355, 86)
					INGAME_MENU0_BOX2 = Rect(174, 429, 355, 86)
					INGAME_MENU0_BOX3 = Rect(174, 534, 355, 86)
					INGAME_MENU0_BOX4 = Rect(174, 630, 355, 86)
					ingame_menu_exit = 0
					while ingame_menu_exit == 0 : #Ingame Menu
						deltaT = clock.tick(DEFAULT_FPS)
						#USER INPUT
						for event in pygame.event.get() :
							if event.type == pygame.KEYDOWN :
								if event.key == pygame.K_ESCAPE : ingame_menu_exit = 1
							elif event.type == pygame.MOUSEMOTION :
								cursor.position = event.pos
							elif event.type == pygame.MOUSEBUTTONDOWN :
								if INGAME_MENU0_BOX1.collidepoint(event.pos) == True : pass
								elif INGAME_MENU0_BOX2.collidepoint(event.pos) == True : pass
								elif INGAME_MENU0_BOX3.collidepoint(event.pos) == True : ingame_menu_exit = 1
								elif INGAME_MENU0_BOX4.collidepoint(event.pos) == True : sys.exit(0)
						#RENDERING
						screen.blit(ingame_menu_background, (0,0))
						cursor_group.update()
						cursor_group.draw(screen)
						pygame.display.flip()
	pygame.draw.rect(screen, (0,0,0), (0,0, 2000, 1800), 0) #Fill screen with black - Placeholder
	pygame.display.flip()

