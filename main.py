#INITIALIZATION
import pygame, math, sys, random
from pygame.locals import *
pygame.init()

screen = pygame.display.set_mode((1024, 768), FULLSCREEN)
pygame.display.set_caption('Project-Giraffeland')
clock = pygame.time.Clock()
logFile = open('log.txt', 'w') #Opens log file, destroys old contents
saveFile = open('save/save.txt', 'w+') #Opens save file
game_start = 0

def log(logpayload):
	timing = pygame.time.get_ticks()
	logFile.write(str(timing))
	logFile.write(' ')
	logFile.write(str(logpayload))
	logFile.write('\n')

log(' Game initialised')

def gameExit(code):
	saveFile.close()
	log('Quitting the game')
	logFile.close()
	pygame.quit()
	sys.exit(code)	

#GLOBAL CONSTANTS
DEFAULT_FPS = 60 #Reasonable estimate for final performance. WE NO NEED MORE THAN 45

#INTRO		
intro_logo = pygame.image.load('graphics/intro_logo.png').convert()
intro_background = pygame.image.load('graphics/intro_background.png').convert()

for i in range(128) : #LOGO FADEIN
	clock.tick(32)
	for event in pygame.event.get() :
			if event.type == pygame.KEYDOWN :
				if event.key == pygame.K_LEFT : game_start = 1
	screen.blit(intro_background, (0,0))
	intro_logo.set_alpha(2*i)
	screen.blit(intro_logo, (200, 200))
	pygame.display.flip()

for i in range(64) : #PAUSE
	clock.tick(32)

pygame.event.clear() #Clears the event list so that user actions during the intro are not processed later
log('Intro finished')

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
log('Menu textures loaded')

screen.blit(background, (0,0))
recta = screen.get_rect()
cursor = CursorSprite('graphics/cursor.png', recta.center)
cursor_group = pygame.sprite.RenderPlain(cursor) #Sprites are always managed in groups, no matter if there is one or over 9k

pygame.mouse.set_visible(0)

MENU0_BOX1 = Rect(196, 444, 553, 60)
MENU0_BOX2 = Rect(196, 564, 553, 60)
MENU0_BOX3 = Rect(196, 621, 553, 60)

MENU1_BOX1 = Rect(382, 462, 274, 60)
MENU1_BOX2 = Rect(472, 219, 158, 63)

MENU2_BOX1 = Rect(382, 462, 274, 60)

MENU3_BOX1 = Rect(382, 462, 274, 60)

menuMode = 0
log('Menu started')

while 1: #Menu loop
	clock.tick(DEFAULT_FPS)

	if menuMode == 0 :
		#USER INPUT
		for event in pygame.event.get() :
			if event.type == pygame.KEYDOWN :
				if event.key == pygame.K_ESCAPE : gameExit(0)
			elif event.type == pygame.MOUSEMOTION :
				cursor.position = event.pos
			elif event.type == pygame.MOUSEBUTTONDOWN :
				if MENU0_BOX1.collidepoint(event.pos) == True : 
					menuMode = 1
					log('Changing to Menu 1')
				elif MENU0_BOX2.collidepoint(event.pos) == True : 
					menuMode = 2
					log('Changing to Menu 2')
				elif MENU0_BOX3.collidepoint(event.pos) == True : 
					menuMode = 3
					log('Changing to Menu 3')
		# RENDERING
		screen.blit(background, (0,0))

	elif menuMode == 1 :
		#USER INPUT
		for event in pygame.event.get() :
			if event.type == pygame.KEYDOWN :
				if event.key == pygame.K_ESCAPE : gameExit(0)
			elif event.type == pygame.MOUSEMOTION :
				cursor.position = event.pos
			elif event.type == pygame.MOUSEBUTTONDOWN :
				if MENU1_BOX1.collidepoint(event.pos) == True :
					menuMode = 0
					log('Changing to Menu 0')
				elif MENU1_BOX2.collidepoint(event.pos) == True : 
					game_start = 1
					log('Starting the game')
		# RENDERING
		screen.blit(menu_background1, (0,0))
	
	elif menuMode == 2 :
		#USER INPUT
		for event in pygame.event.get() :
			if event.type == pygame.KEYDOWN :
				if event.key == pygame.K_ESCAPE : gameExit(0)
			elif event.type == pygame.MOUSEMOTION :
				cursor.position = event.pos
			elif event.type == pygame.MOUSEBUTTONDOWN :
				if MENU2_BOX1.collidepoint(event.pos) == True : 
					menuMode = 0
					log('Changing to Menu 0')
		# RENDERING
		screen.blit(menu_background2, (0,0))
	
	elif menuMode == 3 :
		#USER INPUT
		for event in pygame.event.get() :
			if event.type == pygame.KEYDOWN :
				if event.key == pygame.K_ESCAPE : gameExit(0)
			elif event.type == pygame.MOUSEMOTION :
				cursor.position = event.pos
			elif event.type == pygame.MOUSEBUTTONDOWN :
				if MENU3_BOX1.collidepoint(event.pos) == True : 
					menuMode = 0
					log('Changing to Menu 0')
		# RENDERING
		screen.blit(menu_background3, (0,0))

	cursor_group.update()
	cursor_group.draw(screen)
	pygame.display.flip()
	#GAME START
	if game_start == 1: break

#CLASSES, METHODS, STUFF
def collideEntityRect(entity, recta) :
	if recta.colliderect(entity.rect) == True : 
		if recta.collidepoint(entity.rect.midbottom) == True :
			entity.collidesBottom = True
			return True
		elif recta.collidepoint(entity.rect.midleft) == True :
			entity.collidesRight = True
			return True
		elif recta.collidepoint(entity.rect.midtop) == True :
			entity.collidesTop = True
			return True
		elif recta.collidepoint(entity.rect.midright) == True :
			entity.collidesLeft = True
			return True
		elif recta.collidepoint(entity.rect.bottomright) == True :
			x1,y1 = entity.rect.bottomright
			if x1 > recta.topleft[0] == True :
				entity.collidesBottom = True
				return True
			elif y1 > recta.topleft[1] == True :
				entity.collidesRight = True
				return True
		elif recta.collidepoint(entity.rect.bottomleft) == True :
			x1,y1 = entity.rect.bottomleft
			if x1 < recta.topright[0] == True :
				entity.collidesBottom = True
				return True
			elif y1 > recta.topright[1] == True :
				entity.collidesLeft = True
				return True
		elif recta.collidepoint(entity.rect.topleft) == True :
			x1,y1 = entity.rect.topleft
			if x1 < recta.bottomright[0] == True :
				entity.collidesTop = True
				return True
			elif y1 < recta.bottomright[1] == True :
				entity.collidesLeft = True
				return True
		elif recta.collidepoint(entity.rect.topright) == True :
			x1,y1 = entity.rect.topright
			if x1 > recta.bottomleft[0] == True :
				entity.collidesTop = True
				return True
			elif y1 < recta.bottomleft[1] == True :
				entity.collidesRight = True
				return True
		else : return False

#LEVELGEN
def levelGen() :
	levelGene = False
	while levelGene == False : 
		for i in range(RectNum) :
			RectDemo[i] = Rect(random.randrange(10, 1000), random.randrange(100, 700), random.randrange(50, 400), random.randrange(50, 100))
		levelGene = True
		for i in range(RectNum) :
			for j in range(RectNum) :
				if (RectDemo[i] != RectDemo[j]) & (RectDemo[i].colliderect(RectDemo[j]) == True) : levelGene = False
				elif collideEntityRect(player, RectDemo[i]) == True : levelGene = False

class PlayerSprite(pygame.sprite.Sprite):

	def __init__(self, position):
		pygame.sprite.Sprite.__init__(self)

		#CONSTANTS
		self.MAX_HEALTH = 100
		self.MAX_HORIZ_VELOCITY = 1
		self.MAX_VERT_VELOCITY = 3
		self.JUMP_VELOCITY = 2
		self.MASS = 0.15
		self.IMG_SWITCH = 10
		self.HORIZ_ACC = 0.5
		self.VERT_ACC = 0.5
		#VARIABLES
		self.position = position
		self.lastPositionX = 0
		self.imageNum = 0
		self.velocityX = 0
		self.velocityY = 0
		self.positionX = 0
		self.positionY = 0
		self.health = self.MAX_HEALTH
		#FLAGS
		self.movingLeft = False
		self.movingRight = False
		self.movingDown = False
		self.movingUp = False
		self.collidesLeft = False
		self.collidesRight = False
		self.collidesTop = False
		self.collidesBottom = False

		#IMAGES
		self.src_image0 = pygame.image.load('graphics/player/player0.png').convert_alpha()
		self.image = self.src_image0
		self.rect = self.image.get_rect()
		self.rect.center = self.position
		self.src_imageR= ['0'] * 6
		self.src_imageR[0] = pygame.image.load('graphics/player/playerR0.png').convert_alpha()
		self.src_imageR[1] = pygame.image.load('graphics/player/playerR1.png').convert_alpha()
		self.src_imageR[2] = pygame.image.load('graphics/player/playerR2.png').convert_alpha()
		self.src_imageR[3] = pygame.image.load('graphics/player/playerR3.png').convert_alpha()
		self.src_imageR[4] = pygame.image.load('graphics/player/playerR4.png').convert_alpha()
		self.src_imageR[5] = pygame.image.load('graphics/player/playerR5.png').convert_alpha()
		self.src_imageL= ['0'] * 6
		self.src_imageL[0] = pygame.image.load('graphics/player/playerL0.png').convert_alpha()
		self.src_imageL[1] = pygame.image.load('graphics/player/playerL1.png').convert_alpha()
		self.src_imageL[2] = pygame.image.load('graphics/player/playerL2.png').convert_alpha()
		self.src_imageL[3] = pygame.image.load('graphics/player/playerL3.png').convert_alpha()
		self.src_imageL[4] = pygame.image.load('graphics/player/playerL4.png').convert_alpha()
		self.src_imageL[5] = pygame.image.load('graphics/player/playerL5.png').convert_alpha()

		#MILLANCEOUS
		log('Player model initialised')

	def update(self):
		if self.health < 1 : gameOver = True
		if self.health > self.MAX_HEALTH : 
			self.health = self.MAX_HEALTH

		#COMPUTING VELOCITIES
		if self.movingUp == True : 
			self.velocityY = -self.JUMP_VELOCITY
			self.movingUp = False
		if self.movingDown == True :
			self.velocityY += self.VERT_ACC
		if self.movingRight == True :
			self.velocityX += self.HORIZ_ACC
		elif self.movingLeft == True : 
			self.velocityX -= self.HORIZ_ACC
		#GRAVITY
		self.velocityY += self.MASS * GRAVITY_CONSTANT * deltaT
		#COLLISION RESETS 
		#NEED TO REFACTOR AND COMBINE WITH COLLISIONS
		if (self.collidesRight == True) & (self.velocityX < 0) :
			self.collidesRight = False
		elif (self.collidesLeft == True) & (self.velocityX > 0) :
			self.collidesLeft = False
		if (self.collidesBottom == True) & (self.velocityY < 0) :
			self.collidesBottom = False
		elif (self.collidesTop == True) & (self.velocityY > 0) :
			self.collidesTop = False
		#COLLISIONS
		if (self.collidesRight == True) & (self.velocityX > 0) :
			self.velocityX = 0
		elif (self.collidesLeft == True) & (self.velocityX < 0) :
			self.velocityX = 0
		if (self.collidesBottom == True) & (self.velocityY > 0) :
			self.velocityY = 0
		elif (self.collidesTop == True) & (self.velocityY < 0) :
			self.velocityY = 0
		if (self.collidesBottom == True) & (self.movingRight == False) & (self.movingLeft == False) :
			self.velocityX = 0
		#VELOCITY LIMITS
		if self.velocityX > self.MAX_HORIZ_VELOCITY :
			self.velocityX = self.MAX_HORIZ_VELOCITY
		elif self.velocityX < -self.MAX_HORIZ_VELOCITY :
			self.velocityX = -self.MAX_HORIZ_VELOCITY
		if self.velocityY > self.MAX_VERT_VELOCITY :
			self.velocityY = self.MAX_VERT_VELOCITY
		elif self.velocityY < -self.MAX_VERT_VELOCITY :
			self.velocityY = -self.MAX_HORIZ_VELOCITY

		#MOVEMENT
		self.positionX, self.positionY = self.position
		self.positionX += self.velocityX * deltaT
		self.positionY += self.velocityY * deltaT
		self.position = self.positionX, self.positionY
		self.rect.center = self.position

		#IMAGE CHANGE
		if (self.positionX - self.lastPositionX) > self.IMG_SWITCH : #Moving right
			self.lastPositionX = self.positionX
			self.imageNum = (self.imageNum + 1) % 6
			self.image = self.src_imageR[self.imageNum]
		elif (self.positionX - self.lastPositionX) < -self.IMG_SWITCH : #Moving left
			self.lastPositionX = self.positionX
			self.imageNum = (self.imageNum + 1) % 6
			self.image = self.src_imageL[self.imageNum]
		elif self.positionX == self.lastPositionX : #Not moving
			self.image = self.src_image0

#CONSTANTS
GRAVITY_CONSTANT = 0.05;

#GAME STARTUP
pygame.draw.rect(screen, (0,0,0), (0,0, 2000, 1800), 0) #Fill screen with black
pygame.display.flip()
gamePointer = CursorSprite('graphics/gamePointer.png', (512, 320))
pointer_group = pygame.sprite.RenderPlain(gamePointer)
player = PlayerSprite((512, 400))
player_group = pygame.sprite.RenderPlain(player)
pygame.event.clear() #Clears the event list so that user actions during the loading are not processed later
log('Ending game startup')

RectNum = random.randrange(1, 10)
RectDemo = [Rect(400, 300, 300, 100)] * RectNum
levelGen()



#MAIN GAME LOOP
while 1:
	deltaT = clock.tick(DEFAULT_FPS) # Returns time(milliseconds) passed after previous call of tick()
	#DEMO RECT COLLISIONS
	colliding = 0
	for i in range(RectNum):
		if collideEntityRect(player, RectDemo[i]) == True : colliding = 1
	if colliding != 1 :
		player.collidesBottom = False
		player.collidesTop = False
		player.collidesRight = False
		player.collidesLeft = False

	#DEMO MOVEMENT LIMITS
	if player.positionY > 700 :	player.collidesBottom = True
	elif player.positionY < 60 : player.collidesTop = True
	if player.positionX > 1000 : player.collidesRight = True
	elif player.positionX < 50 : player.collidesLeft = True
	#USER INPUT
	for event in pygame.event.get() :
		if event.type == pygame.KEYDOWN :
			if event.key == pygame.K_ESCAPE :
				#LOAD INGAME MENU
				log('Opening ingame menu')
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
							elif INGAME_MENU0_BOX4.collidepoint(event.pos) == True : gameExit(0)
					#RENDERING
					screen.blit(ingame_menu_background, (0,0))
					cursor_group.update()
					cursor_group.draw(screen)
					pygame.display.flip()
			elif event.key == pygame.K_UP : player.movingUp = True
			elif event.key == pygame.K_DOWN : player.movingDown = True
			elif event.key == pygame.K_LEFT : player.movingLeft = True
			elif event.key == pygame.K_RIGHT : player.movingRight = True
			elif event.key == pygame.K_g : 
				RectNum = random.randrange(2, 10)
				RectDemo = [Rect(400, 300, 300, 100)] * RectNum
				levelGen()

		elif event.type == pygame.KEYUP :
			if event.key == pygame.K_UP : 
				player.movingUp = False
			elif event.key == pygame.K_DOWN : 
				player.movingDown = False
			elif event.key == pygame.K_LEFT : 
				player.movingLeft = False
				player.velocityX = 0
			elif event.key == pygame.K_RIGHT : 
				player.movingRight = False
				player.velocityX = 0

		elif event.type == pygame.MOUSEMOTION : 
			gamePointer.position = event.pos

	#UPDATING
	pointer_group.update()
	player_group.update()
	#RENDERING
	pygame.draw.rect(screen, (0,0,0), (0,0, 2000, 1800), 0) #Fill screen with black - Placeholder
	for i in range(RectNum) :
		pygame.draw.rect(screen, (255,255,255), RectDemo[i], 0) #Draw the rectangle
	pointer_group.draw(screen)
	player_group.draw(screen)
	pygame.display.flip()