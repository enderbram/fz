import pygame
import math
from random import randrange

pygame.init()
pygame.font.init()

# global variables
running = True
star_mass = 50000
fps = 1.0
(width, height) = (600,600)
G = 10
scale = 1
pre_vel = 100 

# setting up screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Gravity Simulator")	

# making necessary surfaces
background = pygame.Surface((600,600))

# set up the text
basicFont = pygame.font.SysFont('helvetica', 14)

text_vel = "Velocity: " + str(int(pre_vel * scale))
text = basicFont.render(text_vel, True, (255, 255, 255), (0, 0, 0))
textRect = text.get_rect()
textRect.centerx = 45
textRect.centery = 10

# setting up clock
clock = pygame.time.Clock()

# Particle class
class Particle(pygame.sprite.Sprite):
	def __init__(self, (x, y), mass, pre_vel, radius, star):
		pygame.sprite.Sprite.__init__(self)
		# initialize needed variables
		self.x = x
		self.y = y
		self.star = star
		self.mass = mass
		self.radius = radius
		self.thickness = 1
		self.vel = 0
		self.velx = pre_vel
		self.vely = 0
		self.die = False

		# making a surface for the particle
		self.circle = pygame.Surface((radius * 2, radius * 2))
		self.circle = self.circle.convert()
		
		# check which kind of particle object is, and give circle a different size and color depending on what it is.	
		if star:
			pygame.draw.circle(self.circle, (255, 255, 255), (radius, radius), radius)
		else:	
			pygame.draw.circle(self.circle, (randrange(10, 245, 50), randrange(1, 254, 50), randrange(1, 254, 50)), (radius, radius), radius)	
				
		self.circle.set_colorkey(self.circle.get_at((0, 0)), pygame.RLEACCEL)

		# give the circle an .rect
		self.image = self.circle
		self.rect = self.image.get_rect()

		# center the circle
		self.rect[0] = self.x - radius
		self.rect[1] = self.y - radius

	def calc(self):
		# calculating difference in x and y positions
		dx = abs(self.x) - star_x # dirty collision fix
		dy = abs(self.y) - star_y # dirty collision fix

		# calc distance, gravity and velocity
		dz = math.hypot(dx, dy)
		self.gravity = G * ((self.mass * star_mass) / dz**2) 
		self.vel = math.sqrt(self.gravity / (0.5 * self.mass))

		# calculating x and y velocity
		self.velx += dx/dz * self.vel / scale
		self.vely += dy/dz * self.vel / scale

		# updating postions
		dt = 1 / float(fps)
		self.x -= self.velx * dt
		self.y -= self.vely * dt
		self.rect[0] = self.x
		self.rect[1] = self.y 

		# checking for collisions
		radii = self.radius + star_radius
		if dz <= radii:
			self.die = True
	
# enable RenderUpdates
particles = pygame.sprite.RenderUpdates()
stars = pygame.sprite.RenderUpdates()

# blit background and text to screen
screen.blit(background, (0,0))
pygame.display.update(screen.blit(text, textRect))

# make star
(star_x, star_y, star_radius) = (screen.get_width() / 2, screen.get_width() / 2, 70)
stars.add(Particle((star_x, star_y), 1.989e30, 0, 70, True))

# give the star the right pos (kinda dirty)
star_x -= 6
star_y -= 6

pygame.display.update(stars.draw(screen))

# update screen
pygame.display.update()

while running:
	# set fps
	tick = clock.tick(60)

	# check for key/ mouse events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.MOUSEBUTTONDOWN:
			(x, y) = pygame.mouse.get_pos()
			particles.add(Particle((x, y), 1.989e29, pre_vel, 7, False))

		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				pre_vel += 5
				text_vel = "Velocity: " + str(int(pre_vel))
				text = basicFont.render(text_vel, True, (255, 255, 255), (0, 0, 0))
				pygame.display.update(screen.blit(text, textRect))
			elif event.key == pygame.K_DOWN:
				pre_vel -= 5
				text_vel = "Velocity: " + str(int(pre_vel)) + "      "
				text = basicFont.render(text_vel, True, (255, 255, 255), (0, 0, 0))
				pygame.display.update(screen.blit(text, textRect))
			elif event.key == pygame.K_k:
				for particle in particles:
					particles.remove(particle)
			elif event.key == pygame.K_q:
					running = False

	particles.clear(screen, background)

	# get excact fps
	fps = clock.get_fps()
	for particle in particles:
		if particle.star == False:
			particle.calc()
			if particle.die:
				particles.remove(particle)
				pygame.display.update(stars.draw(screen))
				pygame.display.update(screen.blit(text, textRect))
	pygame.display.update(particles.draw(screen))
