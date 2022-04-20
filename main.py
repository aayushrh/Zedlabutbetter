import sys
import pygame
from level import start

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


class Tile(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.Surface((TDIMS, TDIMS))
		self.image.fill(WHITE)
		self.rect = pygame.Rect((x, y), self.image.get_size())

		
class Player:
	def __init__(self):
		self.image = pygame.Surface((TDIMS, TDIMS))
		self.rect = pygame.Rect((0, 0), self.image.get_size())
		self.image.fill(WHITE)

		self.xacel = 0
		self.yacel = 0
		self.friction = 0.9
		self.onground = False
		self.speed = 1
		self.jump = 16

	def update(self, tiles):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_a]:
			self.xacel -= self.speed
		if keys[pygame.K_d]:
			self.xacel += self.speed
		if keys[pygame.K_SPACE] and self.onground:
			self.yacel -= self.jump
			self.onground = False
			self.rect.bottom -= 1

		self.onground = False
		for t in tiles:
			if self.rect.colliderect(t.rect):
				if self.rect.y >= t.rect.y:
					self.yacel = -GRAVITY
					self.onground = False
				elif self.rect.bottom > t.rect.top:
					self.yacel = 0
					self.rect.bottom = t.rect.top + 1
					self.onground = True
				else:
					if self.rect.centerx > t.rect.centerx:
						while self.rect.colliderect(t.rect):
							self.rect.x += 1

		if self.onground:
			self.yacel = 0
		else:
			self.yacel -= GRAVITY

		self.xacel *= self.friction
		self.rect.x += round(self.xacel)
		self.rect.y += round(self.yacel)

	def draw(self):
		SCREEN.blit(self.image, self.rect)


def main():
	player = Player()

	tilegroup = pygame.sprite.Group()

	x, y = 0, 0
	for r in start:
		for t in r:
			if t == 1:
				tilegroup.add(Tile(x, y))
			x += 32
		y += 32
		x = 0

	while True:
		SCREEN.fill(BLACK)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		player.update(tilegroup.sprites())
		#tilegroup.update()

		player.draw()
		tilegroup.draw(SCREEN)

		TRUE_SCREEN.blit(pygame.transform.scale(SCREEN, TRUE_SCREEN.get_size()), (0, 0))
		pygame.display.flip()
		CLOCK.tick(FPS)


if __name__ == "__main__":
	main()
