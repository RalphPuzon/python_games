#snake game from kite youtube lesson

import pygame as pg 
import sys
import random

#GAME OBJECTS:
class snake(object):
	def __init__(self):
		self.length = 1
		self.positions = [((SCREEN_WIDTH/2), (SCREEN_HEIGHT/2))]
		self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
		self.color = (17, 24, 47)
		self.score = 0 

	def get_head_position(self):
		return self.positions[0]

	def turn(self,point):
		#if snake is just 1 block, it can move any direction
		#else it can't move back
		if self.length > 1 and (point[0] * -1,
			point[1]*-1) == self.direction:
			return
		else:
			self.direction = point

	def move(self):
		#get current head position
		cur = self.get_head_position()
		#get  current direction
		x, y = self.direction
		# calc new head position using screen width and grid size
		new = (((cur[0] + (x*GRIDSIZE)) % SCREEN_WIDTH),
			   ((cur[1] + (y*GRIDSIZE)) % SCREEN_HEIGHT))
		#if the head overlaps any part of the snake, game over and reset
		#else 
		if len(self.positions) > 2 and new in self.positions[2:]:
			self.reset()
		else:
			self.positions.insert(0, new)
			if len(self.positions) > self.length:
				self.positions.pop() #tail disappear

	def reset(self): #game ends
		self.length = 1
		self.positions = [((SCREEN_WIDTH/2), (SCREEN_HEIGHT/2))]
		self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
		self.score = 0

	def draw(self, surface): #the function that draws every snake frame
		for p in self.positions:
			r = pg.Rect((p[0], p[1]),(GRIDSIZE, GRIDSIZE))
			pg.draw.rect(surface, self.color, r)
			pg.draw.rect(surface, (93, 216, 228), r, 1)

	def handle_keys(self):#handle inputs
		for event in pg.event.get():
			if event.type == pg.QUIT: #if window closed, exit.
				pg.quit()
				sys.exit()
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_UP:
					self.turn(UP)
				elif event.key == pg.K_DOWN:
					self.turn(DOWN)
				elif event.key == pg.K_LEFT:
					self.turn(LEFT)
				elif event.key == pg.K_RIGHT:
					self.turn(RIGHT)

class food(object):
	def __init__(self):
		self.position = (0, 0)
		self.color = (223, 163, 49)
		self.randomize_position()

	def randomize_position(self):  
		self.position = (random.randint(0, GRID_WIDTH-1) * GRIDSIZE,
			             random.randint(0, GRID_HEIGHT-1) * GRIDSIZE)

	def draw(self, surface):
		r = pg.Rect((self.position[0], self.position[1]),
			        (GRIDSIZE, GRIDSIZE))
		pg.draw.rect(surface, self.color, r)
		pg.draw.rect(surface, (93, 216, 228), r, 1)

#HELPER FUNCTIONS
def drawGrid(surface): #to draw the background grid:
	for y in range(0, int(GRID_HEIGHT)):        # loop over (x,y) coordinate
		for x in range(0, int(GRID_WIDTH)):     # and draw alternating
			if (x + y) % 2 == 0 :               # light-dark squares
				r = pg.Rect((x*GRIDSIZE, y*GRIDSIZE),
					        (GRIDSIZE, GRIDSIZE))
				pg.draw.rect(surface, (93, 216, 228), r)
			else:
				rr = pg.Rect((x*GRIDSIZE, y*GRIDSIZE),
					         (GRIDSIZE, GRIDSIZE))
				pg.draw.rect(surface, (84, 194, 205), rr)

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480

GRIDSIZE = 20
GRID_WIDTH = SCREEN_HEIGHT/GRIDSIZE
GRID_HEIGHT = SCREEN_WIDTH/GRIDSIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def main():
	#init pygame:
	pg.init()
	#init clock and screen:
	clock = pg.time.Clock() #to keep track of each action at a given time.
	screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
	#draw screen in surface that gets updated whenever an action is performed:
	surface = pg.Surface(screen.get_size()) 
	surface = surface.convert()
	drawGrid(surface)
	#instantiate in game objects:
	Snake = snake()
	Food = food()
	myfont = pg.font.SysFont("monospace", 16)
	
	while True:
		clock.tick(10) #tick clock at 10fps
		Snake.handle_keys()#check for events and record as a comment
		drawGrid(surface)#update and refresh screen once actions acquired
		Snake.move()
		if Snake.get_head_position() == Food.position:
			Snake.length += 1
			Snake.score += 1
			Food.randomize_position()
		Snake.draw(surface)
		Food.draw(surface)
		screen.blit(surface, (0, 0))
		#display score as text
		text = myfont.render("SCORE: {0}".format(Snake.score), 1, (0, 0, 0))
		screen.blit(text, (5, 10))
		pg.display.update()

main()