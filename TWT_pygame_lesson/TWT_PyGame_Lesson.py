# Pygame lesson by Tim Ruscica (A.K.A. "Tech wih Tim"):

import pygame as pg
from pygame.image import load as il
pg.init()

w_width = 900 
w_height = 500

window = pg.display.set_mode((w_width,w_height)) #defines the size of the window, needs to be passed in a tuple

pg.display.set_caption("Test Game")

#load in images:

walk_right = [il(f"R{i}.png") for i in range(1, 10)]
walk_left = [il(f"L{i}.png") for i in range(1, 10)]
bg = il("background2.jpg")
char = il("standing.png") #image for standstill/jump

##OOP: game objects
class player:
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.vel = 5
		self.is_jump = False
		self.jump_count = 10
		self.left = False    #char facing left
		self.right = False   #char facing right
		self.walk_count = 0
		self.standing = True
		self.hitbox = (self.x + 17, self.y + 11, 29, 52) #shrink the hitbox rectangle

	def draw(self, win):
		if self.walk_count + 1 >= 27: #to avoid index error of looping on sprite
			self.walk_count = 0

		if not(self.standing):
			if self.left:
				win.blit(walk_left[self.walk_count//3], (self.x, self.y)) #so it loops through all 9
				self.walk_count += 1
			elif self.right:
				win.blit(walk_right[self.walk_count//3], (self.x, self.y)) #so it loops through all 9
				self.walk_count += 1
		else:
			if self.right:
				win.blit(walk_right[0], (self.x, self.y))
			else:
				win.blit(walk_left[0], (self.x, self.y))
		self.hitbox = (self.x + 17, self.y + 11, 29, 52) #so it updates per tick
		pg.draw.rect(window, (255, 0,0), self.hitbox, 2) #draw hitbox inspector

class projectile:
	def __init__(self, x, y, radius, color, facing):
		self.x = x
		self.y = y
		self.radius = radius
		self.color = color
		self.facing = facing    # +/- 1 to indicate facing direction
		self.vel = 8 * facing

	def draw(self, win):
		pg.draw.circle(win, self.color,(self.x, self.y), self.radius)	


class enemy:
	walk_right = [il(f"R{i}E.png") for i in range(1, 12)]
	walk_left = [il(f"L{i}E.png") for i in range(1, 12)]

	def __init__(self, x, y, width, height, end):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.end = end
		self.walk_count = 0
		self.vel = 3
		self.path = [self.x, self.end] #start and end of animation loop for enemy
		self.hitbox = (self.x + 17, self.y + 2, 31, 57)

	def draw(self, win):
		self.move()
		if self.walk_count + 1 >= 33:
			 self.walk_count = 0
		
		if self.vel > 0:
			win.blit(self.walk_right[self.walk_count//3], (self.x, self.y))
			self.walk_count += 1
		else:
			win.blit(self.walk_left[self.walk_count//3], (self.x, self.y))
			self.walk_count += 1

		self.hitbox = (self.x + 17, self.y + 2, 31, 57) #so it updates per tick
		pg.draw.rect(window, (255, 0,0), self.hitbox, 2)

	def move(self):
		if self.vel > 0:
			if self.x + self.vel < self.path[1]:
				self.x += self.vel
			else:
				self.vel *= -1
				self.walk_count = 0
		else:
			if self.x - self.vel > self.path[0]:
				self.x += self.vel
			else:
				self.vel *= -1                     #neg*neg = pos
				self.walk_count = 0

	def hit(self):
		pass

#clock var for framerate:
clock = pg.time.Clock() 

#scene redraw function:
def redraw_game_window(): #this function draws every scene, i.e. the bg, rect
	window.blit(bg, (0,0)) #place background anchor at specific coordinate 
	sprite.draw(window)
	goblin.draw(window)
	for bullet in bullets:
		bullet.draw(window)

	pg.display.update()

# PROGRAMMATIC CONEPT OF A GAME: a game is an infinite loop with
# peroidic checks for end states

#############
#	MAIN	#
#############

sprite =  player(10, 430, 64, 64)
bullets = []
goblin = enemy(100, 436, 64, 64, 450)
run = True
while run: 
	#time delay so things don't happen super quick; parameter is in ms
	clock.tick(27) 
	#check events (AKA inputs from player)
	for event in pg.event.get(): # pg.event.get() gets a list of all events
		if event.type == pg.QUIT: #pg.QUIT == closed the game
			run = False

	for bullet in bullets:
		if bullet.x < w_width and bullet.x > 0:
			bullet.x += bullet.vel
		else:
			bullets.pop(bullets.index(bullet)) #find specific bullet and remove from list of bullets

	#obtaining all keystroke events:
	keys = pg.key.get_pressed()

	if keys[pg.K_SPACE]:
		if sprite.left:
			facing = -1
		else:
			facing = 1

		if len(bullets) < 5:
			bullets.append( projectile(round(sprite.x + sprite.width // 2),
				round(sprite.y + sprite.height // 2), 6, (0,0,0), facing))

	if keys[pg.K_a] and sprite.x > sprite.vel:                       #take into account position of character's top left against x of window limit
		sprite.x -= sprite.vel                                     	  #subtract velocity amount of distance from x axis (AKA go left)
		sprite.left, sprite.right = True, False
		sprite.standing = False

	elif keys[pg.K_d] and sprite.x < w_width - (sprite.width + sprite.vel): #take into account character's dimensions 
		sprite.x += sprite.vel
		sprite.left, sprite.right = False, True
		sprite.standing = False

	else:
		sprite.standing = True
		sprite.walk_count = 0

	if not sprite.is_jump: #this block is to prevent character from moving up/down while in mid jump
		
		if keys[pg.K_w]: 
			sprite.is_jump = True
			sprite.left = sprite.right = False
			sprite.walk_count = 0
	else:
		if sprite.jump_count >= -10:                          
			sprite.y -= (sprite.jump_count*abs(sprite.jump_count)) * 0.5 #this is the jump equation. the jump is performed by updating the character's y value in an 
			sprite.jump_count -= 1						    #inverted parabolic equation.
		else:
			sprite.is_jump = False #end jump. reset jump state
			sprite.jump_count = 10 #reset jump count value
	redraw_game_window()
	
#end program/close window
pg.quit()