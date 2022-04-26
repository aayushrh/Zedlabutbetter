import sys
import pygame
import level
from random import randint

pygame.init()

WIDTH, HEIGHT = 1024, 576
TDIMS = 32
GRAVITY = -1

FPS = 60
CLOCK = pygame.time.Clock()
TRUE_SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
SCREEN = pygame.Surface((WIDTH, HEIGHT))

BLACK = "#000000"
WHITE = "#FFFFFF"


# returns startpos
def loadlevel(level, tilegroup):
	tilegroup.empty()
	x, y = 0, 0
	startpos = (0, 0)
	for r in level:
		for t in r:
			if t == 1:
				tilegroup.add(Tile(x, y, 0))
			if t == 3:
				tilegroup.add(Tile(x, y, 1))
			if t == 2:
				startpos = (x, y)
			x += 32
		y += 32
		x = 0
	return startpos


class Tile(pygame.sprite.Sprite):
	def __init__(self, x, y, mode):
		super().__init__()
		self.image = pygame.Surface((TDIMS, TDIMS))
		self.rect = pygame.Rect((x, y), self.image.get_size())
		self.type = mode
		# 0 is normal
		# 1 is kill
		# 2 is moving
		self.col = (WHITE if self.type != 1 else BLACK)
		self.image.fill(self.col)


class Player:
	def __init__(self, pos):
		self.image = pygame.Surface((TDIMS, TDIMS))
		self.rect = pygame.Rect(pos, self.image.get_size())
		self.image.fill(WHITE)

		self.xacel = 0
		self.yacel = 0
		self.friction = 0.75
		self.onground = False
		self.speed = 2
		self.jump = 16
		self.offscreen = "no"  # can be no, up, dw, lf, rt
		# used to change level
		self.dead = False

		self.save = pos + (0, 0)
		self.pause = False

	def update(self, tiles):
		# input
		keys = pygame.key.get_pressed()

		if keys[pygame.K_a]:
			self.xacel -= self.speed
		if keys[pygame.K_d]:
			self.xacel += self.speed
		if keys[pygame.K_SPACE] and self.onground:
			self.yacel -= self.jump
			self.onground = False
			self.rect.bottom -= 1
		if keys[pygame.K_TAB]:
			self.rect.x, self.rect.y, self.xacel, self.yacel = self.save
		if keys[pygame.K_LSHIFT]:
			self.save = (self.rect.x, self.rect.y, self.xacel, self.yacel)

		# collision
		self.onground = False
		for t in tiles:
			if self.rect.colliderect(t.rect):
				if t.type == 1:
					self.dead = True
					break
				if self.rect.y >= t.rect.y:
					self.onground = False
					self.yacel = -GRAVITY
				if self.rect.bottom > t.rect.top > self.rect.bottom - TDIMS:
					self.yacel = 0
					self.rect.bottom = t.rect.top + 1
					self.onground = True
				else:
					counter = 0
					if self.rect.centerx < t.rect.centerx:
						while self.rect.colliderect(t.rect):
							self.rect.x -= 1
							counter += 1
						if counter >= TDIMS / 2:
							self.rect.x += counter
						else:
							self.rect.x -= 1
							self.xacel *= -1.1
					if self.rect.centerx > t.rect.centerx:
						while self.rect.colliderect(t.rect):
							self.rect.x += 1
							counter += 1
						if counter >= TDIMS / 2:
							self.rect.x -= counter
						else:
							self.rect.x += 1
							self.xacel *= -1.1

		# applying gravity and friction
		if self.onground:
			self.yacel = 0
		else:
			self.yacel -= GRAVITY
		self.xacel *= self.friction * (1 if self.onground else 1.1)
		# applying acels to rect
		self.rect.x += round(self.xacel)
		self.rect.y += round(self.yacel)

		# checking if offscreen
		if self.rect.left < 0:
			self.offscreen = "lf"
		elif self.rect.right >= WIDTH:
			self.offscreen = "rt"
		elif self.rect.top < 0:
			self.offscreen = "up"
		elif self.rect.bottom >= HEIGHT:
			self.offscreen = "dw"
		else:
			self.offscreen = "no"
		self.rect.clamp_ip(SCREEN.get_rect())

	def draw(self):
		SCREEN.blit(self.image, self.rect)


def main():
	tilegroup = pygame.sprite.Group()

	startpos = loadlevel(level.start, tilegroup)

	player = Player(startpos)

	lastdir = "dw"

	levelscount = 0
	oldtime = pygame.time.get_ticks()

	while True:
		SCREEN.fill(BLACK)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		player.update(tilegroup.sprites())
		if player.dead:
			main()
			return 0
		if levelscount >= 5:
			print((pygame.time.get_ticks() - oldtime) / 1000)
			return 0
		if player.offscreen != "no" and (
				(player.offscreen == "up" and lastdir != "dw") or (player.offscreen == "lf" and lastdir != "rt") or (
				player.offscreen == "rt" and lastdir != "lf") or (player.offscreen == "dw" and lastdir != "up")):
			while True:
				try:
					startpos = loadlevel(eval(f"level.{player.offscreen}{randint(0, 20)}"), tilegroup)
					player.rect.x, player.rect.y = startpos
					lastdir = player.offscreen
					if player.offscreen == "up":
						player.yacel = -player.jump
					levelscount += 1
					player.save = startpos + (0, 0)
					break
				except AttributeError:
					continue

		player.draw()
		tilegroup.draw(SCREEN)

		TRUE_SCREEN.blit(pygame.transform.scale(SCREEN, TRUE_SCREEN.get_size()), (0, 0))
		pygame.display.flip()
		CLOCK.tick(FPS)


if __name__ == "__main__":
	main()
