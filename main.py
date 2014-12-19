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
pre_vel = 0

# setting up screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Gravity Simulator")	

# making necessary surfaces
background = pygame.Surface((600,600))
circle = pygame.Surface((15,15))

# set up the text
basicFont = pygame.font.SysFont('helvetica', 14)

text_vel = "Velocity: " + str(int(pre_vel))
text = basicFont.render(text_vel, True, (255, 255, 255), (0, 0, 0))
textRect = text.get_rect()
textRect.centerx = 45
textRect.centery = 10

# setting up clock
clock = pygame.time.Clock()

# Particle class
class Particle(pygame.sprite.Sprite):
	def __init__(self, (x, y), mass, pre_vel, circle):
		pygame.sprite.Sprite.__init__(self)
		self.x = x
		self.y = y
		self.mass = mass
		self.radius = int(mass / 100)
		self.color = (255, 255, 255)
		self.thickness = 1
		self.vel = 0
		self.velx = pre_vel
		self.vely = 0
		self.die = False
		self.image = circle
		self.rect = self.image.get_rect()

	def calc(self):
		# calc distance, gravity and velocity
		d = math.hypot(star.x - self.x, star.y - self.y)
		self.gravity = (self.mass * star_mass) / d**2
		self.vel = math.sqrt(self.gravity * 150 / (0.5 * self.mass + star_mass))

		# calculating difference in x and y positions
		dx = self.x - star.x
		dy = self.y - star.y

		dz = math.sqrt(dx**2 + dy**2)

		# calculating x and y velocity
		self.velx += dx/dz * self.vel
		self.vely += dy/dz * self.vel

		# updating postions
		dt = 1 / float(fps)
		self.x -= int(self.velx * dt)
		self.y -= int(self.vely * dt)
		self.rect[0] = self.x
		self.rect[1] = self.y

		# checking for collisions
		radii = self.radius + star.radius
		distance = math.sqrt(((dx) * (dx)) + ((dy) * (dy)))
		if distance < radii:
			self.die = True

	def draw(self):
		pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, self.thickness)
		
# enable RenderUpdates
particles = pygame.sprite.RenderUpdates()
star = pygame.sprite.RenderUpdates()

# blit background and text to screen
screen.blit(background, (0,0))
pygame.display.update(screen.blit(text, textRect))

# making and drawing star
circle = pygame.Surface((500, 500))
circle = circle.convert()
pygame.draw.circle(circle, (255, 255, 255), (screen.get_width() / 2, screen.get_height() / 2), 50, 0)
circle.set_colorkey(circle.get_at((0, 0)), pygame.RLEACCEL)

star.add(Particle((300, 300), 0, 0, circle))
(star.x, star.y, star.radius, star.pre_vel) = (screen.get_width() / 2 , screen.get_height() / 2, 60, 0)
pygame.display.update(star.draw(screen))

# update screen
pygame.display.update()

while running:
	# get fps
	fps = clock.tick(60)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.MOUSEBUTTONDOWN:
			(x, y) = pygame.mouse.get_pos()

			circle = pygame.Surface((15,15))
			circle = circle.convert()
			pygame.draw.circle(circle, (randrange(10, 245, 50), randrange(1, 254, 50), randrange(1, 254, 50)), (int(7.5), int(7.5)), int(7.5), 0)
			circle.set_colorkey(circle.get_at((0, 0)), pygame.RLEACCEL)

			particles.add(Particle((x, y), 450, pre_vel, circle))

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
			
	particles.clear(screen, background)

	for particle in particles:
		particle.calc()

		if particle.die:
			particles.remove(particle)
			pygame.display.update(star.draw(screen))
			pygame.display.update(screen.blit(text, textRect))

	pygame.display.update(particles.draw(screen))


