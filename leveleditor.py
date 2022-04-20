import sys, pygame
from math import floor
from level import start
from copy import deepcopy as copy

pygame.init()

WIDTH, HEIGHT = 1024, 576
TDIMS = 32

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


def main():
	tilegroup = pygame.sprite.Group()

	while True:
		SCREEN.fill(BLACK)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				
				tiles = tilegroup.sprites()
				
				
				with open("testlevel.py", 'a') as f:
					f.write(f"\n{sys.argv[1]} = {level}")
				
				pygame.quit()
				sys.exit()

		if pygame.mouse.get_pressed()[0]:
			x, y = pygame.mouse.get_pos()
			x = floor(x/32)*32
			y = floor(y/32)*32
			shouldadd = True
			for t in tilegroup.sprites():
				if t.rect.x == x and t.rect.y == y:
					shouldadd = False
					break
			if shouldadd:
				tilegroup.add(Tile(x, y))
				
		tilegroup.update()

		tilegroup.draw(SCREEN)

		TRUE_SCREEN.blit(pygame.transform.scale(SCREEN, TRUE_SCREEN.get_size()), (0, 0))
		pygame.display.flip()
		CLOCK.tick(FPS)


if __name__ == "__main__":
	main()