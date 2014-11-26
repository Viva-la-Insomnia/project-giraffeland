#INITIALIZATION
import pygame, math, sys
from pygame.locals import *
screen = pygame.display.set_mode((1024, 768), FULLSCREEN)
pygame.display.set_caption('Project-Giraffeland')
clock = pygame.time.Clock()

#GLOBAL CONSTANTS
DEFAULT_FPS = 40 #Reasonable estimate for final performance. We don't really need more than 45

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

MENU1_BOX1 = Rect(196, 444, 553, 60)
MENU1_BOX2 = Rect(196, 564, 553, 60)
MENU1_BOX3 = Rect(196, 621, 553, 60)

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
				if MENU1_BOX1.collidepoint(event.pos) == True : menuMode = 1
				elif MENU1_BOX2.collidepoint(event.pos) == True : menuMode = 2
				elif MENU1_BOX3.collidepoint(event.pos) == True : menuMode = 3
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
				pass
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
				pass
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
				passs
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
#MAIN GAME LOOP
while 1:
	deltaT = clock.tick(DEFAULT_FPS) # Returns time(milliseconds) passed after previous call of tick()
	pass
