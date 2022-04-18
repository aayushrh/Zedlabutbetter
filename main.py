import sys
import pygame

pygame.init()

WIDTH, HEIGHT = 1280, 720
PWIDTH, PHEIGHT = 10, 10
GROUND_LVL = HEIGHT
GRAVITY = -1

FPS = 60
CLOCK = pygame.time.Clock()
TRUE_SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
SCREEN = pygame.Surface((WIDTH, HEIGHT))

BLACK = "#000000"
WHITE = "#FFFFFF"


class Player:
	def __init__(self):
		self.image = pygame.Surface((PWIDTH, PHEIGHT))
		self.rect = pygame.Rect((0, 0), self.image.get_size())
		self.image.fill(WHITE)

		self.xacel = 0
		self.yacel = 0
		self.friction = 0.9
		self.onground = False
		self.speed = 1
		self.jump = 15

	def update(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_a]:
			self.xacel -= self.speed
		if keys[pygame.K_d]:
			self.xacel += self.speed

		if self.rect.bottom >= GROUND_LVL:
			self.onground = True
			self.yacel = 0
			self.rect.bottom = GROUND_LVL
		else:
			self.onground = False
			self.yacel -= GRAVITY

		if keys[pygame.K_SPACE] and self.onground:
			self.yacel -= self.jump
			self.onground = False

		self.xacel *= self.friction
		self.rect.x += round(self.xacel)
		self.rect.y += round(self.yacel)

	def draw(self):
		SCREEN.blit(self.image, self.rect)

def main():

	player = Player()

	while True:
		SCREEN.fill(BLACK)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		player.update()

		player.draw()

		TRUE_SCREEN.blit(pygame.transform.scale(SCREEN, TRUE_SCREEN.get_size()), (0, 0))
		pygame.display.flip()
		CLOCK.tick(FPS)

if __name__ == "__main__":
	main()
